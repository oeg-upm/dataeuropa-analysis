import json
import pickle
from analysis.util import parse
from analysis.wordcloud import plot_wordcloud_github
from analysis.classify import classify_nlp4types
from analysis.word import draw_words_freq
import requests
import os
import time
from nltk.corpus import stopwords
import sys

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
edp_search_query = "data.europa.eu"
github_token = "YOUR_GITHUB_TOKEN"
github_targets = {'code': ['repository', 'description'], 'repositories': ['description'],
                  'commits': ['repository', 'description'], 'issues': ['body'], 'topics': []}


# Targets=code, repositories, commits, issues, topics


def get_from_github(github_token, target, search_query, page=1):
    code = 200
    content = True
    while code == 200 and content:
        base_json_path = os.path.join(ROOT_DIR, 'data', 'github', "part_" + target + '_' + str(page) + ".json")
        url = "https://api.github.com/search/%s?q=%s&page=%s" % (target, search_query, str(page))
        print("request url: %s" % url)
        r = requests.get(url, headers={'Accept': 'application/vnd.github+json',
                                       'Authorization': 'token ' + github_token})
        code = r.status_code
        if code == 200:
            if not json.loads(r.text)['items']:
                content = False
            else:
                with open(base_json_path, 'w') as f:
                    f.write(r.text)
        time.sleep(5)
        page += 1



def get_items_json(target, keys,subtype=''):
    content = {}
    page=1
    if os.path.exists(os.path.join(ROOT_DIR, 'data', 'github', target + '.pkl')):
        with open(os.path.join(ROOT_DIR, 'data', 'github', target + '.pkl'), 'rb') as handle:
            content = pickle.load(handle)
    for f in os.listdir(os.path.join(ROOT_DIR, 'data', 'github')):
        if 'part' in f and target in f:
            json_file = json.load(open(os.path.join(ROOT_DIR, 'data', 'github', f)))
            new_page=int(os.path.join(ROOT_DIR, 'data', 'github', f).split('_')[-1].strip('.json'))
            if new_page > page:
                page = new_page
            for p in json_file['items']:
                if target == 'code':
                    content[p['repository']['name']] = p[keys[0]][
                        keys[1]]  # how to make this adaptable to all file types?
                elif target == 'commits':
                    content[p['repository']['name']] = p[keys[0]][
                        keys[1]]  # how to make this adaptable to all file types?
                elif target == 'issues':
                    content[p['body']] = p[keys[0]]  # how to make this adaptable to all file types?
                elif target == 'repositories':
                    content[p['name']] = p[keys[0]]  # how to make this adaptable to all file types?
            os.remove(os.path.join(ROOT_DIR, 'data', 'github', f))
    content['last_gh_page_'+subtype]=page
    with open(os.path.join(ROOT_DIR, 'data', 'github', target + '.pkl'), 'wb') as handle:
        pickle.dump(content, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return content


def analyze_content(target):
    with open(os.path.join(ROOT_DIR, 'data', 'github', target + '.pkl'), 'rb') as handle:
        content = pickle.load(handle)
    # Remove None values
    tokens = []
    for k, v in content.items():
        if k is not None:
            if 'last_gh_page' in k:
                continue
            if v is None:
                v = ''
            # Analyze both name of repo and description
            text = k + ' ' + v
            text = text.replace('_', ' ')
            for t in text.split(' '):
                for token in parse(t):
                    token = token.strip()
                    tokens.append(token)
    # Clean tokens
    stop_words = set(stopwords.words('english'))
    clean_tokens = []
    for t in tokens:
        if not any(not c.isalnum() for c in t) and t not in stop_words:
            clean_tokens.append(t)
    return clean_tokens


def plot_tokens(target, tokens):
    plot_wordcloud_github(target, tokens, outFname=os.path.join(ROOT_DIR,"github_" + target + ".svg"))


def plot_types(target, content):
    types = []
    for k, v in content.items():
        if v is not None and 'last_gh_page' not in k:
            t = classify_nlp4types(v)
            types.append(t)
    draw_words_freq(types, 100, palette="mako", out_fname=os.path.join(ROOT_DIR,"github_" + target + "_class.svg"))


def workflow(target):
    if not os.path.exists(os.path.join(ROOT_DIR,'data', 'github', target+".pkl")):
        page_general=1
        page_datastories=1
        page_datasets=1
    else:
        with open(os.path.join(ROOT_DIR, 'data', 'github', target + '.pkl'), 'rb') as handle:
            content = pickle.load(handle)
        if 'last_gh_page_' in list(content.keys()):
            page_general=content['last_gh_page_']
            page_datastories=content['last_gh_page_datastories']
            page_datasets = content['last_gh_page_datasets']
        else:
            page_general = 1
            page_datastories = 1
            page_datasets = 1
    print("Fetching data from GitHub ...")
    get_from_github(github_token, target, edp_search_query,page=page_general)
    content = get_items_json(target, github_targets[target])
    get_from_github(github_token,target,edp_search_query+'+datastories',page=page_datastories)
    content = get_items_json(target, github_targets[target],'datastories')
    get_from_github(github_token, target, edp_search_query + '+datasets', page=page_datasets)
    content = get_items_json(target, github_targets[target], 'datasets')

    tokens = analyze_content(target)
    plot_types(target, content)
    plot_tokens(target, tokens)


if __name__ == "__main__":
    target = sys.argv[1]
    workflow(target)
