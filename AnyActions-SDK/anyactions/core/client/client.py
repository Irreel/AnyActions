import requests
from anyactions.common.exception.anyactions_exceptions import AWSGatewayException
from anyactions.core.client.request_status import RequestStatus

class Client:
    """
    Client to interact with the AnyActions API, deployed on AWS API Gateway.
    """
    def __init__(self, base_url: str, api_key: str):
        """
        Constructor for the Client class.

        :param base_url: The base URL of the API.
        :param api_key: The API key to authenticate the client.
        """
        self.base_url = base_url
        self.api_key = api_key
    

    def get(self, path: str, query: dict = None) -> tuple[RequestStatus, dict|None]:
        """
        Send a GET request to the API.

        :param path: The path of the API endpoint.
        :param query: The query to send with the request.
        :return: The response from the API, or None if the request failed.
        """
        response = requests.get(self.get_url(path), headers=self.get_headers(), json=query)
        status = RequestStatus.from_http_status(response.status_code)
        if status == RequestStatus.OK:
            return (status, self.get_response_body(response))
        else:
            return (status, None)

    def post(self, path: str, data: dict) -> RequestStatus:
        """
        Send a POST request to the API.

        :param path: The path of the API endpoint.
        :param data: The data to send with the request.
        :return: The status of the request.
        """
        response = requests.post(self.get_url(path), headers=self.get_headers(), json=data)
        return RequestStatus.from_http_status(response.status_code)
    
    def get_headers(self) -> dict:
        return {
            "x-api-key": self.api_key
        }
    
    def get_url(self, path: str) -> str:
        return f"{self.base_url}/{path}"
    
    def get_response_body(self, response: requests.Response):
        return response.json() if response.headers["Content-Type"] == "application/json" else response.text
    
    def get_response_status(self, response: requests.Response) -> RequestStatus:
        return RequestStatus.from_http_status(response)
    
    def download(self, action_name: str):
        """
        Download the tool definition and function body for a given action name.

        :param action_name: The name of the action to download.
        :return: A tuple containing the instruction, tool definition, and function body.
        """
        status, response = self.get("download", {"action_name": action_name})
        if status == RequestStatus.OK:
            return (status, self.get_action_spec(response))
        else:
            return (status, None)

    def get_action_spec(self, response: dict):        
        if response["message"] == "Files retrieved successfully":
            instruction = response["files"]["registration_link"]
            tool_def = response["files"]["tool_definition.json"]
            func_body = response["files"]["tools.py"]
            return (instruction, tool_def, func_body)
        else:
            return RequestStatus.INTERNAL_SERVER_ERROR