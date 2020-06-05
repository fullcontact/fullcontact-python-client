# -*- coding: utf-8 -*-

"""
This module serves the base class for all
FullContact API request classes.
"""
from abc import ABCMeta
from typing import Callable, TypeVar

from requests import Response

from ...__about__ import __version__
from ...config.client_config import ClientConfig
from ...response.base.base import BaseApiResponse
from ...schema.base.schema_base import BaseSchema

BaseResponse = TypeVar("BaseResponse", bound=BaseApiResponse)


class BaseApi(object, metaclass=ABCMeta):
    """
    This class acts as the abstract base for all FullContact API
    subclasses. All the functions and attributes common to all
    FullContact API subclasses should be defined here.
    """
    _BASE_URL = "https://api.fullcontact.com/v3/"
    MAX_RETRY_COUNT = 5
    DEFAULT_DELAY = 1.0
    RETRY_STATUS_CODES = (429, 503)

    def __init__(self,
                 client_config: ClientConfig,
                 headers: dict = None
                 ):
        r"""
        Interface to communicate with FullContact API.

        :param client_config: The config to be used to make
        API calls.
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.
        """
        self.config = client_config
        self._headers = self._get_validated_headers(headers)

    @property
    def _default_headers(self):
        return {
            "User-Agent": "FullContact_Python_Client_V%s" % __version__,
            "Content-Type": "application/json",
            "Authorization": "Bearer %s" % self.config.get_api_key()
        }

    @staticmethod
    def _get_validated_headers(headers: dict) -> dict:
        r"""
        Check the type of the headers parameter.

        :param headers: Headers dict to be validated.

        :return: :param headers: if it is a dict with values. {} if None.

        :raises: FullContactException if headers is not dict or None.
        """
        validated_headers = headers if headers is not None else {}
        if type(validated_headers) != dict:
            raise TypeError("Parameter headers should be of type 'dict'")
        return validated_headers

    def _get_merged_headers(self, *headers) -> dict:
        r"""
        Validate and merge header dictionaries.

        :param headers: Multiple header dicts as args.
        """
        merged_headers = {}
        for header in headers:
            merged_headers.update(self._get_validated_headers(header))

        return merged_headers

    def _post_to_api(self,
                     endpoint: str,
                     data: dict = None,
                     headers: dict = None
                     ) -> Response:
        r"""
        Send POST request to API based on parameters.
        Method type is always POST for the requests.

        :param endpoint: endpoint to POST request to
        :param data: body of the request to be sent
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Response object
        """
        url = self._BASE_URL + endpoint
        data = data or {}

        final_headers = self._get_merged_headers(
            self._headers,
            headers,
            self._default_headers)

        return self.config.get_http_session().post(url=url,
                                                   json=data,
                                                   headers=final_headers)

    def _validate_and_post_to_api(self,
                                  request: BaseSchema,
                                  response: Callable[[Response], BaseApiResponse],
                                  endpoint: str,
                                  data: dict,
                                  headers: dict = None) -> BaseResponse:
        r"""
        Validate the request and map the response to a class.

        :param request: Validator object that provides a
        validate() method to validate the data.
        :param response: Class to be used to map the API response.
        :param endpoint: API endpoint to POST request to.
        :param data: Body of the request to be validated and posted.
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response object wrapped in response class.
        """
        validated_data = request.validate(data) or {}
        api_response = self._post_to_api(endpoint, validated_data, headers)

        if validated_data.get('webhookUrl', None) not in (None, ''):
            return BaseApiResponse(api_response)
        return response(api_response)
