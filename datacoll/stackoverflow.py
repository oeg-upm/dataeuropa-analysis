import requests
import os
import json
from analysis.word import draw_words_freq


def get_questions_json():
    json_path = os.path.join('data', 'stackoverflow', 'questions.json')
    if os.path.exists(json_path):
        print("Json already exists: %s" % json_path)
    else:
        body_query = "data.europa.eu"
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


def get_content(j):
    posts = []
    for p in j['items']:
        posts.append(p["body_markdown"])


def get_keywords(body):
    keywords = []
    tokens = body.replace("\n", " ").replace("\t", " ").split(" ")
    for token in tokens:
        t = token.strip().lower()


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


def workflow():
    j = get_questions_json()
    tags = get_tags(j)
    # draw_words_freq(tags, topk=10)
    draw_words_freq(tags, topk=10, out_fname="stackoverflow.svg")

# ids = get_ids_from_q_json(j)
    # j = get_questions_body(ids)
    # print(j)


if __name__ == "__main__":
    workflow()