import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from fullcontact.exceptions import FullContactException
from fullcontact.schema.person_schema import PersonRequestSchema
from .utils.mock_request import MockRequest
from .utils.error_messages import ErrorMessages
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
SCENARIO_GOOD_LOCATION_NO_NAME_GOOD_EMAIL = "good_location_no_name_good_email"
SCENARIO_GOOD_NAME_NO_LOCATION_GOOD_PHONE = "good_name_no_location_good_phone"
SCENARIO_GOOD_LOCATION_BAD_NAME_VALID_INPUT = "good_location_bad_name_valid_input"
SCENARIO_GOOD_NAME_BAD_LOCATION_VALID_INPUT = "good_name_bad_location_valid_input"


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_404_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_404,
                                              status_code=int(SCENARIO_404))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_401_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_401,
                                              status_code=int(SCENARIO_401), message_replace=("<api_key>",
                                                                                              MockRequest.MOCK_TOKEN))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_202_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_202,
                                              status_code=int(SCENARIO_202))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_webhook_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        webhook_url = kwargs.get("json", {}).get("webhookUrl", "")
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_VALID_WEBHOOK,
                                              status_code=int(SCENARIO_202),
                                              message_replace=("<webhook_url>", webhook_url))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_webhook_bad_response(monkeypatch):
    def mock_post(*args, **kwargs):
        webhook_url = kwargs.get("json", {}).get("webhookUrl", "")
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH,
                                              test_scenario=SCENARIO_INVALID_WEBHOOK,
                                              status_code=400, message_replace=("<webhook_url>", webhook_url))

    monkeypatch.setattr(Session, "post", mock_post)


########################################################################################################################


class TestPersonApi(object):

    def setup(self):
        self.fullcontact_client = FullContactClient(MockRequest.MOCK_TOKEN)

    # Empty query provided
    def test_empty_query(self):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.person.enrich()

        assert str(fc_exception.value).startswith(ErrorMessages.NO_QUERYABLE_INPUTS)

    # Wrong location data, correct name data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_GOOD_NAME_BAD_LOCATION))
    def test_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.person.enrich(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.PERSON_ENRICH_INVALID_LOCATION)

    # Wrong name data, correct location data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH,
                                                          SCENARIO_GOOD_LOCATION_BAD_NAME))
    def test_enrich_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.person.enrich(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.PERSON_ENRICH_INVALID_NAME)

    # Correct location with no name and correct name with no location
    @pytest.mark.parametrize("scenario", [
        SCENARIO_GOOD_NAME_NO_LOCATION,
        SCENARIO_GOOD_LOCATION_NO_NAME
    ])
    def test_enrich_missing_name_or_location(self, scenario):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, scenario)
        print(query)
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.person.enrich(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.PERSON_ENRICH_INVALID_NAME_LOCATION)

    # Correct location with no name and correct name with no location with valid queryable input
    @pytest.mark.parametrize("scenario", [
        SCENARIO_GOOD_LOCATION_NO_NAME_GOOD_EMAIL,
        SCENARIO_GOOD_NAME_NO_LOCATION_GOOD_PHONE
    ])
    def test_enrich_missing_name_or_location_with_valid_query(self, scenario, mock_good_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, scenario)
        self.fullcontact_client.person.enrich(**query) # Should not throw any exception

    # Wrong location data, correct name data and any other valid input
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH,
                                                          SCENARIO_GOOD_NAME_BAD_LOCATION_VALID_INPUT))
    def test_good_name_bad_location_with_valid_query(self, query):
        self.fullcontact_client.person.enrich(**query)

    # Wrong name data, correct location data and any other valid input
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH,
                                                          SCENARIO_GOOD_LOCATION_BAD_NAME_VALID_INPUT))
    def test_enrich_good_name_bad_location_with_valid_query(self, query):
        self.fullcontact_client.person.enrich(**query)

    # Acceptable input query provided
    def test_enrich_good_requests(self, mock_good_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.fullcontact_client.person.enrich(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_ENRICH,
            test_scenario=SCENARIO_POSITIVE
        )
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    # Parse 202 message
    def test_enrich_good_webhook_url(self, mock_webhook_good_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_FULL_SERIALIZATION)
        result = self.fullcontact_client.person.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH,
                                                         test_scenario=SCENARIO_VALID_WEBHOOK,
                                                         status_code=int(SCENARIO_202),
                                                         message_replace=("<webhook_url>", query.get("webhookUrl", "")))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # Invalid webhook
    def test_enrich_bad_webhook_url(self, mock_webhook_bad_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_FULL_SERIALIZATION)
        result = self.fullcontact_client.person.enrich(**query)
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
        validated_query = PersonRequestSchema().validate(query)
        assert validated_query == query

    # 202 when profile not found immediately
    def test_enrich_202(self, mock_202_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.fullcontact_client.person.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_202,
                                                         status_code=int(SCENARIO_202))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # 404 when profile not found
    def test_enrich_404(self, mock_404_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.fullcontact_client.person.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_404,
                                                         status_code=int(SCENARIO_404))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # 401 when invalid token is provided
    def test_enrich_401(self, mock_401_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.fullcontact_client.person.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH,
                                                         test_scenario=SCENARIO_401,
                                                         status_code=int(SCENARIO_401),
                                                         message_replace=("<api_key>",
                                                                          MockRequest.MOCK_TOKEN))
        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")
