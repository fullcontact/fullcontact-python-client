import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from fullcontact.exceptions import FullContactException
from fullcontact.schema.verify_schema import VerifyRequestSchema
from .utils.mock_request import MockRequest
from .utils.error_messages import ErrorMessages
from .utils.mock_response import MockResponse

REQUEST_TYPE = "verify"
METHOD_MATCH = "match"
METHOD_ACTIVITY = "activity"
METHOD_SIGNALS = "signals"
SCENARIO_POSITIVE = "positive"
SCENARIO_200 = "200"


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

