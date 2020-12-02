# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Audience create and download
API requests.
"""
from concurrent.futures import Future

from .base.tags_base_api import TagsBaseApi
from ..response.audience_response import AudienceCreateResponse, AudienceDownloadResponse
from ..schema.audience_schema import AudienceCreateRequestSchema, AudienceDownloadRequestSchema


class AudienceApi(TagsBaseApi):
    r"""
    Class that provides methods to perform
    Audience create and download operations.
    """
    _create_endpoint = "audience.create"
    _download_endpoint = "audience.download"

    _create_request = AudienceCreateRequestSchema()
    _download_request = AudienceDownloadRequestSchema()

    _create_response = AudienceCreateResponse
    _download_response = AudienceDownloadResponse

    def create(self,
               webhookUrl: str,
               tags: dict,
               headers: dict = None) -> _create_response:
        r"""
        POST tags to FullContact Tags Create API.

        :param webhookUrl: Webhook to which the result should be posted
        :param tags: Tags as dict for which the audience should be created.
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _create_response
        """
        return self._validate_and_post_to_api(
            self._create_request,
            self._create_response,
            self._create_endpoint,
            dict(webhookUrl=webhookUrl, tags=self._tags_dict_to_list(tags)),
            headers
        )

    def download(self,
                 requestId: str,
                 headers: dict = None) -> _download_response:
        r"""
        Get the audience response file.

        :param requestId: The requestId received on audience.create
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _download_response
        """
        return self._validate_and_get_from_api(
            self._download_request,
            self._download_response,
            self._download_endpoint,
            dict(requestId=requestId),
            headers
        )

    def create_async(self,
                     webhookUrl: str,
                     tags: dict,
                     headers: dict = None) -> Future:
        r"""
        POST tags to FullContact Tags Create API asynchronously.

        :param webhookUrl: Webhook to which the result should be posted
        :param tags: Tags as dict for which the audience should be created.
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _create_response
        """
        return self.config.get_executor().submit(
            self.create,
            webhookUrl,
            tags,
            headers
        )

    def download_async(self,
                       requestId: str,
                       headers: dict = None) -> Future:
        r"""
        Get the audience response file asynchronously.

        :param requestId: The requestId received on audience.create
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _download_response
        """
        return self.config.get_executor().submit(
            self.download,
            requestId,
            headers
        )
