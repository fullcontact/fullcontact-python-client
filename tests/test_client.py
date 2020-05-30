import pytest

from fullcontact import FullContactClient
from fullcontact.exceptions import FullContactException
from .utils.mock_request import MockRequest


class TestFullContactClient(object):

    # No API Key provided
    def test_no_api_key(self):
        with pytest.raises(TypeError):
            FullContactClient()

    # Empty/None API Key provided
    @pytest.mark.parametrize("api_key", ["", None])
    def test_empty_none_api_key(self, api_key):
        with pytest.raises(FullContactException) as fc_exception:
            FullContactClient(api_key)
        assert str(fc_exception.value) == "Invalid/Empty API Key provided."

    # API Key provided as bytes
    def test_invalid_type_api_key(self):
        with pytest.raises(TypeError) as type_error:
            FullContactClient(MockRequest.MOCK_TOKEN.encode("utf-8"))
        assert str(type_error.value) == "Parameter 'api_key' should be of type 'str'"

    # Acceptable API Key provided
    def test_good_api_key(self):
        FullContactClient(MockRequest.MOCK_TOKEN)


