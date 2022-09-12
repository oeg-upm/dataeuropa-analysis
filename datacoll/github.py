import json
import pickle
from analysis.util import parse
from analysis.wordcloud import plot_wordcloud_github
import requests
import os
import time
from nltk.corpus import stopwords
import shutil
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
edp_search_query = "data.europa.eu"
github_token="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"
github_targets={'code':['repository','description'], 'repositories':['description'],
                    'commits':['repository','description'], 'issues':[], 'topics':[]}
#Targets=code, repositories, commits, issues, topics
def get_from_github(github_token,target,search_query):
    json_path = os.path.join(ROOT_DIR,'data', 'github', target + ".json")
    if os.path.exists(json_path):
        print("Ignore search. %s already exists" % json_path)
    else:
        #We need to attain partial results up until we get a 403
        #Code page 20
        page=21
        code=200
        while code==200:
            base_json_path = os.path.join(ROOT_DIR, 'data', 'github', "part_" + target +'_'+str(page) +".json")
            url = "https://api.github.com/search/%s?q=%s&page=%s" % (target, search_query,str(page))
            print("request url: %s" % url)
            r = requests.get(url, headers={'Accept': 'application/vnd.github+json', 'Authorization': 'token '+github_token})
            code=r.status_code
            if code==200:
                with open(base_json_path,'w') as f:
                    f.write(r.text)
            time.sleep(5)
            print('Reached page %d' %page)
            page += 1
    # with open(json_path,'w') as f:
    #     j = json.load(f)
    # return j

def get_items_json(target, keys):
    content={}
    for f in os.listdir(os.path.join(ROOT_DIR, 'data', 'github')):
        if 'part' in f and target in f:
            json_file=json.load(open(os.path.join(ROOT_DIR, 'data', 'github',f)))
            for p in json_file['items']:
                if target=='code':
                        content[p['repository']['name']]=p[keys[0]][keys[1]] #how to make this adaptable to all file types?
                elif target=='commits':
                        content[p['repository']['name']] = p[keys[0]][keys[1]]  # how to make this adaptable to all file types?
                elif target=='issues':
                        content[p['repository_url']] = p[keys[0]][keys[1]]  # how to make this adaptable to all file types?
                elif target=='repositories':
                        content[p['name']] = p[keys[0]]  # how to make this adaptable to all file types?
    return content

def analyze_content(target):
    with open(os.path.join(ROOT_DIR, 'data', 'github',target+'.pkl'),'rb') as handle:
        content=pickle.load(handle)
    #Remove None values
    tokens=[]
    for k,v in content.items():
        if v is None:
            v=''
        #Analyze both name of repo and description
        text=k+' '+v
        text=text.replace('_',' ')
        for t in text.split(' '):
            for token in parse(t):
                token = token.strip()
                tokens.append(token)
    #Clean tokens
    stop_words=set(stopwords.words('english'))
    clean_tokens=[]
    for t in tokens:
        if not any(not c.isalnum() for c in t) and t not in stop_words:
            clean_tokens.append(t)
    return clean_tokens


def plot_tokens(target,tokens):
    plot_wordcloud_github(target,tokens)

def workflow():
    for i in github_targets.keys():
        j=get_from_github(github_token,i,edp_search_query)
        content=get_items_json(j,github_targets[i])

if __name__ == "__main__":
    target='commits'
    #get_from_github(github_token,target,edp_search_query)
    content=get_items_json(target,github_targets[target])
    with open(os.path.join(ROOT_DIR, 'data', 'github',target+'.pkl'),'wb') as handle:
       pickle.dump(content,handle,protocol=pickle.HIGHEST_PROTOCOL)
    tokens=analyze_content(target)
    plot_tokens(target,tokens)
