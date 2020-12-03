import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from .utils.error_messages import ErrorMessages
from .utils.mock_request import MockRequest
from .utils.mock_response import MockResponse

REQUEST_TYPE = "audience"
METHOD_CREATE = "create"
METHOD_DOWNLOAD = "download"
SCENARIO_POSITIVE = "positive"
SCENARIO_404 = "404"
SCENARIO_401 = "401"


def get_method_from_request(request_data):
    url = request_data.get("url", "")
    if url.endswith("create/"):
        return METHOD_CREATE
    else:
        return METHOD_DOWNLOAD


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(
            REQUEST_TYPE,
            method=get_method_from_request(kwargs),
            test_scenario=SCENARIO_POSITIVE,
            key_replace={"requestId": ("<requestId>", MockRequest.MOCK_REQUEST_ID)})

    monkeypatch.setattr(Session, "post", mock_post)
    monkeypatch.setattr(Session, "get", mock_post)


@pytest.fixture
def mock_404_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(
            REQUEST_TYPE,
            method=get_method_from_request(kwargs),
            test_scenario=SCENARIO_404,
            status_code=int(SCENARIO_404),
            key_replace={"requestId": ("<requestId>", MockRequest.MOCK_REQUEST_ID)})

    monkeypatch.setattr(Session, "get", mock_post)


@pytest.fixture
def mock_401_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(
            REQUEST_TYPE,
            method=get_method_from_request(kwargs),
            test_scenario=SCENARIO_401,
            status_code=int(SCENARIO_401),
            message_replace=("<api_key>", MockRequest.MOCK_TOKEN))

    monkeypatch.setattr(Session, "post", mock_post)
    monkeypatch.setattr(Session, "get", mock_post)


########################################################################################################################


class TestAudienceApi(object):

    def setup(self):
        self.fullcontact_client = FullContactClient(MockRequest.MOCK_TOKEN)

    # Empty query provided
    @pytest.mark.parametrize("function_name, expected_exception, expected_error_message", [
        (METHOD_CREATE, TypeError, ErrorMessages.AUDIENCE_CREATE_MISSING_ARGUMENT),
        (METHOD_DOWNLOAD, TypeError, ErrorMessages.AUDIENCE_DOWNLOAD_MISSING_ARGUMENT)
    ])
    def test_empty_query(self, function_name, expected_exception, expected_error_message):
        with pytest.raises(expected_exception) as fc_exception:
            getattr(self.fullcontact_client.audience, function_name)()

        assert str(fc_exception.value).startswith(expected_error_message)

    @pytest.mark.parametrize("method", [METHOD_CREATE, METHOD_DOWNLOAD])
    def test_good_requests(self, mock_good_response, method):
        queries = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        if type(queries) is not list:
            queries = [queries]
        for query in queries:
            expected_result = MockResponse.get_mock_response(
                REQUEST_TYPE, method, SCENARIO_POSITIVE,
                key_replace={"requestId": ("<requestId>", MockRequest.MOCK_REQUEST_ID)})
            if "requestId" in query:
                query["requestId"] = MockRequest.MOCK_REQUEST_ID
            result = getattr(self.fullcontact_client.audience, method)(**query)
            assert result.is_successful and \
                   result.get_status_code() == expected_result.status_code

    # Parsing 404 response
    def test_404_requests(self, mock_good_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_DOWNLOAD, SCENARIO_POSITIVE)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, METHOD_DOWNLOAD, SCENARIO_404,
            key_replace={"requestId": ("<requestId>", MockRequest.MOCK_REQUEST_ID)})
        if "requestId" in query:
            query["requestId"] = MockRequest.MOCK_REQUEST_ID
        result = self.fullcontact_client.audience.download(**query)
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code

    # Parsing 401 response
    @pytest.mark.parametrize("method", [METHOD_CREATE, METHOD_DOWNLOAD])
    def test_401_requests(self, mock_401_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        if type(query) is list:
            query = query[0]
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method, SCENARIO_401, int(SCENARIO_401),
            message_replace=("<api_key>", MockRequest.MOCK_TOKEN))

        if "requestId" in query:
            query["requestId"] = MockRequest.MOCK_REQUEST_ID
        result = getattr(self.fullcontact_client.audience, method)(**query)
        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")
