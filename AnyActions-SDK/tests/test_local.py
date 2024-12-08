import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import json
import shutil
from pathlib import Path
from anyactions import action
from anyactions.common.procedure.local import (
    get_tool_callable,
    write_local_tool,
    read_local_tool,
    check_local_tool_legit,
    get_local_tool_definition,
    get_local_api_key,
    read_tool_decorators,
    check_tool_decorator
)
# from anyactions.common.exception.anyactions_exceptions import LocalToolException

class TestLocal(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.observer = True
        self.api_dir_path = "./.actions"
        self.api_key_path = os.path.join(self.api_dir_path, ".api_key")
        self.tool_name = "test_tool"
        self.tool_path = os.path.join(self.api_dir_path, f"{self.tool_name}.py")
        
        # Create directory if it doesn't exist
        os.makedirs(self.api_dir_path, exist_ok=True)
        os.makedirs(os.path.dirname(self.api_key_path), exist_ok=True)
        
        # Sample tool definition and function
        self.tool_definition = {
            "type": "function",
            "function": {
                "name": "test_tool",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "q": {
                            "type": "string"
                        }
                    },
                    "required": ["q"],
                    "additionalProperties": False
                }
            }
        }
        
        self.tool_func = '''"""_tool_definition_
{
    "type": "function",
    "function": {
        "name": "test_tool",
        "parameters": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string"
                }
            },
            "required": ["q"],
            "additionalProperties": false
        }
    }
}
"""

from anyactions import action

@action
def test_tool(q: str, api_key: str):
    return {"query": q, "api_key": api_key}
'''
        # Write the test tool file
        with open(self.tool_path, 'w', encoding='utf-8') as f:
            f.write(self.tool_func)

    @action
    def tool_callable(self, q: str, api_key: str):
        return {"query": q, "api_key": api_key}
    
    def tearDown(self):
        # Clean up: remove the temporary directory and its contents
        if os.path.exists(self.api_dir_path):
            shutil.rmtree(self.api_dir_path)
        
    @patch('os.path.exists')
    def test_check_local_tool_legit_success(self, mock_exists):
        mock_exists.return_value = True
        
        with patch('anyactions.common.procedure.local.read_tool_definition') as mock_read_def:
            mock_read_def.return_value = {
                "function": {"name": "test_tool"}
            }
            
            result = check_local_tool_legit(self.api_dir_path, self.tool_name)
            self.assertTrue(result)

    @patch('os.path.exists')
    def test_check_local_tool_legit_missing_dir(self, mock_exists):
        mock_exists.return_value = False
        
        with self.assertRaises(AssertionError):
            check_local_tool_legit(self.api_dir_path, self.tool_name)

    @patch('builtins.open', new_callable=mock_open, read_data='test function content')
    def test_read_local_tool(self, mock_file):
        result = read_local_tool(self.api_dir_path, self.tool_name)
        self.assertEqual(result, 'test function content')
        mock_file.assert_called_once_with(self.tool_path, 'r', encoding='utf-8')

    def test_write_local_tool(self):
        tool_definition = {
            "name": "test_tool",
            "function": {
                "name": "test_tool"
            }
        }
        tool_func = "def test_tool():\n    pass"
        
        mock_open_obj = mock_open()
        with patch('builtins.open', mock_open_obj):
            write_local_tool(self.api_dir_path, tool_definition, tool_func)
            
        mock_open_obj.assert_called_once_with(self.tool_path, 'w', encoding='utf-8')
        mock_open_obj().write.assert_called_once_with(tool_func)

    @patch('os.path.exists')
    def test_get_local_api_key(self, mock_exists):
        mock_exists.return_value = True
        api_key = "test_api_key"
        
        with patch('builtins.open', mock_open(read_data=api_key)):
            result = get_local_api_key(self.api_dir_path, self.tool_name)
            self.assertEqual(result, api_key)

    @patch('importlib.util.spec_from_file_location')
    def test_get_tool_callable(self, mock_spec):
        mock_module = MagicMock()
        mock_spec.return_value.loader.exec_module = MagicMock()
        mock_spec.return_value.loader.exec_module.return_value = None
        mock_function = MagicMock()
        setattr(mock_module, self.tool_name, mock_function)
        
        with patch('importlib.util.module_from_spec', return_value=mock_module):
            result = get_tool_callable(self.tool_name, self.tool_path)
            self.assertEqual(result, mock_function)
            
    def test_read_tool_decorators(self):
        result = read_tool_decorators(self.api_dir_path, self.tool_name)
        self.assertEqual(result, ['action'])
        
    def test_check_tool_decorator(self):
        result = check_tool_decorator(self.tool_callable, 'action')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()