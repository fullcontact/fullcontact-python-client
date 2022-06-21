import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from fullcontact.exceptions import FullContactException
from .utils.mock_request import MockRequest
from .utils.error_messages import ErrorMessages
from .utils.mock_response import MockResponse

REQUEST_TYPE = "verify"
METHOD_MATCH = "match"
METHOD_ACTIVITY = "activity"
METHOD_SIGNALS = "signals"
SCENARIO_POSITIVE = "positive"
SCENARIO_200 = "200"
SCENARIO_404 = "400"
SCENARIO_GOOD_LOCATION_BAD_NAME = "good_location_bad_name"
SCENARIO_GOOD_NAME_BAD_LOCATION = "good_name_bad_location"
SCENARIO_GOOD_NAME_NO_LOCATION = "good_name_no_location"
SCENARIO_GOOD_LOCATION_NO_NAME = "good_location_no_name"
SCENARIO_GOOD_NAME_BAD_LOCATION_VALID_INPUT = "good_name_bad_location_valid_input"
SCENARIO_GOOD_LOCATION_BAD_NAME_VALID_INPUT = "good_location_bad_name_valid_input"


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_good_response_match(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_MATCH, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_good_response_signals(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_SIGNALS, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_good_response_activity(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ACTIVITY, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_bad_response_match(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_MATCH, test_scenario=SCENARIO_404,
                                              status_code=int(SCENARIO_404))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_bad_response_signals(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_SIGNALS, test_scenario=SCENARIO_404,
                                              status_code=int(SCENARIO_404))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_bad_response_activity(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ACTIVITY, test_scenario=SCENARIO_404,
                                              status_code=int(SCENARIO_404))

    monkeypatch.setattr(Session, "post", mock_post)


########################################################################################################################


class TestVerifyApi(object):

    def setup(self):
        self.fullcontact_client = FullContactClient(MockRequest.MOCK_TOKEN)

    # Empty query provided
    def test_empty_query(self):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.match()

        assert str(fc_exception.value).startswith(ErrorMessages.NO_QUERYABLE_INPUTS)

    # Good Request Data
    def test_match_positive(self, mock_good_response_match):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MATCH, SCENARIO_POSITIVE)
        result = self.fullcontact_client.verify.match(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_MATCH,
            test_scenario=SCENARIO_POSITIVE
        )

        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    def test_activity_positive(self, mock_good_response_activity):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ACTIVITY, SCENARIO_POSITIVE)
        result = self.fullcontact_client.verify.activity(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_ACTIVITY,
            test_scenario=SCENARIO_POSITIVE
        )

        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    def test_signals_positive(self, mock_good_response_signals):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_SIGNALS, SCENARIO_POSITIVE)
        result = self.fullcontact_client.verify.signals(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_SIGNALS,
            test_scenario=SCENARIO_POSITIVE
        )

        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    def test_match_good_name_bad_location_with_valid_query(self, mock_good_response_match):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MATCH, SCENARIO_GOOD_NAME_BAD_LOCATION_VALID_INPUT)
        for i in query:
            result = self.fullcontact_client.verify.match(**i)

            assert result.is_successful and \
                   result.get_status_code() == 200

    def test_signals_good_name_bad_location_with_valid_query(self, mock_good_response_signals):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_SIGNALS, SCENARIO_GOOD_NAME_BAD_LOCATION_VALID_INPUT)
        for i in query:
            result = self.fullcontact_client.verify.signals(**i)

            assert result.is_successful and \
                   result.get_status_code() == 200

    def test_activity_good_name_bad_location_with_valid_query(self, mock_good_response_signals):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ACTIVITY, SCENARIO_GOOD_NAME_BAD_LOCATION_VALID_INPUT)
        for i in query:
            result = self.fullcontact_client.verify.activity(**i)

            assert result.is_successful and \
                   result.get_status_code() == 200

    def test_match_good_location_bad_name_with_valid_query(self, mock_good_response_match):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MATCH, SCENARIO_GOOD_LOCATION_BAD_NAME_VALID_INPUT)
        for i in query:
            result = self.fullcontact_client.verify.match(**i)

            assert result.is_successful and \
                   result.get_status_code() == 200

    def test_activity_good_location_bad_name_with_valid_query(self, mock_good_response_match):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ACTIVITY, SCENARIO_GOOD_LOCATION_BAD_NAME_VALID_INPUT)
        for i in query:
            result = self.fullcontact_client.verify.activity(**i)

            assert result.is_successful and \
                   result.get_status_code() == 200

    def test_signals_good_location_bad_name_with_valid_query(self, mock_good_response_match):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_SIGNALS, SCENARIO_GOOD_LOCATION_BAD_NAME_VALID_INPUT)
        for i in query:
            result = self.fullcontact_client.verify.signals(**i)

            assert result.is_successful and \
                   result.get_status_code() == 200

    # Wrong name data, correct location data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MATCH,
                                                          SCENARIO_GOOD_LOCATION_BAD_NAME))
    def test_match_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.match(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_NAME)

    # Wrong name data, correct location data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_SIGNALS,
                                                          SCENARIO_GOOD_LOCATION_BAD_NAME))
    def test_signals_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.signals(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_NAME)

    # Wrong name data, correct location data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ACTIVITY,
                                                          SCENARIO_GOOD_LOCATION_BAD_NAME))
    def test_activity_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.activity(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_NAME)

    # Wrong location data, correct name data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MATCH,
                                                          SCENARIO_GOOD_NAME_BAD_LOCATION))
    def test_match_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.match(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_LOCATION)

    # Wrong location data, correct name data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_SIGNALS,
                                                          SCENARIO_GOOD_NAME_BAD_LOCATION))
    def test_signals_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.signals(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_LOCATION)

    # Wrong location data, correct name data
    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ACTIVITY,
                                                          SCENARIO_GOOD_NAME_BAD_LOCATION))
    def test_activity_good_name_bad_location_query(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.activity(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_LOCATION)

    # Correct location with no name and correct name with no location
    @pytest.mark.parametrize("scenario", [
        SCENARIO_GOOD_NAME_NO_LOCATION,
        SCENARIO_GOOD_LOCATION_NO_NAME
    ])
    def test_match_missing_name_or_location(self, scenario):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MATCH, scenario)
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.match(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_NAME_LOCATION)

    # Correct location with no name and correct name with no location
    @pytest.mark.parametrize("scenario", [
        SCENARIO_GOOD_NAME_NO_LOCATION,
        SCENARIO_GOOD_LOCATION_NO_NAME
    ])
    def test_activity_missing_name_or_location(self, scenario):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ACTIVITY, scenario)
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.activity(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_NAME_LOCATION)

    # Correct location with no name and correct name with no location
    @pytest.mark.parametrize("scenario", [
        SCENARIO_GOOD_NAME_NO_LOCATION,
        SCENARIO_GOOD_LOCATION_NO_NAME
    ])
    def test_signals_missing_name_or_location(self, scenario):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_SIGNALS, scenario)
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.verify.signals(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.VERIFY_INVALID_NAME_LOCATION)

    # Bad Request Data
    def test_match_404(self, mock_bad_response_match):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_MATCH, SCENARIO_404)
        result = self.fullcontact_client.verify.match(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_MATCH,
            test_scenario=SCENARIO_404,
            status_code=int(SCENARIO_404)
        )

        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    # Bad Request Data
    def test_activity_404(self, mock_bad_response_activity):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ACTIVITY, SCENARIO_404)
        result = self.fullcontact_client.verify.activity(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_ACTIVITY,
            test_scenario=SCENARIO_404,
            status_code=int(SCENARIO_404)
        )

        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    # Bad Request Data
    def test_signals_404(self, mock_bad_response_signals):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_SIGNALS, SCENARIO_404)
        result = self.fullcontact_client.verify.signals(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_SIGNALS,
            test_scenario=SCENARIO_404,
            status_code=int(SCENARIO_404)
        )

        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()