import hashlib
import json
import os
import requests
from .util import parse

base_uri = "https://data.europa.eu/api/hub/search/datasets/"


# "s2115_85_3_449_eng"


def get_dataset(dataset_name, cache):
    hash_object = hashlib.md5(dataset_name.encode('utf-8'))
    digest = hash_object.hexdigest()
    hash_path = os.path.join(cache, digest)
    if cache != "" and os.path.exists(hash_path):
        with open(hash_path) as f:
            j = json.load(f)
    else:
        url = base_uri+dataset_name
        print("calling: %s" % url)
        response = requests.get(url)
        j = response.json()
        if cache != "":
            with open(hash_path, 'w') as f:
                json.dump(j, f)
    return j


def get_categories(j):
    categories = []
    for cat in j['result']['categories']:
        categories.append(cat['label']['en'])
    return categories


def get_redirect_url(url):
    response = requests.get(url)
    new_url = response.url
    # print("redirect: \n%s to \n%s" % (url, new_url))
    return new_url


def cat_from_url(url):
    toks = parse(url, seps=[']', '[', '(', ')', ','])
    url = toks[0]
    url = get_redirect_url(url)
    dataset_name = url.split('/')[-1].split("?")[0]
    cache_path = os.path.join("data", "data-europa")
    # print("cache path: %s" % cache_path)
    j = get_dataset(dataset_name, cache_path)
    return get_categories(j)

