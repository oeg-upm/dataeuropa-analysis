from datacoll import stackoverflow
from analysis import util
from unittest import TestCase

class TestStackOverflow(TestCase):


    def test_workflow(self):
        """
        This is just to test if the workflow works without errors.
        :return:
        """
        j = stackoverflow.get_questions_json()
        stackoverflow.add_urls(j)
        stackoverflow.include_only_cats(j, [util.CATEGORY_DATASET, util.CATEGORY_DATA_STORY])
        posts = stackoverflow.get_posts(j)
        tags = stackoverflow.get_tags(j)
        top_terms = stackoverflow.get_top_terms(posts, k_per_doc=20, top_k=0, min_len=3)
        self.assertGreater(len(posts), 0)
        self.assertGreater(len(tags), 0)
