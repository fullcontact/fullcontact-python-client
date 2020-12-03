# -*- coding: utf-8 -*-

"""
This module serves the base class for all
FullContact Enrich API request classes.
"""

from abc import ABCMeta, abstractmethod
from concurrent.futures import Future

from .base_api import BaseApi
from ...schema.base.schema_base import BaseRequestSchema
from ...response.base.enrich_base import BaseEnrichResponse


class EnrichBaseApi(BaseApi, metaclass=ABCMeta):

    @property
    @abstractmethod
    def _enrich_endpoint(self) -> str:
        r"""
        Endpoint for enrich.

        :return: Enrich endpoint that can be used by self._enrich_url
        """
        raise NotImplementedError(
            "The property '_enrich_endpoint' is "
            "not implemented in %s" % self.__class__
        )

    @property
    @abstractmethod
    def _enrich_request(self) -> BaseRequestSchema:
        r"""
        Handler for the Enrich API request.
        This has to be the instance of a class which provides a validate()
        method to validate the enrich request
        """
        raise NotImplementedError(
            "The property '_enrich_request' is "
            "not implemented in %s" % self.__class__
        )

    @property
    @abstractmethod
    def _enrich_response(self) -> BaseEnrichResponse:
        r"""
        Handler for the output data.
        This has to be class that accepts only requests.Response as parameter
        in the constructor
        """
        raise NotImplementedError(
            "The property '_enrich_response' is "
            "not implemented in %s" % self.__class__
        )

    def enrich(self, headers: dict = None, **query) -> _enrich_response:
        r"""
        POST query to FullContact Enrich API.

        :param query: query as kwargs, for creating request body
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in self._enrich_response
        """

        return self._validate_and_post_to_api(
            self._enrich_request,
            self._enrich_response,
            self._enrich_endpoint,
            query,
            headers
        )

    def enrich_async(self, headers: dict = None, **query) -> Future:
        r"""
        POST query to FullContact Enrich API asynchronously.

        :param query: query as kwargs, for creating request body
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response object
        wrapped in self._enrich_response.
        """
        return self.config.get_executor().submit(self.enrich, headers, **query)
