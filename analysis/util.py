import json

CATEGORY_DATA_STORY = "Data Story"
CATEGORY_DATASET = "Dataset"

def ppretty(j):
    print(json.dumps(j, indent=4, sort_keys=True))




def parse(text, seps=[")", " ", "(", "[", "]", ",", "}", "{", "\n", ".", "\r"]):
    if len(seps) == 0:
        return [text]
    tokens = []
    for token in text.split(seps[0]):
        token = token.strip()
        if token == "":
            continue
        toks = parse(token, seps[1:])
        tokens += toks
    # print(f"text: {text}")
    # print(f"tokens: {tokens}")
    return tokens


def categorize_edp_url(url):
    if "/datastories" in url:
        return "Data Story"
    if "/eli/" in url:
        return "Legislation"
    if "/dataset" in url or '/data/' in url:
        return "Dataset"
    if "esco" in url:
        return "ESCO"
    return "Other"


def shorten_url(url):
    prefixes = [
        ["http://dbpedia.org/ontology/", "dbo:"],
    ]
    for p in prefixes:
        if url.startswith(p[0]):
            return url.replace(p[0], p[1])
    return url


def urls_from_text(text, search_query, seps=["\n", "\r"]):
    urls = []
    for t in text.split(' '):
        for token in parse(t, seps=seps):
            token = token.strip()
            if token == "":
                continue
            if search_query not in token:
                continue
            cleaned_token = ""
            # skip if the start of the toke is not h for http or d for data
            for i in range(len(token)):
                if token[i:i + 4] == "http":
                    cleaned_token = token[i:]
                    break
            if cleaned_token != "":
                if "](" in cleaned_token and cleaned_token[-1]==")":
                    # print(f"Extra split: {cleaned_token}")
                    cleaned_token = cleaned_token.split("](")[1][:-1]
                    # print(f"\t=> {cleaned_token}")
                elif cleaned_token.count(")") > cleaned_token.count("(") and cleaned_token[-1]==")":
                    # print(f"Remove extra ): %s" % cleaned_token)
                    cleaned_token = cleaned_token[:-1]
                urls.append(cleaned_token)
    return urls