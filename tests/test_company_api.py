import pytest

from fullcontact import FullContactClient
from fullcontact.config.client_config import Session
from fullcontact.exceptions import FullContactException
from fullcontact.schema.company_schema import CompanyEnrichRequestSchema, CompanySearchRequestSchema
from .utils.mock_request import MockRequest
from .utils.error_messages import ErrorMessages
from .utils.mock_response import MockResponse

REQUEST_TYPE = "company"
METHOD_ENRICH = "enrich"
METHOD_SEARCH = "search"
SCENARIO_POSITIVE = "positive"
SCENARIO_202 = "202"
SCENARIO_404 = "404"
SCENARIO_401 = "401"
SCENARIO_VALID_WEBHOOK = "valid_webhook"
SCENARIO_INVALID_WEBHOOK = "invalid_webhook"
SCENARIO_FULL_SERIALIZATION = "full_serialization"


# MOCK API CALLS #######################################################################################################

@pytest.fixture
def mock_webhook_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        webhook_url = kwargs.get('json', {}).get('webhookUrl', '')
        method = METHOD_SEARCH if kwargs.get("url", "").endswith("search") else METHOD_ENRICH
        return MockResponse.get_mock_response(REQUEST_TYPE, method=method, test_scenario=SCENARIO_VALID_WEBHOOK,
                                              status_code=int(SCENARIO_202),
                                              message_replace=("<webhook_url>", webhook_url))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_webhook_bad_response(monkeypatch):
    def mock_post(*args, **kwargs):
        webhook_url = kwargs.get('json', {}).get('webhookUrl', '')
        method = METHOD_SEARCH if kwargs.get("url", "").endswith("search") else METHOD_ENRICH
        return MockResponse.get_mock_response(REQUEST_TYPE, method=method, test_scenario=SCENARIO_INVALID_WEBHOOK,
                                              status_code=400, message_replace=("<webhook_url>", webhook_url))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_good_response(monkeypatch):
    def mock_post(*args, **kwargs):
        method = METHOD_SEARCH if kwargs.get("url", "").endswith("search") else METHOD_ENRICH
        return MockResponse.get_mock_response(REQUEST_TYPE, method=method, test_scenario=SCENARIO_POSITIVE)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_404_response(monkeypatch):
    def mock_post(*args, **kwargs):
        method = METHOD_SEARCH if kwargs.get("url", "").endswith("search") else METHOD_ENRICH
        query = kwargs.get('json', {})
        message_replace = ("<input_query>", ", ".join(["%s=%s" % (k, v) for k, v in query.items()])) \
            if method == METHOD_SEARCH \
            else ("<domain_name>", query.get("domain", None))
        return MockResponse.get_mock_response(REQUEST_TYPE, method=method, test_scenario=SCENARIO_404,
                                              status_code=int(SCENARIO_404),
                                              message_replace=message_replace)

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_401_response(monkeypatch):
    def mock_post(*args, **kwargs):
        method = METHOD_SEARCH if kwargs.get("url", "").endswith("search") else METHOD_ENRICH
        return MockResponse.get_mock_response(REQUEST_TYPE, method=method, test_scenario=SCENARIO_401,
                                              status_code=int(SCENARIO_401),
                                              message_replace=("<api_key>", MockRequest.MOCK_TOKEN))

    monkeypatch.setattr(Session, "post", mock_post)


@pytest.fixture
def mock_202_response(monkeypatch):
    def mock_post(*args, **kwargs):
        method = METHOD_SEARCH if kwargs.get("url", "").endswith("search") else METHOD_ENRICH
        return MockResponse.get_mock_response(REQUEST_TYPE, method=method, test_scenario=SCENARIO_202,
                                              status_code=int(SCENARIO_202))

    monkeypatch.setattr(Session, "post", mock_post)


########################################################################################################################


