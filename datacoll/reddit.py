import requests
import os
import json
from analysis import util
from analysis.util import ppretty, parse, categorize_edp_url, urls_from_text
from analysis.category import draw_cat_per_sub, draw_count
from analysis.classify import classify_nlp4types
from analysis.word import draw_words_freq
from analysis.scraptopic import cat_from_url
from analysis.keyword import get_top_terms
from collections import Counter


edp_search_query = "data.europa.eu"


def split_into_subreddits(d):
    per_sub = dict()
    for j in d['data']['children']:
        sub = j["data"]["subreddit"]
        if sub not in per_sub:
            per_sub[sub] = {'posts': []}
        rec = {'url': j["data"]["url"], 'score': j["data"]["score"], 'title': j["data"]["title"], 'class': '',
               'upvote_ratio': j["data"]["upvote_ratio"], 'ups': j["data"]["ups"], 'kind': j["kind"],
               'text': j["data"]["selftext"]}
        if j["data"]["selftext"].strip() != "":
            rec['class'] = classify_nlp4types(j["data"]["selftext"], cache=os.path.join("data", "reddit", "nlp4types"))
        per_sub[sub]['posts'].append(rec)
    return per_sub


def fetch_urls(d):
    for sub in d:
        d[sub]['urls'] = []
        for post in d[sub]['posts']:
            post['urls'] = []
            if post['kind'] == "t3":
                url_list = urls_from_text(text=post['text'], search_query=edp_search_query, seps=["\n", "\r"])
                if len(url_list) > 0:
                    post['urls'] = url_list

                url = post['url']
                if edp_search_query in url:
                    post['urls'].append(post['url'])
            else:
                print("kind is not t3: ")
                ppretty(post)

            d[sub]['urls'] += post['urls']


def search_subreddit():
    search_query = "data.europa.eu"
    subreddit = "datasets"
    json_path = os.path.join('data', 'reddit', subreddit + ".json")
    if os.path.exists(json_path):
        print("Ignore search. %s already exists" % json_path)
    else:
        url = "https://www.reddit.com/r/%s/search.json?q=%s&limit=100" % (subreddit, search_query)
        print("request url: %s" % url)
        # Just to get ride of the error Too many requests
        r = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        with open(json_path, 'w') as f:
            f.write(r.text)
    with open(json_path) as f:
        j = json.load(f)
    return j


def only_include_cat(d, cats):
    """
    Only include urls of a certain edp category. This was mainly done to only include data story and dataset categories.
    :param d:
    :param cats:
    :return:
    """
    print("\n\n===============\nonly_include_cat: ")
    for sub in d:
        print("\n---------\nsub[%s]" % sub)
        urls = []
        ids_to_delete = []
        for post_id, post in enumerate(d[sub]['posts']):
            post_urls = []
            for url in post['urls']:
                url_cat = categorize_edp_url(url)
                if url_cat in cats:
                    post_urls.append(url)
                else:
                    print("ignore: %s" % (url))
            post['urls'] = post_urls
            if len(post_urls) == 0:
                ids_to_delete.append(post_id)
            urls += post_urls

        for post_id in ids_to_delete[::-1]:
            print("deleting post: ")
            print(d[sub]['posts'][post_id])
            del d[sub]['posts'][post_id]

        d[sub]['urls'] = urls



# def url_from_text(text):
#     urls = []
#     for t in text.split(' '):
#         for token in parse(t, seps=["\n", "\r"]):
#             token = token.strip()
#             if token == "":
#                 continue
#             if edp_search_query not in token:
#                 continue
#             cleaned_token = ""
#             # skip if the start of the toke is not h for http or d for data
#             for i in range(len(token)):
#                 if token[i:i + 4] in ["http"]:
#                     cleaned_token = token[i:]
#                     break
#             if cleaned_token != "":
#                 urls.append(cleaned_token)
#     return urls


def force_https(urls):
    urls_https = []
    for u in urls:
        if u.startswith("http://"):
            u = u.replace("http://", "https://")
        urls_https.append(u)
    return urls_https


def clean_urls(urls):
    c_urls = []
    for u in urls:
        u = u.split("[")[0]
        u = u.split("]")[0]
        u = u.split(",")[0]
        u = u.split(")")[0]
        u = u.split('"')[0]
        c_urls.append(u)
    return c_urls


def categorize_urls(urls):
    cats = [categorize_edp_url(u) for u in urls]
    return dict(Counter(cats))


def add_category(d):
    for sub in d:
        d[sub]['categories'] = categorize_urls(d[sub]['urls'])
    return d


def remove_empty(d):
    subs = list(d.keys())
    for sub in subs:
        d[sub]['categories'] = categorize_urls(d[sub]['urls'])
        if not d[sub]['urls']:
            del d[sub]


def get_cat_merged(d):
    cat_count = Counter([])
    for sub in d:
        cat_count += d[sub]['categories']
    return cat_count


def get_classes(d):
    classes = []
    for sub in d:
        for post in d[sub]['posts']:
            if post['class'] == "":
                continue
            classes.append(post['class'])
    return classes


def draw_dataset_edp_cat(d):
    urls = []
    for sub in d:
        urls += d[sub]['urls']
    cats = []
    for u in urls:
        if 'dataset' in u:  #or ('/data/' in u and not u.endswith('/data/')):
            # print("\ntesting: %s" % u)
            c = cat_from_url(u)
            # print(c)
            cats += c
    print("categories: ")
    print(cats)
    draw_count(Counter(cats), "reddit_datasets_cats.svg", palette="viridis", rotation=90, margins={'bottom': 0.5})


def get_posts(d):
    posts = []
    for sub in d:
        for post in d[sub]['posts']:
            if post['kind'] == "t3":
                posts.append(post['text'])
    return posts


def workflow():
    d = search_subreddit()
    d = split_into_subreddits(d)
    fetch_urls(d)
    remove_empty(d)
    only_include_cat(d, [util.CATEGORY_DATASET, util.CATEGORY_DATA_STORY])
    d = add_category(d)

    posts = get_posts(d)
    top_terms = get_top_terms(posts, k_per_doc=20, top_k=0, min_len=3)
    draw_words_freq(top_terms, topk=20, ylabel="Keywords", out_fname="reddit_keywords.svg")

    draw_cat_per_sub(d, "reddit_cat_per_sub.svg", palette="magma_r")
    cat_count = get_cat_merged(d)
    draw_count(cat_count, "reddit_cat.svg",margins={'bottom':0.6})
    classes = get_classes(d)
    draw_words_freq(classes, 100, palette="mako", out_fname="reddit_class.svg")
    draw_dataset_edp_cat(d)


if __name__ == "__main__":
    workflow()
