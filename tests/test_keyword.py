import unittest
from nltk.tokenize import word_tokenize
from analysis.keyword import tf_idf, tf_tokens, idf_docs, preprocess


class KeywordTest(unittest.TestCase):

    def setUp(self) -> None:
        self.texts = [
            "Spain Hello abc sample abc",
            "spain Hello another another example example example"
        ]
        self.tokens_coll = []
        for t in self.texts:
            tokens = word_tokenize(t)
            tokens = preprocess(tokens, remove_stop_words=False)
            self.tokens_coll.append(tokens)

    def test_prep(self):
        texts = [
            "This is a sample a",
            "This is another another example example example"
        ]
        t = texts[0]
        tokens = word_tokenize(t)
        tokens = preprocess(tokens)
        self.assertEqual(len(tokens), 1)
        t = texts[1]
        tokens = word_tokenize(t)
        tokens = preprocess(tokens)
        self.assertEqual(len(tokens), 5)

    def test_tf(self):
        texts = [
            "This is a sample a",
            "This is another another example example example"
        ]
        t = texts[0]
        tokens = word_tokenize(t)
        tokens = preprocess(tokens, remove_stop_words=False)
        tf_0 = tf_tokens(tokens)
        self.assertEqual(tf_0['this'], 0.2)
        t = texts[1]
        tokens = word_tokenize(t)
        tokens = preprocess(tokens, remove_stop_words=False)
        tf_1 = tf_tokens(tokens)
        self.assertEqual(tf_1['this'], 1/7)

    def test_idf(self):
        docs_per_term = dict()
        for i, tokens in enumerate(self.tokens_coll):

            for t in set(tokens):
                if t not in docs_per_term:
                    docs_per_term[t] = []
                docs_per_term[t].append(i)

        terms_idf = idf_docs(docs_per_term, len(self.tokens_coll))
        self.assertEqual(round(terms_idf["example"], 3), 0.301)

    def test_tfidf(self):
        tf_idf_dict = tf_idf(self.texts)
        # print(tf_idf_dict)
        # self.assertEqual(tf_idf_dict[0]["example"], 0)
        self.assertEqual(round(tf_idf_dict[1]["example"], 3), 0.129)

