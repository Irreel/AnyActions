from enum import Enum

class RequestStatus(Enum):
    OK = 1
    ERROR = 2
    TIMEOUT = 3
    NOT_FOUND = 4
    NOT_AUTHORIZED = 5
    FORBIDDEN = 6
    BAD_REQUEST = 7
    CONFLICT = 8
    UNPROCESSABLE_ENTITY = 9
    INTERNAL_SERVER_ERROR = 10
    SERVICE_UNAVAILABLE = 11
    GATEWAY_TIMEOUT = 12
    UNKNOWN = 13

    @staticmethod
    def from_http_status(http_status):
        if http_status == 200:
            return RequestStatus.OK
        elif http_status == 400:
            return RequestStatus.BAD_REQUEST
        elif http_status == 401:
            return RequestStatus.NOT_AUTHORIZED
        elif http_status == 403:
            return RequestStatus.FORBIDDEN
        elif http_status == 404:
            return RequestStatus.NOT_FOUND
        elif http_status == 409:
            return RequestStatus.CONFLICT
        elif http_status == 422:
            return RequestStatus.UNPROCESSABLE_ENTITY
        elif http_status == 500:
            return RequestStatus.INTERNAL_SERVER_ERROR
        elif http_status == 503:
            return RequestStatus.SERVICE_UNAVAILABLE
        elif http_status == 504:
            return RequestStatus.GATEWAY_TIMEOUT
        else:
            return RequestStatus.UNKNOWN