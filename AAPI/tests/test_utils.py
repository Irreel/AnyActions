import unittest
from aapi.utils import create_inter_api_key


class TestUtils(unittest.TestCase):
    def test_create_inter_api_key_success(self):
        legal_api_name = 'GOOGLE_SEARCH'
        api_file_path = './test_api_key_file'
        user = {}
        status, inter_api_key = create_inter_api_key(legal_api_name, api_file_path, user)
        self.assertTrue(status)
        self.assertIsInstance(inter_api_key, str)
    def test_create_inter_api_key_invalid_name(self):
        legal_api_name = 'INVALID_NAME'
        api_file_path = './test_api_key_file'
        user = {}
        status, inter_api_key = create_inter_api_key(legal_api_name, api_file_path, user)
        self.assertFalse(status)
        self.assertIsNone(inter_api_key)
if __name__ == '__main__':
    unittest.main()