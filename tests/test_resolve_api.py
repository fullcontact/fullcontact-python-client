import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from fullcontact.exceptions import FullContactException
from .utils.error_messages import ErrorMessages
from .utils.mock_request import MockRequest
from .utils.mock_response import MockResponse

REQUEST_TYPE = "identity"
METHOD_MAP = "map"
METHOD_RESOLVE = "resolve"
METHOD_DELETE = "delete"
METHOD_MAP_RESOLVE = "mapResolve"
SCENARIO_POSITIVE = "positive"
SCENARIO_404 = "404"
SCENARIO_401 = "401"
SCENARIO_GOOD_NAME_BAD_LOCATION = "good_name_bad_location"
SCENARIO_GOOD_NAME_NO_LOCATION = "good_name_no_location"
SCENARIO_GOOD_NAME_NO_LOCATION_WITH_PLACEKEY = "good_name_no_location_with_placekey"
SCENARIO_GOOD_LOCATION_BAD_NAME = "good_location_bad_name"
SCENARIO_GOOD_LOCATION_NO_NAME = "good_location_no_name"
SCENARIO_FULL_SERIALIZATION = "full_serialization"


def get_method_from_request(request_data):
    url = request_data.get("url", "")
    if url.endswith("map/"):
        return METHOD_MAP
    elif url.endswith("mapResolve/"):
        return METHOD_MAP_RESOLVE
    elif url.endswith("resolve/"):
        return METHOD_RESOLVE
    else:
        return METHOD_DELETE


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(
            REQUEST_TYPE,
            method=get_method_from_request(kwargs),
            test_scenario=SCENARIO_POSITIVE,
            key_replace={"recordId": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personId": ("<personId>", MockRequest.MOCK_PERSON_ID),
                         "recordIds": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personIds": ("<personId>", MockRequest.MOCK_PERSON_ID)
                         }, )

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_404_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(
            REQUEST_TYPE,
            method=get_method_from_request(kwargs),
            test_scenario=SCENARIO_404,
            status_code=int(SCENARIO_404),
            key_replace={"recordId": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personId": ("<personId>", MockRequest.MOCK_PERSON_ID),
                         "recordIds": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personIds": ("<personId>", MockRequest.MOCK_PERSON_ID)
                         }, )

    monkeypatch.setattr(Session, "post", mock_post)


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


########################################################################################################################


