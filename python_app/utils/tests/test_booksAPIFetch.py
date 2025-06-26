import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory of the project (python_app) to sys.path for absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.booksAPIFetch import fetch_openlibrary_data


class TestFetchOpenLibraryData(unittest.TestCase):
    @patch('utils.booksAPIFetch.requests.get')
    def test_fetch_openlibrary_data_success(self, mock_get):
        # Mock a successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "numFound": 1,
            "docs": [
                {
                    "title": "Test Book",
                    "author_name": ["Test Author"],
                    "first_publish_year": 2000,
                    "isbn": ["1234567890"],
                    "key": "/books/OL1234567M"
                }
            ]
        }
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_openlibrary_data("Test Book")

        # Assertions
        self.assertEqual(result, {
            "Title": "Test Book",
            "Author": "Test Author",
            "First_Publish_Year": 2000,
            "ISBN": "1234567890",
            "OpenLibrary_ID": "/books/OL1234567M"
        })
        mock_get.assert_called_once_with("https://openlibrary.org/search.json?title=Test Book")

    @patch('utils.booksAPIFetch.requests.get')
    def test_fetch_openlibrary_data_no_results(self, mock_get):
        # Mock an API response with no results
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "numFound": 0,
            "docs": []
        }
        mock_get.return_value = mock_response

        # Call the function
        result = fetch_openlibrary_data("Nonexistent Book")

        # Assertions
        self.assertIsNone(result)
        mock_get.assert_called_once_with("https://openlibrary.org/search.json?title=Nonexistent Book")

    @patch('utils.booksAPIFetch.requests.get')
    def test_fetch_openlibrary_data_error_handling(self, mock_get):
        # Mock an exception during the API call
        mock_get.side_effect = Exception("API error")

        # Call the function
        result = fetch_openlibrary_data("Error Book")

        # Assertions
        self.assertIsNone(result)
        mock_get.assert_called_once_with("https://openlibrary.org/search.json?title=Error Book")


if __name__ == '__main__':
    unittest.main()