import unittest
from aapi.main import Hub
from unittest.mock import patch, mock_open

class TestHub(unittest.TestCase):
    @patch('aapi.main.os.path.exists')
    @patch('aapi.main.open', new_callable=mock_open, read_data="ACTION_TEST_API_KEY = 'test_key'\n")
    def test_verification_with_existing_key(self, mock_file, mock_exists):
        mock_exists.return_value = True
        hub = Hub(api_key='test_api_key')
        status, provider_name, action_name, inter_api_key = hub.verification('TEST_API')
        self.assertTrue(status)
        self.assertEqual(inter_api_key, 'test_key')
        
    @patch('aapi.main.os.path.exists')
    @patch('aapi.main.open', new_callable=mock_open)
    def test_verification_without_key(self, mock_file, mock_exists):
        mock_exists.return_value = False
        hub = Hub(api_key='test_api_key')
        status, provider_name, action_name, inter_api_key = hub.verification('TEST_API')
        self.assertFalse(status)
        self.assertIsNone(inter_api_key)

    def test_tools(self):
        hub = Hub(api_key='test_api_key')
        tool_list = ['google_search', 'wikipedia_search']
        result = hub.tools(tool_list)
        self.assertIsInstance(result, list)
        
        
if __name__ == '__main__':
    unittest.main()