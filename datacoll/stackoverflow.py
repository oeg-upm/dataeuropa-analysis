import requests
import os
import json
from collections import Counter
from analysis.word import draw_words_freq
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
        # body_query = "data.europa.eu"
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


def get_urls(posts):
    urls = []
    seps = ["\n", "\r", "##", "[", "]", ")", "(", "<", ">", ";", ": ", "\t", " "]
    # posts = get_content(j)
    for p in posts:
        urls += urls_from_text(text=p.replace("\n", " ").replace("\r", " "), search_query=search_query, seps=seps)
    return urls


def get_content(j):
    posts = []
    for p in j['items']:
        posts.append(p["body_markdown"])
    return posts
    

# def get_keywords(body):
#     keywords = []
#     tokens = body.replace("\n", " ").replace("\t", " ").split(" ")
#     for token in tokens:
#         t = token.strip().lower()


# def get_ids_from_q_json(j):
#     ids = []
#     for q in j["items"]:
#         ids.append(str(q["question_id"]))
#     return ids
#
#
# def get_questions_body(ids):
#     if len(ids) > 100:
#         print("The maximum number of ids than can be handled by the API is 100. ")
#     print("ids: ")
#     print(ids)
#     ids_str = ";".join(ids)
#     uri = "https://api.stackexchange.com/2.3/questions/%s?order=desc&sort=activity&site=stackoverflow" % ids_str
#     r = requests.get(uri)
#     json_path = os.path.join('data', 'stackoverflow', 'qbody.json')
#     if os.path.exists(json_path):
#         print("Json already exists: %s" % json_path)
#     else:
#         with open(json_path, 'w') as f:
#             f.write(r.text)
#     with open(json_path) as f:
#         j = json.load(f)
#     return j


def draw_dataset_edp_cat(urls):
    cats = []
    # related_urls = [u for u in urls if "dataset" in u]
    # print("related urls: %d" % len(related_urls))
    for u in urls:
        if 'dataset' in u:
            c = cat_from_url(u)
            cats += c
        # else:
        #     print("un related: %s" % u)
    print("categories: ")
    print(cats)
    draw_count(Counter(cats), "stackoverflow_datasets_cats.svg", palette="viridis", rotation=90, margins={'bottom': 0.5})


def get_categories(urls):
    cats = [categorize_edp_url(url) for url in urls]
    return Counter(cats)


def workflow():
    j = get_questions_json()
    tags = get_tags(j)
    draw_words_freq(tags, topk=10, out_fname="stackoverflow_tags.svg")
    posts = get_content(j)
    top_terms = get_top_terms(posts, k_per_doc=20, top_k=0, min_len=3)
    draw_words_freq(top_terms, topk=20, ylabel="keywords", out_fname="stackoverflow_keywords.svg")
    urls = get_urls(posts)
    draw_dataset_edp_cat(urls)
    cat_count = get_categories(urls)
    draw_count(cat_count, "stackoverflow_cat.svg")



# ids = get_ids_from_q_json(j)
    # j = get_questions_body(ids)
    # print(j)


if __name__ == "__main__":
    workflow()
