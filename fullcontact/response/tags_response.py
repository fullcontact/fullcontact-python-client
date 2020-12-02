# -*- coding: utf-8 -*-

"""
This module serves the class for wrapping
FullContact Tags Get, Create and Delete
API Responses.
"""

from .base.base import BaseApiResponse
from .base.tags_base import BaseTagsResponse


class TagsGetResponse(BaseTagsResponse):
    def get_recordId(self) -> str:
        return self.json().get("recordId", None)

    def get_partnerId(self) -> str:
        return self.json().get("partnerId", None)


class TagsCreateResponse(BaseApiResponse):
    pass


class TagsDeleteResponse(BaseApiResponse):
    pass
