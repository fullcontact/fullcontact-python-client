# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Tags Get, Create and Delete
API Requests.
"""

from concurrent.futures import Future

from .base.tags_base_api import TagsBaseApi
from ..response.tags_response import TagsGetResponse, TagsCreateResponse, TagsDeleteResponse
from ..schema.tags_schema import TagsGetRequestSchema, TagsCreateRequestSchema, TagsDeleteRequestSchema


class TagsApi(TagsBaseApi):
    r"""
     Class that provides methods to perform
     Tags Get, Create and Delete operations.
     """
    _get_endpoint = "tags.get"
    _create_endpoint = "tags.create"
    _delete_endpoint = "tags.delete"

    _get_request = TagsGetRequestSchema()
    _create_request = TagsCreateRequestSchema()
    _delete_request = TagsDeleteRequestSchema()

    _get_response = TagsGetResponse
    _create_response = TagsCreateResponse
    _delete_response = TagsDeleteResponse

    def get(self, headers: dict = None, **identifiers) -> _get_response:
        r"""
        POST identifiers to FullContact Tags Get API.

        :param headers: additional_headers to be passed.
        Authorization and Content-Type are added automatically.
        :param identifiers: Identifiers to be used to find the tags.

        :return: requests.Response wrapped in _get_response
        """
        return self._validate_and_post_to_api(
            self._get_request,
            self._get_response,
            self._get_endpoint,
            identifiers,
            headers
        )

    def create(self,
               recordId: str,
               tags: dict,
               headers: dict = None) -> _create_response:
        r"""
        POST tags and recordId to FullContact Tags Create API.

        :param recordId: Existing recordId to which the tags should be added.
        :param tags: A dictionary of tags in format:
            {key: [value1, value2, ...]}
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _create_response
        """
        return self._validate_and_post_to_api(
            self._create_request,
            self._create_response,
            self._create_endpoint,
            dict(recordId=recordId, tags=self._tags_dict_to_list(tags)),
            headers
        )

    def delete(self,
               recordId: str,
               tags: dict,
               headers: dict = None) -> _delete_response:
        r"""
        POST tags and recordId to FullContact Tags Delete API.

        :param recordId: Existing recordId from which
        the tags should be deleted.
        :param tags: A dictionary of tags in format:
            {key: [value1, value2, ...]}
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: requests.Response wrapped in _delete_response
        """
        return self._validate_and_post_to_api(
            self._delete_request,
            self._delete_response,
            self._delete_endpoint,
            dict(recordId=recordId, tags=self._tags_dict_to_list(tags)),
            headers
        )

    def get_async(self, headers: dict = None, **identifiers) -> Future:
        r"""
        POST identifiers to FullContact Tags Get API asynchronously.

        :param headers: additional_headers to be passed.
        Authorization and Content-Type are added automatically.
        :param identifiers: Identifiers to be used to find the tags.

        :return: Future object. result() will return a requests.Response
        wrapped in _get_response
        """
        return self.config.get_executor().submit(
            self.get,
            headers,
            **identifiers
        )

    def create_async(self,
                     recordId: str,
                     tags: dict,
                     headers: dict = None) -> Future:
        r"""
        POST tags and recordId to FullContact Tags Create API asynchronously.

        :param recordId: Existing recordId to which the tags should be added.
        :param tags: A dictionary of tags in format:
            {key: [value1, value2, ...]}
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _create_response
        """
        return self.config.get_executor().submit(
            self.create,
            recordId,
            tags,
            headers
        )

    def delete_async(self,
                     recordId: str,
                     tags: dict,
                     headers: dict = None) -> Future:
        r"""
        POST tags and recordId to FullContact Tags Delete API asynchronously.

        :param recordId: Existing recordId from which
        the tags should be deleted.
        :param tags: A dictionary of tags in format:
            {key: [value1, value2, ...]}
        :param headers: Additional_headers to be passed.
        Authorization and Content-Type are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _delete_response
        """
        return self.config.get_executor().submit(
            self.delete,
            recordId,
            tags,
            headers
        )
