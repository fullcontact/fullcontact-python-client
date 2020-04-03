# -*- coding: utf-8 -*-

"""
This module serves the base class for all
FullContact Enrich API request classes.
"""

from abc import ABCMeta, abstractmethod
from concurrent.futures import Future

from .base import ApiBase
from ...response.base.base import BaseApiResponse


class SearchBase(ApiBase, metaclass=ABCMeta):

    @property
    @abstractmethod
    def search_endpoint(self):
        r"""
                Endpoint for search
                :return: Search endpoint that can be used by self._search_url
                """
        raise NotImplementedError(
            "The property 'search_endpoint' is "
            "not implemented in %s" % self.__class__
        )

    @property
    @abstractmethod
    def _search_request_handler(self):
        r"""
        Handler for the Search API request
        This has to be the instance of a class which provides a validate()
        method to validate the search request
        """
        raise NotImplementedError(
            "The property '_search_request_handler' is "
            "not implemented in %s" % self.__class__
        )

    @property
    @abstractmethod
    def _search_response_handler(self):
        r"""
        Handler for the Search API response
        This has to be class that accepts only requests.Response as parameter
        in the constructor
        """
        raise NotImplementedError(
            "The property '_search_response_handler' is "
            "not implemented in %s" % self.__class__
        )

    @property
    def _search_url(self):
        r"""
        URL to be used by self.search()
        :return: Enrich URL created by concatenating
        ApiBase._BASE_URL and
        self.search_endpoint
        """
        return self._BASE_URL + self.search_endpoint

    def search(self,
               headers: dict = None,
               delay: int = ApiBase._DEFAULT_DELAY,
               max_retries: int = ApiBase._MAX_RETRY_COUNT,
               **query
               ) -> _search_response_handler:
        r"""
        POST query to FullContact Search API
        :param headers: headers to be added to the request
        :param delay: base delay for exponential back-off
        :param max_retries: maximum number of retries
        :param query: query as kwargs, for creating request body
        :return: requests.Response wrapped in self._search_response_handler
        """
        validated_query = self._search_request_handler.validate(query) or {}
        api_response = self._get_from_api(
            url=self._search_url,
            data=validated_query,
            headers=headers,
            delay=delay,
            max_retries=max_retries
        )
        if validated_query.get('webhookUrl', None) not in (None, ''):
            return BaseApiResponse(api_response)
        return self._search_response_handler(api_response)

    def search_async(self,
                     headers: dict = None,
                     delay: int = ApiBase._DEFAULT_DELAY,
                     max_retries: int = ApiBase._MAX_RETRY_COUNT,
                     **query
                     ) -> Future:
        r"""
        POST query to FullContact Search API
        :param headers: headers to be added to the request
        :param delay: base delay for exponential back-off
        :param max_retries: maximum number of retries
        :param query: query as kwargs, for creating request body
        :return: Future object. result() will return a requests.Response
        wrapped in self._search_response_handler
        """
        return self._executor.submit(self.search, headers, delay, max_retries, **query)
