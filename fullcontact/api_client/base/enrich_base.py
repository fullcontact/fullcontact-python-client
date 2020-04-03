# -*- coding: utf-8 -*-

"""
This module serves the base class for all
FullContact Enrich API request classes.
"""

from abc import ABCMeta, abstractmethod
from concurrent.futures import Future

from .base import ApiBase
from ...response.base.base import BaseApiResponse


class EnrichBase(ApiBase, metaclass=ABCMeta):

    @property
    @abstractmethod
    def enrich_endpoint(self) -> str:
        r"""
        Endpoint for enrich
        :return: Enrich endpoint that can be used by self._enrich_url
        """
        raise NotImplementedError(
            "The property 'enrich_endpoint' is "
            "not implemented in %s" % self.__class__
        )

    @property
    @abstractmethod
    def _enrich_request_handler(self):
        r"""
        Handler for the Enrich API request
        This has to be the instance of a class which provides a validate()
        method to validate the enrich request
        """
        raise NotImplementedError(
            "The property '_enrich_request_handler' is "
            "not implemented in %s" % self.__class__
        )

    @property
    @abstractmethod
    def _enrich_response_handler(self):
        r"""
        Handler for the output data.
        This has to be class that accepts only requests.Response as parameter
        in the constructor
        """
        raise NotImplementedError(
            "The property '_enrich_response_handler' is "
            "not implemented in %s" % self.__class__
        )

    @property
    def _enrich_url(self) -> str:
        r"""
        URL to be used by self.enrich()
        :return: Enrich URL created by concatenating ApiBase._BASE_URL and
        self.enrich_endpoint
        """
        return self._BASE_URL + self.enrich_endpoint

    def enrich(self,
               headers: dict = None,
               delay: int = ApiBase._DEFAULT_DELAY,
               max_retries: int = ApiBase._MAX_RETRY_COUNT,
               **query
               ) -> _enrich_response_handler:
        r"""
        POST query to FullContact Enrich API
        :param headers: headers to be added to the request
        :param delay: base delay for exponential back-off
        :param max_retries: maximum number of retries
        :param query: query as kwargs, for creating request body
        :return: requests.Response wrapped in self._enrich_response_handler
        """
        validated_query = self._enrich_request_handler.validate(query) or {}
        api_response = self._get_from_api(
            url=self._enrich_url,
            data=validated_query,
            headers=headers,
            delay=delay,
            max_retries=max_retries
        )
        if validated_query.get('webhookUrl', None) not in (None, ''):
            return BaseApiResponse(api_response)
        return self._enrich_response_handler(api_response)

    def enrich_async(self,
                     headers: dict = None,
                     delay: int = ApiBase._DEFAULT_DELAY,
                     max_retries: int = ApiBase._MAX_RETRY_COUNT,
                     **query
                     ) -> Future:
        r"""
        POST query to FullContact Enrich API asynchronously
        :param headers: headers to be added to the request
        :param delay: base delay for exponential back-off
        :param max_retries: maximum number of retries
        :param query: query as kwargs, for creating request body
        :return: Future object. result() will return a requests.Response object
        wrapped in self._enrich_response_handler.
        """
        return self._executor.submit(self.enrich, headers, delay, max_retries, **query)
