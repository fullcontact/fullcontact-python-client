# -*- coding: utf-8 -*-

"""
This module serves the base class for all
FullContact API request classes.
"""
from abc import ABCMeta
from typing import Callable, TypeVar

from requests import Response

from ...config.client_config import ClientConfig
from ...response.base.base import BaseApiResponse
from ...schema.base.schema_base import BaseSchema

BaseResponse = TypeVar("BaseResponse", bound=BaseApiResponse)


class ApiBase(object, metaclass=ABCMeta):
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
                 client_config: ClientConfig
                 ):
        r"""
        Interface to communicate with FullContact API.

        :param client_config: The config to be used to make
        API calls.
        """
        self.config = client_config

    def _post_to_api(self,
                     endpoint: str,
                     data: dict = None,
                     ) -> Response:
        r"""
        Send POST request to API based on parameters.
        Method type is always POST for the requests.

        :param endpoint: endpoint to POST request to
        :param data: body of the request to be sent
        :return: Response object
        """
        url = self._BASE_URL + endpoint
        data = data or {}
        headers = self.config.get_headers()

        headers.update({
            "Authorization": "Bearer %s" % self.config.get_api_key(),
            "Content-Type": "application/json"
        })

        return self.config.get_http_session().post(url=url,
                                                   json=data,
                                                   headers=headers)

    def _validate_and_post_to_api(self,
                                  request_validator: BaseSchema,
                                  response_validator: Callable[[Response], BaseApiResponse],
                                  endpoint: str,
                                  data: dict) -> BaseResponse:
        r"""
        Validate the request and map the response to a class.

        :param request_validator: Validator object that provides a
        validate() method to validate the data.
        :param response_validator: Class to be used to map the API response.
        :param endpoint: API endpoint to POST request to.
        :param data: Body of the request to be validated and posted.
        """
        validated_data = request_validator.validate(data) or {}
        api_response = self._post_to_api(endpoint, validated_data)

        if validated_data.get('webhookUrl', None) not in (None, ''):
            return BaseApiResponse(api_response)
        return response_validator(api_response)
