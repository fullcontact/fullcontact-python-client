from ..resources import get_resource_json


class MockRequest(object):
    MOCK_TOKEN = "dummy70k3nT0Mock"

    @staticmethod
    def get_mock_request(type, method, test_scenario):
        return get_resource_json("request", type, method, test_scenario)