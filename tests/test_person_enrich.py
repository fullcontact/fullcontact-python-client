import pytest
import requests
from fullcontact import PersonClient
from fullcontact.exceptions import FullContactException
from fullcontact.schema.person_schema import PersonSchema

from .utils.mock_request import MockRequest
from .utils.mock_response import MockResponse

REQUEST_TYPE = "person"
METHOD_ENRICH = "enrich"
SCENARIO_POSITIVE = "positive"
SCENARIO_202 = "202"
SCENARIO_404 = "404"
SCENARIO_401 = "401"
SCENARIO_VALID_WEBHOOK = "valid_webhook"
SCENARIO_INVALID_WEBHOOK = "invalid_webhook"
SCENARIO_GOOD_NAME_BAD_LOCATION = "good_name_bad_location"
SCENARIO_GOOD_NAME_NO_LOCATION = "good_name_no_location"
SCENARIO_GOOD_LOCATION_BAD_NAME = "good_location_bad_name"
SCENARIO_GOOD_LOCATION_NO_NAME = "good_location_no_name"
SCENARIO_FULL_SERIALIZATION = "full_serialization"


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_404_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_404,
                                              status_code=int(SCENARIO_404))

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_401_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_401,
                                              status_code=int(SCENARIO_401), message_replace=("<api_key>",
                                                                                              MockRequest.MOCK_TOKEN))

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_202_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_202,
                                              status_code=int(SCENARIO_202))

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_webhook_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        webhook_url = kwargs.get("json", {}).get("webhookUrl", "")
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_VALID_WEBHOOK,
                                              status_code=int(SCENARIO_202),
                                              message_replace=("<webhook_url>", webhook_url))

    monkeypatch.setattr(requests, "post", mock_post)


@pytest.fixture
def mock_webhook_bad_response(monkeypatch):
    def mock_post(*args, **kwargs):
        webhook_url = kwargs.get("json", {}).get("webhookUrl", "")
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH,
                                              test_scenario=SCENARIO_INVALID_WEBHOOK,
                                              status_code=400, message_replace=("<webhook_url>", webhook_url))

    monkeypatch.setattr(requests, "post", mock_post)


########################################################################################################################


class TestPersonEnrich(object):

    def setup(self):
        self.person_client = PersonClient(MockRequest.MOCK_TOKEN)

    # Empty/None API Key provided
    @pytest.mark.parametrize("api_key", ["", None])
    def test_empty_none_api_key(self, api_key):
        with pytest.raises(FullContactException) as fc_exception:
            PersonClient("")
        assert str(fc_exception.value) == "Invalid/Empty API Key provided."

    # No API Key provided
    def test_no_api_key(self):
        with pytest.raises(FullContactException) as fc_exception:
            PersonClient()
        assert str(fc_exception.value) == "Invalid/Empty API Key provided."

    # Acceptable API Key provided
    def test_good_api_key(self):
        PersonClient(MockRequest.MOCK_TOKEN)

    # Empty query provided
    def test_empty_query(self):
        with pytest.raises(FullContactException) as fc_exception:
            self.person_client.enrich()

        assert str(fc_exception.value) == "No queryable inputs given (" \
                                          "for example: email, emails, phone, phones," \
                                          " location, name, profiles, maids)"

    # Wrong location data, correct name data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_GOOD_NAME_BAD_LOCATION))
    def test_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.person_client.enrich(**query)
        assert str(fc_exception.value) == "Possible combinations to query by Location are:\n" \
                                          "addressLine1 + city + region\n" \
                                          "addressLine1 + city + regionCode\n" \
                                          "addressLine1 + postalCode"

    # Wrong name data, correct location data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH,
                                                          SCENARIO_GOOD_LOCATION_BAD_NAME))
    def test_enrich_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.person_client.enrich(**query)
        assert str(fc_exception.value) == "Possible combinations to query by Name are:\n" \
                                          "given + family\n" \
                                          "full"

    # Correct location with no name and correct name with no location
    @pytest.mark.parametrize("scenario", [
        SCENARIO_GOOD_NAME_NO_LOCATION,
        SCENARIO_GOOD_LOCATION_NO_NAME
    ])
    def test_enrich_missing_name_or_location(self, scenario):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, scenario)
        with pytest.raises(FullContactException) as fc_exception:
            self.person_client.enrich(**query)
        assert str(fc_exception.value) == "Location and Name have to be queried together"

    # Acceptable input query provided
    def test_enrich_good_requests(self, mock_good_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.person_client.enrich(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_ENRICH,
            test_scenario=SCENARIO_POSITIVE
        )
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.raw() == expected_result.json()

    # Parse 202 message
    def test_enrich_good_webhook_url(self, mock_webhook_good_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_FULL_SERIALIZATION)
        result = self.person_client.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_VALID_WEBHOOK,
                                              status_code=int(SCENARIO_202),
                                              message_replace=("<webhook_url>", query.get("webhookUrl", "")))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # Invalid webhook
    def test_enrich_bad_webhook_url(self, mock_webhook_bad_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_FULL_SERIALIZATION)
        result = self.person_client.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH,
                                                         test_scenario=SCENARIO_INVALID_WEBHOOK,
                                                         status_code=400,
                                                         message_replace=(
                                                             "<webhook_url>", query.get("webhookUrl", "")
                                                         ))
        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # Full serialization using schema
    def test_full_schema_serialization(self):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_FULL_SERIALIZATION)
        validated_query = PersonSchema().validate(query)
        assert validated_query == query

    # 202 when profile not found immediately
    def test_enrich_202(self, mock_202_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.person_client.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_202,
                                                         status_code=int(SCENARIO_202))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # 404 when profile not found
    def test_enrich_404(self, mock_404_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.person_client.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_404,
                                              status_code=int(SCENARIO_404))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # 401 when invalid token is provided
    def test_enrich_401(self, mock_401_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.person_client.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH,
                                                                 test_scenario=SCENARIO_401,
                                                                 status_code=int(SCENARIO_401),
                                                                 message_replace=("<api_key>",
                                                                                  MockRequest.MOCK_TOKEN))
        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")
