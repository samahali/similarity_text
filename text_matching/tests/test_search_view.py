import json

from django.test import TestCase

from django.urls import reverse
from pathlib import Path

from utility import TextSimilarity, read_single_col_in_dataset

file_path = Path(__file__).parent.parent.parent.resolve()
DUMMY_MEDICAL_CSV = f'{file_path}/utility/Dummy medical dataset.csv'


class TestSearchView(TestCase):
    """ search view functionality"""

    def setUp(self) -> None:
        self.url = reverse("text_matching:search")
        self.values = read_single_col_in_dataset('Values', DUMMY_MEDICAL_CSV)
        self.keys = read_single_col_in_dataset('Key', DUMMY_MEDICAL_CSV)

    def test_not_allowed_request_method(self):
        """Test not allowed methods, accepted method POST"""
        not_allowed_status_code = 405
        patch_response = self.client.patch(self.url)
        self.assertEqual(patch_response.status_code, not_allowed_status_code)
        get_response = self.client.get(self.url)
        self.assertEqual(get_response.status_code, not_allowed_status_code)
        put_response = self.client.put(self.url)
        self.assertEqual(put_response.status_code, not_allowed_status_code)
        delete_response = self.client.delete(self.url)
        self.assertEqual(
            delete_response.status_code, not_allowed_status_code
        )

    def test_search(self):
        """ test search with the key has greater than 50 percentage of similarity"""
        for key in self.keys:
            values = TextSimilarity(key, 50).search_for_similarity(self.values)
            if values:
                post_response = self.client.post(self.url, {'key': key})
                success_status_code = 200
                self.assertEqual(post_response.status_code, success_status_code)
                self.assertIsNotNone(post_response.context)
                self.assertIsNotNone(post_response.context[0].template_name, 'text_matching/similarity_table.html')
                if post_response.context[0].get('key'):
                    self.assertEqual(post_response.context[0].get('key'), key)
                    self.assertEqual(len(post_response.context[0].get('matching_text', [])), len(values))
                    self.assertJSONEqual(
                        json.dumps(post_response.context[0].get('matching_text'), sort_keys=True),
                        json.dumps(values, sort_keys=True),
                    )
                    break

    def test_no_key_search(self):
        """ test no search key"""
        post_response = self.client.post(self.url, {'key': ''})
        self.assertEqual(post_response.status_code, 200)

    def test_no_similarity_matched_key_search(self):
        """ test no similarity found"""
        post_response = self.client.post(self.url, {'key': 'xyz'})
        self.assertEqual(post_response.status_code, 200)

    def test_many_request_search(self):
        """ test many request call of search endpoint"""
        counter = 0
        for key in self.keys:
            values = TextSimilarity(key, 50).search_for_similarity(self.values)

            if values:
                counter += 1
                post_response = self.client.post(self.url, {'key': key})
                success_status_code = 200
                self.assertEqual(post_response.status_code, success_status_code)
                self.assertIsNotNone(post_response.context)
                if counter == 6:
                    self.assertIsNotNone(post_response.context[0].template_name, 'text_matching/error_429.html')
                    break