class TestResolveApi(object):

    def setup(self):
        self.fullcontact_client = FullContactClient(MockRequest.MOCK_TOKEN)

    # Empty query provided
    @pytest.mark.parametrize("function_name, expected_exception, expected_error_message", [
        (METHOD_MAP, FullContactException, ErrorMessages.NO_QUERYABLE_INPUTS),
        (METHOD_RESOLVE, FullContactException, ErrorMessages.NO_QUERYABLE_INPUTS),
        (METHOD_DELETE, TypeError, ErrorMessages.IDENTITY_DELETE_MISSING_ARGUMENT)
    ])
    def test_empty_query(self, function_name, expected_exception, expected_error_message):
        with pytest.raises(expected_exception) as fc_exception:
            getattr(self.fullcontact_client.identity, function_name)()

        assert str(fc_exception.value).startswith(expected_error_message)

    # Invalid location-name combinations
    @pytest.mark.parametrize("method, scenario, expected_error", [
        (METHOD_MAP, SCENARIO_GOOD_LOCATION_BAD_NAME, ErrorMessages.PERSON_ENRICH_INVALID_NAME),
        (METHOD_MAP, SCENARIO_GOOD_LOCATION_NO_NAME, ErrorMessages.PERSON_ENRICH_INVALID_NAME_LOCATION),
        (METHOD_MAP, SCENARIO_GOOD_NAME_BAD_LOCATION, ErrorMessages.PERSON_ENRICH_INVALID_LOCATION),
        (METHOD_MAP, SCENARIO_GOOD_NAME_NO_LOCATION, ErrorMessages.PERSON_ENRICH_INVALID_NAME_LOCATION),
        (METHOD_RESOLVE, SCENARIO_GOOD_LOCATION_BAD_NAME, ErrorMessages.PERSON_ENRICH_INVALID_NAME),
        (METHOD_RESOLVE, SCENARIO_GOOD_LOCATION_NO_NAME, ErrorMessages.PERSON_ENRICH_INVALID_NAME_LOCATION),
        (METHOD_RESOLVE, SCENARIO_GOOD_NAME_BAD_LOCATION, ErrorMessages.PERSON_ENRICH_INVALID_LOCATION),
        (METHOD_RESOLVE, SCENARIO_GOOD_NAME_NO_LOCATION, ErrorMessages.PERSON_ENRICH_INVALID_NAME_LOCATION)
    ])
    def test_invalid_name_location(self, method, scenario, expected_error):
        queries = MockRequest.get_mock_request(REQUEST_TYPE, method, scenario)
        if type(queries) != list:
            queries = [queries]

        for query in queries:
            with pytest.raises(FullContactException) as fc_exception:
                getattr(self.fullcontact_client.identity, method)(**query)
            assert str(fc_exception.value).startswith(expected_error)

    # Correct name with no location and with Placekey
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MAP,
                                                          SCENARIO_GOOD_NAME_NO_LOCATION_WITH_PLACEKEY))
    def test_identity_map_with_name_and_placekey(self, query):
        self.fullcontact_client.identity.map(**query)

    # Full serialization
    @pytest.mark.parametrize("method", [METHOD_MAP, METHOD_MAP_RESOLVE, METHOD_RESOLVE, METHOD_DELETE])
    def test_full_serialization(self, mock_good_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_FULL_SERIALIZATION)
        getattr(self.fullcontact_client.identity, method)(**query)

    # Positive input parameters
    @pytest.mark.parametrize("method", [METHOD_MAP, METHOD_MAP_RESOLVE, METHOD_RESOLVE, METHOD_DELETE])
    def test_good_requests(self, mock_good_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method, SCENARIO_POSITIVE,
            key_replace={"recordId": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personId": ("<personId>", MockRequest.MOCK_PERSON_ID),
                         "recordIds": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personIds": ("<personId>", MockRequest.MOCK_PERSON_ID)
                         })
        if "recordId" in query:
            query["recordId"] = MockRequest.MOCK_RECORD_ID
        if "personId" in query:
            query["personId"] = MockRequest.MOCK_PERSON_ID
        result = getattr(self.fullcontact_client.identity, method)(**query)
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code

    # Parsing 404 response
    @pytest.mark.parametrize("method", [METHOD_RESOLVE, METHOD_DELETE])
    def test_404_requests(self, mock_good_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method, SCENARIO_404,
            key_replace={"recordId": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personId": ("<personId>", MockRequest.MOCK_PERSON_ID),
                         "recordIds": ("<recordId>", MockRequest.MOCK_RECORD_ID),
                         "personIds": ("<personId>", MockRequest.MOCK_PERSON_ID)
                         })
        if "recordId" in query:
            query["recordId"] = MockRequest.MOCK_RECORD_ID
        if "personId" in query:
            query["personId"] = MockRequest.MOCK_PERSON_ID
        result = getattr(self.fullcontact_client.identity, method)(**query)
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code

    # Parsing 401 response
    @pytest.mark.parametrize("method", [METHOD_MAP, METHOD_MAP_RESOLVE, METHOD_RESOLVE, METHOD_DELETE])
    def test_401_requests(self, mock_401_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method, SCENARIO_401, int(SCENARIO_401),
            message_replace=("<api_key>", MockRequest.MOCK_TOKEN))
        if "recordId" in query:
            query["recordId"] = MockRequest.MOCK_RECORD_ID
        if "personId" in query:
            query["personId"] = MockRequest.MOCK_PERSON_ID
        result = getattr(self.fullcontact_client.identity, method)(**query)
        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")
