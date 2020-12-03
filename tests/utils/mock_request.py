from ..resources import get_resource_json
from enum import Enum


class MockRequest(object):
    MOCK_TOKEN = "dummy70k3nT0Mock"
    MOCK_RECORD_ID = "dummyR3c0rd1d70Mock"
    MOCK_PERSON_ID = "dummyP3r50n1d70Mock"
    MOCK_PARTNER_ID = "dummyP4r7n3r1d70Mock"
    MOCK_REQUEST_ID = "dummy-R3qu-3571d-70Mock"

    @staticmethod
    def get_mock_request(type, method, test_scenario):
        return get_resource_json("request", type, method, test_scenario)