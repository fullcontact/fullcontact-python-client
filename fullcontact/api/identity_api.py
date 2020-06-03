# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Identity Map, Resolve and Delete
API requests.
"""

from concurrent.futures import Future

from .base.base import ApiBase
from ..response.identity_response import IdentityMapResponse, IdentityResolveResponse, IdentityDeleteResponse
from ..schema.identity_schema import IdentityMapSchema, IdentityResolveSchema, IdentityDeleteSchema


class IdentityApi(ApiBase):
    r"""
     Class that provides methods to perform
     Identity Resolution operations.
     """
    _map_endpoint = "identity.map"
    _resolve_endpoint = "identity.resolve"
    _delete_endpoint = "identity.delete"

    _map_request_handler = IdentityMapSchema()
    _resolve_request_handler = IdentityResolveSchema()
    _delete_request_handler = IdentityDeleteSchema()

    _map_response_handler = IdentityMapResponse
    _resolve_response_handler = IdentityResolveResponse
    _delete_response_handler = IdentityDeleteResponse

    def map(self, headers: dict = None, **fields) -> _map_response_handler:
        r"""
        POST query to FullContact Identity Map API.

        :param fields: fields to be used for identity.map
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _map_response_handler
        """
        return self._validate_and_post_to_api(
            self._map_request_handler,
            self._map_response_handler,
            self._map_endpoint,
            fields,
            headers
        )

    def resolve(self, headers: dict = None, **identifiers) -> _resolve_response_handler:
        r"""
        POST query to FullContact Identity Resolve API.

        :param identifiers: identifiers to be used for identity.resolve
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _resolve_response_handler
        """
        return self._validate_and_post_to_api(
            self._resolve_request_handler,
            self._resolve_response_handler,
            self._resolve_endpoint,
            identifiers,
            headers
        )

    def delete(self, recordId: str, headers: dict = None) -> _delete_response_handler:
        r"""
        POST query to FullContact Identity Delete API.

        :param recordId: recordId to be used for identity.delete
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _delete_response_handler
        """
        identifiers = dict(recordId=recordId)
        return self._validate_and_post_to_api(
            self._delete_request_handler,
            self._delete_response_handler,
            self._delete_endpoint,
            identifiers,
            headers
        )

    def map_async(self, headers: dict = None, **fields) -> Future:
        r"""
        POST query to FullContact Identity Map API asynchronously.

        :param fields: fields to be used for identity.map
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.
        :return: Future object. result() will return a requests.Response
        wrapped in self._map_response_handler
        """
        return self.config.get_executor().submit(self.map, headers, **fields)

    def resolve_async(self, headers: dict = None, **identifiers) -> Future:
        r"""
        POST query to FullContact Identity Resolve API asynchronously.

        :param identifiers: identifiers to be used for identity.resolve
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in self._resolve_response_handler
        """
        return self.config.get_executor().submit(self.resolve, headers, **identifiers)

    def delete_async(self, recordId, headers: dict = None) -> Future:
        r"""
        POST query to FullContact Identity Delete API asynchronously.

        :param recordId: recordId to be used for identity.delete
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in self._delete_response_handler
        """
        return self.config.get_executor().submit(self.delete, recordId, headers)
