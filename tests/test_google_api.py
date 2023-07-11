import sys
from unittest import TestCase
from unittest.mock import patch, Mock

import requests

from ..google_api import utilities
from ..schemas import LookUpFilters


# sys.path.append("/..")

class TestBuildQuery(TestCase):
    def test_no_filters(self):
        filters = LookUpFilters(keyword=None, author=None, title=None, publisher=None, category=None)
        result = utilities.build_query(filters)

        self.assertEqual("", result)
    

    def test_title_author_filters(self):
        filters = LookUpFilters(keyword=None, author="King", title="it", publisher=None, category=None)
        result = utilities.build_query(filters)

        self.assertIn("inauthor:King", result)
        self.assertIn("intitle:it", result)
    
    def test_all_filters(self):
        filters = LookUpFilters(keyword="keyword", author="King", title="it", publisher="publisher", category="Horror")
        result = utilities.build_query(filters)

        self.assertIn("inauthor:King", result)
        self.assertIn("intitle:it", result)
        self.assertIn("keyword", result)
        self.assertIn("inpublisher:publisher", result)
        self.assertIn("subject:Horror", result)


class TestRetrieveBooks(TestCase):
    @patch("assessment_r5.google_api.utilities.requests")
    def test_return_raising_exception(self, requests_mock):
        filters = "inauthor:King"
        
        get_mock = Mock(status_code=requests.codes.not_found)
        requests_mock.codes.ok = 200
        requests_mock.get.return_value = get_mock
        
        with self.assertRaises(Exception):
            result = utilities.retrieve_books(filters)
    
    
    @patch("assessment_r5.google_api.utilities.requests")
    def test_return_ok(self, requests_mock):
        filters = "inauthor:King"
        expected_response = {"items": {"title": "It", "authors": ["Stephen King"]}}

        get_mock = Mock(status_code=requests.codes.ok)
        get_mock.json.return_value = expected_response
        requests_mock.codes.ok = 200
        requests_mock.get.return_value = get_mock

        result = utilities.retrieve_books(filters)
        self.assertEqual(expected_response["items"], result)
    






if __name__ == '__main__':
    unittest.main()