import math
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import Counter
from .util import parse

# nltk.download('wordnet')
# nltk.download('omw-1.4')


def preprocess(tokens, lang='english', lemm=True, lower=True, remove_stop_words=True):
    if lower:
        tokens = [t.lower() for t in tokens]
    if lemm:
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(t) for t in tokens]
    if remove_stop_words:
        lang_stop_words = stopwords.words(lang)
        tokens = [t for t in tokens if t not in lang_stop_words]
    return tokens


# def tf(text):
#     # words = parse(text)
#     words = word_tokenize(text)
#     return Counter(words)

def tf_tokens(tokens):
    tf = dict()
    c = Counter(tokens)
    for k in c:
        tf[k] = c[k]/len(tokens)
    # print("tf_tokens> ")
    # print(tf)
    return tf


def tf_idf(texts):
    docs_tf = dict()
    docs_per_term = dict()
    for i, t in enumerate(texts):
        tokens = word_tokenize(t)
        tokens = preprocess(tokens)
        docs_tf[i] = tf_tokens(tokens)

        for t in set(tokens):
            if t not in docs_per_term:
                docs_per_term[t] = []
            docs_per_term[t].append(i)

    terms_idf = idf_docs(docs_per_term, len(texts))
    # print("\nterms idf: ")
    # print(terms_idf)
    #
    # print("\ntf: ")
    # print(docs_tf)
    # print("=========")

    tf_idf_dict = dict()
    for doc_id in docs_tf:
        tf_idf_dict[doc_id] = dict()
        for term in docs_tf[doc_id]:
            tf_idf_dict[doc_id][term] = docs_tf[doc_id][term] * terms_idf[term]
    return tf_idf_dict


def idf_docs(docs_per_term, N):
    idf_dict = dict()
    for term in docs_per_term:
        if term in idf_dict:
            continue
        idf_dict[term] = math.log(N/len(docs_per_term[term]), 10)
    return idf_dict
