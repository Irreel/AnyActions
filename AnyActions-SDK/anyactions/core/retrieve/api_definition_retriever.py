from anyactions.core.client.client import Client
from anyactions.core.client.request_status import RequestStatus
from anyactions.common.protocol.protocols import GetApiByProviderActionRequestBuilder

class Retriever:
    """
    Interact with the API to retrieve the API definition
    """
    def __init__(self, client: Client):
        self.client = client
    
    def retrieve_api_definition(self, action: str) -> dict:
        """
        Retrieve the API definition for a given action.

        :param action: The action to retrieve the API definition for.
        :return: The API definition.
        """
        status, response = self.client.get("download", params=self.get_request(action))
        if (status == RequestStatus.OK):
            return response
        elif (status == RequestStatus.NOT_FOUND):
            #TODO: Fall back to generating with LLM
            raise NotImplementedError
        else:
            return None

    
    def get_request(self, action: str) -> dict:
        builder = GetApiByProviderActionRequestBuilder()
        builder.set_action(action)
        return builder.get()