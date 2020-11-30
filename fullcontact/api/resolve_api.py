# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Identity Map, Resolve and Delete
API requests.
"""

from concurrent.futures import Future

from .base.base_api import BaseApi
from ..response.resolve_response import IdentityMapResponse, IdentityResolveResponse, IdentityDeleteResponse
from ..schema.resolve_schema import IdentityMapRequestSchema, IdentityResolveRequestSchema, IdentityDeleteRequestSchema


class ResolveApi(BaseApi):
    r"""
     Class that provides methods to perform
     Identity Resolution operations.
     """
    _map_endpoint = "identity.map"
    _resolve_endpoint = "identity.resolve"
    _delete_endpoint = "identity.delete"

    _map_request = IdentityMapRequestSchema()
    _resolve_request = IdentityResolveRequestSchema()
    _delete_request = IdentityDeleteRequestSchema()

    _map_response = IdentityMapResponse
    _resolve_response = IdentityResolveResponse
    _delete_response = IdentityDeleteResponse

    def map(self, headers: dict = None, **fields) -> _map_response:
        r"""
        POST query to FullContact Identity Map API.

        :param fields: Fields to be used for identity.map
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _map_response
        """
        return self._validate_and_post_to_api(
            self._map_request,
            self._map_response,
            self._map_endpoint,
            fields,
            headers
        )

    def resolve(self,
                headers: dict = None,
                include_tags: bool = False,
                **identifiers) -> _resolve_response:
        r"""
        POST query to FullContact Identity Resolve API.

        :param headers: Additional_headers to be passed. Authorization and Content-Type
        are added automatically.
        :param include_tags: Flag to toggle tags in the response.
        :param identifiers: identifiers to be used for identity.resolve

        :return: requests.Response wrapped in _resolve_response
        """
        return self._validate_and_post_to_api(
            self._resolve_request,
            self._resolve_response,
            self._resolve_endpoint,
            identifiers,
            dict(tags=include_tags),
            headers
        )

    def delete(self, recordId: str, headers: dict = None) -> _delete_response:
        r"""
        POST query to FullContact Identity Delete API.

        :param recordId: recordId to be used for identity.delete
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _delete_response
        """
        identifiers = dict(recordId=recordId)
        return self._validate_and_post_to_api(
            self._delete_request,
            self._delete_response,
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
        wrapped in self._map_response
        """
        return self.config.get_executor().submit(self.map, headers, **fields)

    def resolve_async(self, headers: dict = None, **identifiers) -> Future:
        r"""
        POST query to FullContact Identity Resolve API asynchronously.

        :param identifiers: identifiers to be used for identity.resolve
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in self._resolve_response
        """
        return self.config.get_executor().submit(self.resolve, headers, **identifiers)

    def delete_async(self, recordId, headers: dict = None) -> Future:
        r"""
        POST query to FullContact Identity Delete API asynchronously.

        :param recordId: recordId to be used for identity.delete
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in self._delete_response
        """
        return self.config.get_executor().submit(self.delete, recordId, headers)
