import requests
import os
import json
from collections import Counter
from analysis.word import draw_words_freq
from analysis import util
from analysis.util import urls_from_text, categorize_edp_url
from analysis.scraptopic import cat_from_url
from analysis.category import draw_count
from analysis.keyword import get_top_terms

search_query = "data.europa.eu"


def get_questions_json():
    json_path = os.path.join('data', 'stackoverflow', 'questions.json')
    if os.path.exists(json_path):
        print("Json already exists: %s" % json_path)
    else:
        body_query = search_query
        # uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&body=%s&site=stackoverflow" % body_query
        uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&q=%s&site=stackoverflow&filter=!nKzQUR30SM" % body_query
        r = requests.get(uri)
        with open(json_path, 'w') as f:
            f.write(r.text)
    with open(json_path) as f:
        j = json.load(f)
    return j


def get_tags(j):
    tags = []
    for p in j['items']:
        for t in p["tags"]:
            tags.append(t.strip().lower())
    return tags


def get_urls(j):
    urls = []
    for p in j['items']:
        urls += p['urls']
    return urls


def include_only_cats(j, cats):
    """
    Only include urls from the provided categories
    :param j:
    :param cats:
    :return:
    """
    to_be_deleted = []
    for pid, p in enumerate(j['items']):
        urls = []
        p['categories'] = []
        for url in p['urls']:
            cat = categorize_edp_url(url)
            if cat in cats:
                urls.append(url)
                p['categories'].append(cat)
            else:
                print("skip: %s" % url)
        p['urls'] = urls
        if len(p['urls']) == 0:
            to_be_deleted.append(pid)

    for pid in to_be_deleted[::-1]:
        del j['items'][pid]


def add_urls(j):
    """
    Add urls extracted from the body of the post
    :param j:
    :return:
    """
    seps = ["\n", "\r", "##", "[", "]", ")", "(", "<", ">", ";", ": ", "\t", " "]
    for p in j['items']:
        body_clean = p["body_markdown"].replace("\n", " ").replace("\r", " ")
        p['urls'] = urls_from_text(text=body_clean, search_query=search_query, seps=seps)


def get_posts(j):
    posts = []
    for p in j['items']:
        posts.append(p["body_markdown"])
    return posts
    

def draw_dataset_edp_cat(urls):
    cats = []
    # related_urls = [u for u in urls if "dataset" in u]
    # print("related urls: %d" % len(related_urls))
    for u in urls:
        if categorize_edp_url(u) == util.CATEGORY_DATASET:
        # if 'dataset' in u:
            c = cat_from_url(u)
            cats += c
        # else:
        #     print("un related: %s" % u)
    print("categories: ")
    print(cats)
    draw_count(Counter(cats), "stackoverflow_datasets_cats.svg", palette="viridis", rotation=90, margins={'bottom': 0.5})


def get_categories(j):
    cats = []
    for p in j['items']:
        cats += p['categories']
    return Counter(cats)


def workflow():
    j = get_questions_json()
    add_urls(j)
    all_posts = get_posts(j)
    include_only_cats(j, [util.CATEGORY_DATASET, util.CATEGORY_DATA_STORY])
    posts = get_posts(j)
    print("%d posts are found. Only %d have either data or data story url" % (len(all_posts), len(posts)))
    tags = get_tags(j)
    draw_words_freq(tags, topk=10, out_fname="stackoverflow_tags.svg")
    top_terms = get_top_terms(posts, k_per_doc=20, top_k=0, min_len=3)
    draw_words_freq(top_terms, topk=20, ylabel="keywords", out_fname="stackoverflow_keywords.svg")

    urls = get_urls(j)
    for u in urls:
        print(u)
    draw_dataset_edp_cat(urls)
    cat_count = get_categories(j)
    draw_count(cat_count, "stackoverflow_cat.svg")


if __name__ == "__main__":
    workflow()
