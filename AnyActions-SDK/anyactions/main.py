import os
import json
from dotenv import load_dotenv
from anyactions.core.client import Client, RequestStatus

def setup():
    load_dotenv()

def load_data(json_file: str) -> dict:
    with open(json_file) as f:
        return json.load(f)

def test_get():
    client = Client(os.environ["AWS_GATEWAY_BASE_URL"], os.environ["AWS_GATEWAY_API_KEY"])
    status, response = client.get("download", load_data("test-files/test-retrieve-not-found.json"))
    assert status == RequestStatus.NOT_FOUND, f"Expected status NOT_FOUND, got {status}"
    status, response = client.get("download", load_data("test-files/test-retrieve-ok.json"))
    assert status == RequestStatus.OK, f"Expected status OK, got {status}"

# def test_save():
#     client = Client(os.environ["AWS_GATEWAY_BASE_URL"], os.environ["AWS_GATEWAY_API_KEY"])
#     status = client.post("upload", load_data("test-files/test-callback-ok-deprecated.json"))
#     assert status == RequestStatus.OK, f"Expected status OK, got {status}"
    
def test_callback():
    client = Client(os.environ["AWS_GATEWAY_BASE_URL"], os.environ["AWS_GATEWAY_API_KEY"])
    status = client.post("callback", load_data("test-files/test-callback-ok.json"))
    assert status == RequestStatus.OK, f"Expected status OK, got {status}"

def main():
    setup()
    test_get()
    # test_save()
    test_callback()

if __name__ == '__main__':
    main()