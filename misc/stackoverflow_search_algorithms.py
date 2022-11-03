import requests
import os
import json
from datacoll.stackoverflow import get_content, get_urls
from collections import Counter
from analysis.word import draw_words_freq
from analysis.util import urls_from_text, categorize_edp_url
from analysis.scraptopic import cat_from_url
from analysis.category import draw_count
from analysis.keyword import get_top_terms

search_query = "data.europa.eu"


def get_questions_json1():
    json_path = os.path.join('misc', 'stack_overflow_questions1.json')
    if os.path.exists(json_path):
        print("Json already exists: %s" % json_path)
    else:
        body_query = search_query
        # body_query = "data.europa.eu"
        uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&body=%s&site=stackoverflow&filter=!nKzQUR30W7" % body_query
        # uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&body=%s&site=stackoverflow" % body_query
        # uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&q=%s&site=stackoverflow&filter=!nKzQUR30SM" % body_query
        r = requests.get(uri)
        with open(json_path, 'w') as f:
            f.write(r.text)
    with open(json_path) as f:
        j = json.load(f)
    return j


def get_questions_json2():
    json_path = os.path.join('misc', 'stack_overflow_questions2.json')
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


# def get_questions_json_algo1():
#     body_query = search_query
#     # body_query = "data.europa.eu"
#     uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&body=%s&site=stackoverflow" % body_query
#     # uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&q=%s&site=stackoverflow&filter=!nKzQUR30SM" % body_query
#     r = requests.get(uri)
#     return r.json()
#
#
# def get_questions_json_algo2():
#     body_query = search_query
#     # body_query = "data.europa.eu"
#     # uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&body=%s&site=stackoverflow" % body_query
#     uri = "https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&q=%s&site=stackoverflow&filter=!nKzQUR30SM" % body_query
#     r = requests.get(uri)
#     return r.json()
#

def get_posts_ids(j):
    posts = []
    for p in j['items']:
        posts.append(p["question_id"])
    return posts


def workflow():
    j1 = get_questions_json1()
    j2 = get_questions_json2()
    posts1 = get_posts_ids(j1)
    posts2 = get_posts_ids(j2)
    s1 = set(posts1)
    s2 = set(posts2)

    bodies1 = get_content(j1)  # a list of the body of each post
    bodies2 = get_content(j2)
    urls1 = get_urls(bodies1)
    urls2 = get_urls(bodies2)

    print("S1 represents the results (posts) from algorithm 1 and S2 represent the posts resulted from algorithm 2")
    print("S1 has %d posts" % len(posts1))
    print("S2 has %d posts" % len(posts2))

    print("S1 has %d data europa links" % len(urls1))
    print("S2 has %d data europa links" % len(urls2))

    print("S1 - S2 = %d" % len(s1-s2))
    print("S2 - S1 = %d" % len(s2-s1))


workflow()