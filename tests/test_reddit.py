from datacoll import reddit
from analysis import util
from unittest import TestCase

class TestReddit(TestCase):

    def test_search_subreddit(self):
        """
        This only checks if the function returns some data.
        :return:
        """
        j = reddit.search_subreddit()
        keys = list(j.keys())
        self.assertGreater(len(keys), 0)

    def test_workflow(self):
        """
        This is just to test if the workflow works without errors.
        :return:
        """
        d = reddit.search_subreddit()
        d = reddit.split_into_subreddits(d)
        reddit.fetch_urls(d)
        d = reddit.add_category(d)
        reddit.remove_empty(d)
        reddit.only_include_cat(d, [util.CATEGORY_DATASET, util.CATEGORY_DATA_STORY])

        posts = reddit.get_posts(d)
        top_terms = reddit.get_top_terms(posts, k_per_doc=20, top_k=0, min_len=3)
        self.assertGreater(len(top_terms), 0)