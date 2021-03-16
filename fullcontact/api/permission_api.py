"""
This module serves the class for making
FullContact Permission Create, Delete,
Find, Current, Verify API Requests.
"""

from concurrent.futures import Future

from .base.base_api import BaseApi
from ..response.permission_response import PermissionCreateResponse, PermissionDeleteResponse, PermissionFindResponse, \
    PermissionCurrentResponse, PermissionVerifyResponse
from ..schema.permission_schema import PermissionCreateRequestSchema, PermissionDeleteRequestSchema, \
    PermissionFindRequestSchema, PermissionCurrentRequestSchema, PermissionVerifyRequestSchema


class PermissionApi(BaseApi):
    r"""
     Class that provides methods to perform
     Permission Create, Delete, Find, Current, Verify operations.
     """
    _create_endpoint = "permission.create"
    _delete_endpoint = "permission.delete"
    _find_endpoint = "permission.find"
    _current_endpoint = "permission.current"
    _verify_endpoint = "permission.verify"

    _create_request = PermissionCreateRequestSchema()
    _delete_request = PermissionDeleteRequestSchema()
    _find_request = PermissionFindRequestSchema()
    _current_request = PermissionCurrentRequestSchema()
    _verify_request = PermissionVerifyRequestSchema()

    _create_response = PermissionCreateResponse
    _delete_response = PermissionDeleteResponse
    _find_response = PermissionFindResponse
    _current_response = PermissionCurrentResponse
    _verify_response = PermissionVerifyResponse

    def create(self, headers: dict = None, **query) -> _create_response:
        r"""
        POST Multifield query and consents to FullContact Permission Create API.

        :param query: Multifield query + Consent request.
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _create_response
        """
        return self._validate_and_post_to_api(
            self._create_request,
            self._create_response,
            self._create_endpoint,
            query,
            headers
        )

    def delete(self, headers: dict = None, **query) -> _create_response:
        r"""
        POST Multifield query to FullContact Permission Delete API.

        :param query: Multifield query.
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _delete_response
        """
        return self._validate_and_post_to_api(
            self._delete_request,
            self._delete_response,
            self._delete_endpoint,
            query,
            headers
        )

    def find(self, headers: dict = None, **query) -> _create_response:
        r"""
        POST Multifield query to FullContact Permission Find API.

        :param query: Multifield query.
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _find_response
        """
        return self._validate_and_post_to_api(
            self._find_request,
            self._find_response,
            self._find_endpoint,
            query,
            headers
        )

    def current(self, headers: dict = None, **query) -> _create_response:
        r"""
        POST Multifield query to FullContact Permission Current API.

        :param query: Multifield query.
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _current_response
        """
        return self._validate_and_post_to_api(
            self._current_request,
            self._current_response,
            self._current_endpoint,
            query,
            headers
        )

    def verify(self, headers: dict = None, **query) -> _create_response:
        r"""
        POST Multifield query and purposeId, channel to FullContact Permission Verify API.

        :param query: Multifield query + purposeId + channel.
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _verify_response
        """
        return self._validate_and_post_to_api(
            self._verify_request,
            self._verify_response,
            self._verify_endpoint,
            query,
            headers
        )

    def create_async(self, headers: dict = None, **query) -> Future:
        r"""
        POST Multifield query and consents to FullContact Permission Create API Asynchronously.

        :param query: Multifield query + Consent request.
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _create_response
        """
        return self.config.get_executor().submit(
            self.create,
            headers,
            **query
        )

    def delete_async(self, headers: dict = None, **query) -> Future:
        r"""

        POST Multifield query to FullContact Permission Delete API Asynchronously.

        :param query: Multifield query.
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _delete_response
        """
        return self.config.get_executor().submit(
            self.delete,
            headers,
            **query
        )

    def find_async(self, headers: dict = None, **query) -> Future:
        r"""
        POST Multifield query to FullContact Permission Find API Asynchronously.

        :param query: Multifield query.
        :param headers: Additional_headers to be passed.
         Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
         wrapped in _find_response
        """
        return self.config.get_executor().submit(
            self.find,
            headers,
            **query
        )

    def current_async(self, headers: dict = None, **query) -> Future:
        r"""
        POST Multifield query to FullContact Permission Current API Asynchronously.

        :param query: Multifield query.
        :param headers: Additional_headers to be passed.
         Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
         wrapped in _current_response
        """
        return self.config.get_executor().submit(
            self.current,
            headers,
            **query
        )

    def verify_async(self, headers: dict = None, **query) -> Future:
        r"""
        POST Multifield query and purposeId, channel to FullContact Permission Verify API Asynchronously.

        :param query: Multifield query + purposeId + channel.
        :param headers: Additional_headers to be passed.
         Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
         wrapped in _verify_response
        """
        return self.config.get_executor().submit(
            self.verify,
            headers,
            **query
        )
