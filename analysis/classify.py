import os.path

import requests
import hashlib
import json
from .util import shorten_url


def classify_nlp4types(text, cache=""):
    hash_object = hashlib.md5(text.encode('utf-8'))
    digest = hash_object.hexdigest()
    hash_path = os.path.join(cache, digest)
    if cache != "" and os.path.exists(hash_path):
        with open(hash_path) as f:
            j = json.load(f)
    else:
        url = "http://nlp4types.linkeddata.es/process"
        response = requests.post(url, data={'description': text})
        j = response.json()
        if cache != "":
            with open(hash_path, 'w') as f:
                json.dump(j, f)
    shortened = shorten_url(j['predictions'][1:-1])
    return shortened
