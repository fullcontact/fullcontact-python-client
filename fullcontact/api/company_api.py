# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Company Enrich and Search
API requests.
"""

from concurrent.futures import Future

from .base.enrich_base import EnrichBase
from ..response.company_response import CompanyEnrichResponse, CompanySearchResponse
from ..schema.company_schema import CompanyEnrichRequestSchema, CompanySearchRequestSchema


class CompanyApi(EnrichBase):
    r"""
    Class that provides methods to perform
    Company Enrich and Search operations.
    """
    _enrich_endpoint = "company.enrich"
    _enrich_request_handler = CompanyEnrichRequestSchema()
    _enrich_response_handler = CompanyEnrichResponse

    _search_endpoint = "company.search"
    _search_request_handler = CompanySearchRequestSchema()
    _search_response_handler = CompanySearchResponse

    def search(self, headers: dict = None, **query) -> _search_response_handler:
        r"""
        POST query to FullContact Company Search API

        :param query: query as kwargs, for creating request body
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in self._search_response_handler
        """

        return self._validate_and_post_to_api(
            self._search_request_handler,
            self._search_response_handler,
            self._search_endpoint,
            query,
            headers
        )

    def search_async(self, headers: dict = None, **query) -> Future:
        r"""
        POST query to FullContact Company Search API

        :param query: query as kwargs, for creating request body
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in self._search_response_handler
        """
        return self.config.get_executor().submit(self.search, headers, **query)
