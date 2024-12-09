# Get Started

Generate API description from existingyaml file
```bash
python genAPIDscp.py
```

Exploration on generating API yaml from wild search is at `genAPIByByob.ipynb`

# Explained

For openapi.yaml, it has explicit information about operationId, which is the name of the API endpoint. Use the function `endpoint_from_openapi_yaml` to extract these information.

For swagger.yaml, the name of the API endpoint is inconsistent. It is recommended to convert swagger to openapi format first, and then use the function endpoint_from_openapi_yaml to extract the API information.

Reference:
https://cookbook.openai.com/examples/third_party/web_search_with_google_api_bring_your_own_browser_tool
https://github.com/openai/openai-cookbook/blob/main/examples/third_party/Web_search_with_google_api_bring_your_own_browser_tool.ipynb


# Upload to AWS Lambda Layer

Openai Lambda Layer not support python 3.11 yet.
```bash
# For macOS
brew install python@3.10
```

Create new venv
```bash
python3.10 -m venv create_layer
source create_layer/bin/activate
pip install -r requirements.txt
```

<!-- ```bash
pip install \
--platform manylinux2014_aarch64 \
--target=package \
--implementation cp \
--python-version 3.11 \
--only-binary=:all: --upgrade \
-r requirements.txt
``` -->

Create zip file
```bash
rm layer_content.zip
sh package.sh
```
