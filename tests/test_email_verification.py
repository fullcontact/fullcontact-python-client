import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from .utils.error_messages import ErrorMessages
from .utils.mock_request import MockRequest
from .utils.mock_response import MockResponse

REQUEST_TYPE = "verification"
METHOD_EMAIL = "email"
SCENARIO_POSITIVE = "positive"


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(
            REQUEST_TYPE,
            method=METHOD_EMAIL,
            test_scenario=SCENARIO_POSITIVE
        )

    monkeypatch.setattr(Session, "get", mock_post)


########################################################################################################################


class TestVerificationApi(object):

    def setup(self):
        self.fullcontact_client = FullContactClient(MockRequest.MOCK_TOKEN)

    # Empty query provided)
    def test_empty_query(self):
        with pytest.raises(TypeError) as fc_exception:
            self.fullcontact_client.verification.email()

        assert str(fc_exception.value).startswith(ErrorMessages.VERIFICATION_EMAIL_MISSING_ARGUMENT)

    # Send a good request
    def test_good_requests(self, mock_good_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_EMAIL, SCENARIO_POSITIVE)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, METHOD_EMAIL, SCENARIO_POSITIVE
        )
        result = self.fullcontact_client.verification.email(**query)
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code
