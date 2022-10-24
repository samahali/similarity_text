from django.test import TestCase

from django.urls import reverse
from pathlib import Path

from utility import read_single_col_in_dataset

file_path = Path(__file__).parent.parent.parent.resolve()
DUMMY_MEDICAL_CSV = f'{file_path}/utility/Dummy medical dataset.csv'


class TestIndexView(TestCase):
    """ index view functionality"""

    def setUp(self) -> None:
        self.url = reverse("text_matching:index")
        self.keys = read_single_col_in_dataset('Key', DUMMY_MEDICAL_CSV)

    def test_not_allowed_request_method(self):
        """Test not allowed methods, accepted method GET"""
        not_allowed_status_code = 405
        patch_response = self.client.patch(self.url)
        self.assertEqual(patch_response.status_code, not_allowed_status_code)
        post_response = self.client.post(self.url)
        self.assertEqual(post_response.status_code, not_allowed_status_code)
        put_response = self.client.put(self.url)
        self.assertEqual(put_response.status_code, not_allowed_status_code)
        delete_response = self.client.delete(self.url)
        self.assertEqual(
            delete_response.status_code, not_allowed_status_code
        )

    def test_index(self):
        """ test success scenario for calling index """
        get_response = self.client.get(self.url)
        success_status_code = 200
        self.assertEqual(get_response.status_code, success_status_code)
        self.assertIsNotNone(get_response.context)
        self.assertEqual(len(get_response.context[0].get('keys')), len(self.keys))
        self.assertEqual(get_response.context[0].get('keys'), self.keys)

    def test_many_request_index(self):
        """ test many request scenario for calling index """
        counter = 0
        for i in range(10):
            counter += 1
            post_response = self.client.get(self.url)
            success_status_code = 200
            self.assertEqual(post_response.status_code, success_status_code)
            self.assertIsNotNone(post_response.context)
            if counter == 6:
                self.assertIsNotNone(post_response.context[0].template_name, 'text_matching/error_429.html')
                break
