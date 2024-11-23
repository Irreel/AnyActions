import os
import unittest
import tempfile
import shutil
import json
from pathlib import Path
from unittest import mock
from AAPI.aapi.utils import write_tool_to_local

class TestWriteToolToLocal(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to act as the api_dir_path
        # self.temp_dir = tempfile.mkdtemp()
        self.temp_dir = str(Path(__file__).parent / 'tmp')
        os.makedirs(self.temp_dir, exist_ok=True)

        # Sample tool definition
        self.tool_definition = {
            "type": "function",
            "function": {
                "name": "sample_tool",
                "description": "Sample tool function.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "param1": {
                            "type": "string",
                            "description": "The first parameter as a string."
                        },
                        "param2": {
                            "type": "integer",
                            "description": "The second parameter as an integer."
                        }
                    },
                    "required": ["param1", "param2"],
                    "additionalProperties": False
                }
            }
        }

        # Sample tool function as a string
        self.tool_func = (
            "def sample_tool(param1, param2, api_key=None):\n"
            "    \"\"\"\n"
            "    Sample tool function.\n"
            "    \"\"\"\n"
            "    return f\"Param1: {param1}, Param2: {param2}, API Key: {api_key}\""
        )

    def tearDown(self):
        # Remove the temporary directory after the test
        # shutil.rmtree(self.temp_dir)
        pass

    def test_write_tool_to_local_without_exec_sh(self):
        # Call the function without exec_sh
        write_tool_to_local(
            api_dir_path=self.temp_dir,
            tool_definition=self.tool_definition,
            tool_func=self.tool_func
        )

        # Path to the expected tool file
        expected_file = Path(self.temp_dir) / "sample_tool.py"
        
        # # Read and print the content of the created tool file
        # with expected_file.open('r', encoding='utf-8') as f:
        #     print(f.read())
        
        self.assertTrue(expected_file.exists(), "Tool file was not created.")

        # Read the content of the created tool file
        with expected_file.open('r', encoding='utf-8') as f:
            content = f.read()

        # Expected docstring
        expected_docstring = json.dumps(self.tool_definition, indent=4).replace('\n', '\n    ')

        # Check if the function definition is correct
        expected_function_def = "def sample_tool(param1, param2, api_key=None):\n"
        self.assertIn(expected_function_def, content, "Function definition is incorrect.")

        # Check if the docstring is correctly written
        self.assertIn('"""_tool_definition_', content, "Docstring start marker is missing.")
        self.assertIn(expected_docstring, content, "Docstring content is incorrect.")

        # Check if the function body is correctly written
        self.assertIn("return f\"Param1: {param1}, Param2: {param2}, API Key: {api_key}\"", content, "Function body is incorrect.")

    # @mock.patch('AAPI.aapi.utils.subprocess.run')
    # def test_write_tool_to_local_with_exec_sh(self, mock_subprocess_run):
    #     exec_sh = "echo 'Executing shell command'"
        
    #     # Call the function with exec_sh
    #     write_tool_to_local(
    #         api_dir_path=self.temp_dir,
    #         tool_definition=self.tool_definition,
    #         tool_func=self.tool_func,
    #         exec_sh=exec_sh
    #     )

    #     # Assert that subprocess.run was called with the correct command
    #     mock_subprocess_run.assert_called_with(exec_sh, shell=True, check=True)

    #     # Path to the expected tool file
    #     expected_file = Path(self.temp_dir) / "sample_tool.py"
    #     self.assertTrue(expected_file.exists(), "Tool file was not created.")

    # def test_write_tool_to_local_invalid_tool_definition(self):
    #     # Missing 'name' in tool_definition
    #     invalid_tool_definition = {
    #         "type": "function",
    #         "function": {
    #             "parameters": {
    #                 "type": "object",
    #                 "properties": {
    #                     "param1": {"type": "string"}
    #                 },
    #                 "required": ["param1"],
    #                 "additionalProperties": False
    #             }
    #         }
    #     }

    #     with self.assertRaises(KeyError):
    #         write_tool_to_local(
    #             api_dir_path=self.temp_dir,
    #             tool_definition=invalid_tool_definition,
    #             tool_func=self.tool_func
    #         )

    # def test_write_tool_to_local_invalid_tool_func(self):
    #     # Invalid tool_func (not a properly formatted string)
    #     invalid_tool_func = "def incomplete_function(param1, param2"

    #     with self.assertRaises(Exception) as context:
    #         write_tool_to_local(
    #             api_dir_path=self.temp_dir,
    #             tool_definition=self.tool_definition,
    #             tool_func=invalid_tool_func
    #         )
        
    #     self.assertIn("Failed to write tool to", str(context.exception))

if __name__ == '__main__':
    unittest.main()