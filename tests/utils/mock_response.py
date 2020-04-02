from .mock_request import MockRequest
from ..resources import get_resource_json


class MockResponse(object):
    def __init__(self, type, method, test_scenario, status_code, message_replace=None):
        self.type = type
        self.method = method
        self.test_scenario = test_scenario
        self.status_code = status_code
        self.headers = {}
        self.__jsondata = get_resource_json("response", type, method, test_scenario)
        if message_replace is not None:
            self._set_message(message_replace)

    def json(self):
        return self.__jsondata

    def _set_message(self, message_replace):
        if self.__jsondata.get("message", None) is not None:
            self.__jsondata["message"] = self.__jsondata["message"].replace(*message_replace)

    @property
    def success(self):
        if int(self.status_code / 100) == 2:
            return True
        return False

    @property
    def reason(self):
        if self.json().get("message", None) is not None:
            return self.json().get("message")
        elif self.success:
            return "OK"
        else:
            return "Failed"

    @staticmethod
    def get_mock_response(type, method, test_scenario, status_code=200, message_replace=None):
        return MockResponse(type, method, test_scenario, status_code, message_replace)
