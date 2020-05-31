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
    map_endpoint = "identity.map"
    resolve_endpoint = "identity.resolve"
    delete_endpoint = "identity.delete"

    _map_request_handler = IdentityMapSchema()
    _resolve_request_handler = IdentityResolveSchema()
    _delete_request_handler = IdentityDeleteSchema()

    _map_response_handler = IdentityMapResponse
    _resolve_response_handler = IdentityResolveResponse
    _delete_response_handler = IdentityDeleteResponse

    def map(self, **fields) -> _map_response_handler:
        r"""
        POST query to FullContact Identity Map API.

        :param fields: fields to be used for identity.map
        :return: requests.Response wrapped in _map_response_handler
        """
        return self._validate_and_post_to_api(
            self._map_request_handler,
            self._map_response_handler,
            self.map_endpoint,
            fields
        )

    def resolve(self, **identifiers) -> _resolve_response_handler:
        r"""
        POST query to FullContact Identity Resolve API.

        :param identifiers: identifiers to be used for identity.resolve
        :return: requests.Response wrapped in _resolve_response_handler
        """
        return self._validate_and_post_to_api(
            self._resolve_request_handler,
            self._resolve_response_handler,
            self.resolve_endpoint,
            identifiers
        )

    def delete(self, recordId: str) -> _delete_response_handler:
        r"""
        POST query to FullContact Identity Delete API.

        :param recordId: recordId to be used for identity.delete
        :return: requests.Response wrapped in _delete_response_handler
        """
        identifiers = dict(recordId=recordId)
        return self._validate_and_post_to_api(
            self._delete_request_handler,
            self._delete_response_handler,
            self.delete_endpoint,
            identifiers
        )

    def map_async(self, **fields) -> Future:
        r"""
        POST query to FullContact Identity Map API asynchronously.

        :param fields: fields to be used for identity.map
        :return: Future object. result() will return a requests.Response
        wrapped in self._map_response_handler
        """
        return self.config.get_executor().submit(self.map, **fields)

    def resolve_async(self, **identifiers) -> Future:
        r"""
        POST query to FullContact Identity Resolve API asynchronously.

        :param identifiers: identifiers to be used for identity.resolve
        :return: Future object. result() will return a requests.Response
        wrapped in self._resolve_response_handler
        """
        return self.config.get_executor().submit(self.resolve, **identifiers)

    def delete_async(self, recordId) -> Future:
        r"""
        POST query to FullContact Identity Delete API asynchronously.

        :param recordId: recordId to be used for identity.delete
        :return: Future object. result() will return a requests.Response
        wrapped in self._delete_response_handler
        """
        return self.config.get_executor().submit(self.delete, recordId)
