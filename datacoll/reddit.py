import requests
import os
import json
from analysis.util import ppretty, parse, categorize_edp_url
from analysis.category import draw_cat_per_sub
from collections import Counter

edp_search_query = "data.europa.eu"


def search_subreddit(subreddit, search_query):
    json_path = os.path.join('data', 'reddit', subreddit+".json")
    if os.path.exists(json_path):
        print("Ignore search. %s already exists" % json_path)
    else:
        url = "https://www.reddit.com/r/%s/search.json?q=%s&limit=100" % (subreddit, search_query)
        print("request url: %s" % url)
        # r = requests.get(url)
        # Just to get ride of the the error Too many requests
        r = requests.get(url, headers={'User-agent': 'your bot 0.1'})
        with open(json_path, 'w') as f:
            f.write(r.text)
    with open(json_path) as f:
        j = json.load(f)
    return j


def url_from_text(text):
    urls = []
    for t in text.split(' '):
        for token in parse(t, seps=["\n", "\r"]):
            token = token.strip()
            if token == "":
                continue
            if edp_search_query not in token:
                continue
            cleaned_token = ""
            # skip if the start of the toke is not h for http or d for data
            for i in range(len(token)):
                if token[i:i+4] in ["http"]:
                    cleaned_token = token[i:]
                    break
            if cleaned_token != "":
                urls.append(cleaned_token)
    return urls


def get_urls(j):
    urls = []
    # print("get urls: ")
    # print(j)
    for post in j['data']['children']:
        if post['kind'] == "t3":
            url = post['data']['url']
            if edp_search_query not in url:
                url_list = url_from_text(post['data']['selftext'])
                if len(url_list) > 0:
                    # print("list: %s" % str(url_list))
                    urls += url_list
            else:
                urls.append(url)
            # print(urls[-1])
        else:
            ppretty(post)

    return urls


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
        old_u = u
        u = u.split("[")[0]
        u = u.split("]")[0]
        u = u.split(",")[0]
        u = u.split(")")[0]
        u = u.split('"')[0]
        c_urls.append(u)
        # Just to verify clean up
        # if u != old_u:
        #     print("old: <%s>" % old_u)
        #     print("new: <%s>" % u)
    return c_urls


def search_subs():
    search_query = "data.europa.eu"
    d = dict()
    subs = ["europe", "datasets", "EuroStatistics"]
    # Because we reached Too Many Requests error.
    # subs = ["europe"]
    # subs = ["EuroStatistics"]
    for sub in subs:
        print("\n\nsubreddit: %s\n============" % sub)
        j = search_subreddit(sub, search_query)
        urls = get_urls(j)
        print(urls)
        urls = force_https(urls)
        urls = clean_urls(urls)
        # for u in urls:
        #     print(u)
        d[sub] = {'urls': urls}
    return d


def categorize_urls(urls):
    cats = [categorize_edp_url(u) for u in urls]
    return dict(Counter(cats))


def add_category(d):
    for sub in d:
        d[sub]['categories'] = categorize_urls(d[sub]['urls'])
        print("sub: %s" % sub)
        print(d[sub]['categories'])
    return d


def workflow():
    d = search_subs()
    d = add_category(d)
    draw_cat_per_sub(d, "reddit.svg")
    # print(d)


if __name__ == "__main__":
    workflow()
