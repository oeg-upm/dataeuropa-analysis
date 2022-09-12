import json


def ppretty(j):
    print(json.dumps(j, indent=4, sort_keys=True))


def parse(text, seps=[")", " ", "(", "[", "]", ",", "", "}", "{", "\n", ".", "\r"]):
    if len(seps) == 0:
        return [text]
    tokens = []
    for token in text.split(seps[0]):
        token = token.strip()
        if token == "":
            continue
        toks = parse(token, seps[1:])
        tokens += toks

    return tokens


def categorize_edp_url(url):
    if "/datastories" in url:
        return "Data Story"
    if "/eli/" in url:
        return "Legislation"
    if "/dataset" in url or '/data/' in url:
        return "Dataset"
    return "Other"
