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
        
    def test_process_func_str(self):
        tool_definition = """{
        "type": "function",
        "function": {"name": "test_func", "description": "test function", "parameters": {}},
        }"""
        func_str = 'def test_func(a, b):\n    return a + b'
        processed_str = process_func_str(tool_definition, func_str)
        # self.assertEqual(processed_str, '"""\ndef test_func(a, b):\n    return a + b\n"""\n\n@action\ndef test_func(a, b):\n    return a + b')
        print(processed_str)
    
if __name__ == '__main__':
    unittest.main()