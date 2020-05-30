from ..resources import get_resource_json


class MockResponse(object):
    def __init__(self, type, method, test_scenario, status_code, message_replace=None, key_replace=None):
        self.type = type
        self.method = method
        self.test_scenario = test_scenario
        self.status_code = status_code
        self.headers = {}
        self.__jsondata = get_resource_json("response", type, method, test_scenario)
        if message_replace is not None:
            self._set_message(message_replace)

        if key_replace is not None:
            self._set_key(key_replace)

    def json(self):
        return self.__jsondata

    def _set_message(self, message_replace):
        self._set_key({"message": message_replace})

    def _set_key(self, replace_items):
        for k, v in replace_items.items():
            if self.__jsondata.get(k, None) is not None:
                if type(self.__jsondata[k]) == list:
                    self.__jsondata[k][0] = self.__jsondata[k][0].replace(*v)
                else:
                    self.__jsondata[k] = self.__jsondata[k].replace(*v)

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
    def get_mock_response(type, method, test_scenario, status_code=200, message_replace=None, key_replace=None):
        return MockResponse(type, method, test_scenario, status_code, message_replace, key_replace)