class TestCompanyApi(object):

    def setup(self):
        self.fullcontact_client = FullContactClient(MockRequest.MOCK_TOKEN)

    # Empty query provided
    @pytest.mark.parametrize("function_name, expected_error_message", [
        (METHOD_ENRICH, ErrorMessages.COMPANY_ENRICH_NOT_QUERYABLE),
        (METHOD_SEARCH, ErrorMessages.COMPANY_SEARCH_NOT_QUERYABLE)
    ])
    def test_empty_query(self, function_name, expected_error_message):
        with pytest.raises(FullContactException) as fc_exception:
            getattr(self.fullcontact_client.company, function_name)()
        assert str(
            fc_exception.value).startswith(expected_error_message)

    # Acceptable input query provided
    @pytest.mark.parametrize("method", [METHOD_ENRICH, METHOD_SEARCH])
    def test_good_requests(self, mock_good_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        result = getattr(self.fullcontact_client.company, method)(**query)
        expected_result = MockResponse.get_mock_response(
            REQUEST_TYPE, method=method,
            test_scenario=SCENARIO_POSITIVE
        )
        assert result.json() and \
               result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.json() == expected_result.json()

    # Parse 202 message
    @pytest.mark.parametrize("method", [
        METHOD_ENRICH, METHOD_SEARCH
    ])
    def test_enrich_good_webhook_url(self, mock_webhook_good_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_FULL_SERIALIZATION)
        result = getattr(self.fullcontact_client.company, method)(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=method,
                                                         test_scenario=SCENARIO_VALID_WEBHOOK,
                                                         status_code=int(SCENARIO_202),
                                                         message_replace=(
                                                             "<webhook_url>", query.get("webhookUrl", "")
                                                         ))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # Invalid webhook
    @pytest.mark.parametrize("method", [METHOD_ENRICH, METHOD_SEARCH])
    def test_enrich_bad_webhook_url(self, mock_webhook_bad_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_FULL_SERIALIZATION)
        result = getattr(self.fullcontact_client.company, method)(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=method,
                                                         test_scenario=SCENARIO_INVALID_WEBHOOK,
                                                         status_code=400,
                                                         message_replace=(
                                                             "<webhook_url>", query.get("webhookUrl", "")
                                                         ))
        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # Full serialization using schema
    @pytest.mark.parametrize("method, schema", [
        (METHOD_ENRICH, CompanyEnrichRequestSchema()),
        (METHOD_SEARCH, CompanySearchRequestSchema())
    ])
    def test_full_schema_serialization(self, method, schema):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_FULL_SERIALIZATION)
        validated_query = schema.validate(query)
        assert validated_query == query

    # 202 when profile not found immediately

    def test_enrich_202(self, mock_202_response):
        query = MockRequest.get_mock_request(REQUEST_TYPE, METHOD_ENRICH, SCENARIO_POSITIVE)
        result = self.fullcontact_client.company.enrich(**query)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method=METHOD_ENRICH, test_scenario=SCENARIO_202,
                                                         status_code=int(SCENARIO_202))
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # 404 when profile not found
    @pytest.mark.parametrize("method", [METHOD_ENRICH, METHOD_SEARCH])
    def test_404(self, mock_404_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        message_replace = ("<input_query>", ", ".join(["%s=%s" % (k, v) for k, v in query.items()])) \
            if method == METHOD_SEARCH \
            else ("<domain_name>", query.get("domain", None))
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method, SCENARIO_404,
                                                         status_code=int(SCENARIO_404),
                                                         message_replace=message_replace)
        result = getattr(self.fullcontact_client.company, method)(**query)
        assert result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message")

    # 404 when profile not found
    @pytest.mark.parametrize("method", [METHOD_ENRICH, METHOD_SEARCH])
    def test_401(self, mock_401_response, method):
        query = MockRequest.get_mock_request(REQUEST_TYPE, method, SCENARIO_POSITIVE)
        expected_result = MockResponse.get_mock_response(REQUEST_TYPE, method, SCENARIO_401,
                                                         status_code=int(SCENARIO_401))
        result = getattr(self.fullcontact_client.company, method)(**query)
        assert not result.is_successful and \
               result.get_status_code() == expected_result.status_code and \
               result.get_message() == expected_result.json().get("message").replace("<api_key>",
                                                                                     MockRequest.MOCK_TOKEN)
