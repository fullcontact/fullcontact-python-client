import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from fullcontact.exceptions import FullContactException
from .utils.error_messages import ErrorMessages
from .utils.mock_request import MockRequest
from .utils.mock_response import MockResponse

REQUEST_TYPE = "permission"
METHOD_CREATE = "create"
METHOD_DELETE = "delete"
METHOD_FIND = "find"
METHOD_CURRENT = "current"
METHOD_VERIFY = "verify"
SCENARIO_POSITIVE = "positive"
SCENARIO_MISSING_REQUIRED_FIELDS = "missing_required"


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_good_create_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_CREATE, test_scenario=SCENARIO_POSITIVE,
                                              status_code=202)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_good_find_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_FIND, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_good_current_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_CURRENT, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_good_verify_response(monkeypatch):
    def mock_post(*args, **kwargs):
        return MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_VERIFY, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


########################################################################################################################


class TestPermissionApi(object):

    def setup(self):
        self.fullcontact_client = FullContactClient(MockRequest.MOCK_TOKEN)

    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_CREATE,
                                                          SCENARIO_MISSING_REQUIRED_FIELDS))
    def test_permission_create_missing_required(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.permission.create(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.PERMISSION_CREATE_MISSING_REQUIRED_FIELDS)

    def test_permission_delete_missing_required(self):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.permission.delete({})
        assert str(fc_exception.value).startswith(ErrorMessages.PERMISSION_DELETE_MISSING_REQUIRED_FIELDS)

    @pytest.mark.parametrize("query",
                             MockRequest.get_mock_request(REQUEST_TYPE, METHOD_VERIFY,
                                                          SCENARIO_MISSING_REQUIRED_FIELDS))
    def test_permission_verify_missing_required(self, query):
        with pytest.raises(FullContactException) as fc_exception:
            self.fullcontact_client.permission.verify(**query)
        assert str(fc_exception.value).startswith(ErrorMessages.PERMISSION_VERIFY_MISSING_REQUIRED_FIELDS)

    def test_permission_create_positive(self, mock_good_create_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_CREATE, SCENARIO_POSITIVE)
        result = self.fullcontact_client.permission.create(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_CREATE,
            test_scenario=SCENARIO_POSITIVE, status_code=202
        )
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    def test_permission_delete_positive(self, mock_good_create_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_DELETE, SCENARIO_POSITIVE)
        result = self.fullcontact_client.permission.delete(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_CREATE,
            test_scenario=SCENARIO_POSITIVE, status_code=202
        )
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    def test_permission_find_positive(self, mock_good_find_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_FIND, SCENARIO_POSITIVE)
        result = self.fullcontact_client.permission.find(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_FIND,
            test_scenario=SCENARIO_POSITIVE
        )
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    def test_permission_current_positive(self, mock_good_current_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_FIND, SCENARIO_POSITIVE)
        result = self.fullcontact_client.permission.current(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_CURRENT,
            test_scenario=SCENARIO_POSITIVE
        )
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    def test_permission_verify_positive(self, mock_good_verify_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_VERIFY, SCENARIO_POSITIVE)
        result = self.fullcontact_client.permission.verify(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=METHOD_VERIFY,
            test_scenario=SCENARIO_POSITIVE
        )
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()
