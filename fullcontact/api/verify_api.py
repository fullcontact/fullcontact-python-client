# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Verify Activity, Match and Signals
API requests.
"""

from concurrent.futures import Future

from .base.base_api import BaseApi
from ..response.verify_response import VerifyActivityResponse, VerifyMatchResponse, VerifySignalResponse
from ..schema.verify_schema import VerifyRequestSchema


class VerifyApi(BaseApi):
    r"""
     Class that provides methods to perform
     Identity Resolution operations.
     """
    _match_endpoint = "verify.match"
    _signals_endpoint = "verify.signals"
    _activity_endpoint = "verify.activity"

    _verify_request = VerifyRequestSchema()

    _match_response = VerifyMatchResponse
    _signals_response = VerifySignalResponse
    _activity_response = VerifyActivityResponse

    def match(self, headers: dict = None, **query) -> _match_response:
        r"""
        POST query to FullContact Verify Match API.

        :param query: query as kwargs, for creating request body
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _match_response
        """
        return self._validate_and_post_to_api(
            self._verify_request,
            self._match_response,
            self._match_endpoint,
            query,
            headers
        )

    def signals(self,
                headers: dict = None,
                **query) -> _signals_response:
        r"""
        POST query to FullContact Verify Signals API.

        :param headers: Additional_headers to be passed. Authorization and Content-Type
        are added automatically.
        :param query: query as kwargs, for creating request body

        :return: requests.Response wrapped in _signals_response
        """
        return self._validate_and_post_to_api(
            self._verify_request,
            self._signals_response,
            self._signals_endpoint,
            query,
            headers
        )

    def activity(self, headers: dict = None, **query) -> _activity_response:
        r"""
        POST query to FullContact Verify Activity API.

        :param query: query as kwargs, for creating request body
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _activity_response
        """
        return self._validate_and_post_to_api(
            self._verify_request,
            self._activity_response,
            self._activity_endpoint,
            query,
            headers
        )

    def match_async(self, headers: dict = None, **query) -> Future:
        r"""
        POST query to FullContact Verify Match API Asynchronously.

        :param query: query as kwargs, for creating request body
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
         wrapped in _match_response
        """
        return self.config.get_executor().submit(self.match, headers, **query)

    def signals_async(self,
                      headers: dict = None,
                      **query) -> Future:
        r"""
        POST query to FullContact Verify Signals API.

        :param headers: Additional_headers to be passed. Authorization and Content-Type
        are added automatically.
        :param query: query as kwargs, for creating request body

        :return: Future object. result() will return a requests.Response
        wrapped in _signals_response
        """
        return self.config.get_executor().submit(self.signals, headers, **query)

    def activity_sync(self, headers: dict = None, **query) -> Future:
        r"""
        POST query to FullContact Verify Activity API.

        :param query: query as kwargs, for creating request body
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _activity_response
        """
        return self.config.get_executor().submit(self.activity, headers, **query)
