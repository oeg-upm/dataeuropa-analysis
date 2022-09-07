import json
import requests
import os
import time
from jsonmerge import merge
import shutil

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
edp_search_query = "data.europa.eu"
github_token="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"

#Targets=code, repositories, commits, issues, topics
def get_from_github(github_token,target,search_query):
    json_path = os.path.join(ROOT_DIR,'data', 'github', target + ".json")
    if os.path.exists(json_path):
        print("Ignore search. %s already exists" % json_path)
    else:
        #We need to attain partial results up until we get a 403
        page=9
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

def get_items_json(json_file, keys):
    content={}
    for p in json_file['items']:
        content[p['name']]=p[keys[0]][keys[1]] #how to make this adaptable to all file types?
    return content

def workflow():
    github_targets={'code':['repository','description'], 'repositories':[], 'commits':[], 'issues':[], 'topics':[]}
    for i in github_targets.keys():
        j=get_from_github(github_token,i,edp_search_query)
        content=get_items_json(j,github_targets[i])

if __name__ == "__main__":
    get_from_github(github_token,'code',edp_search_query)
