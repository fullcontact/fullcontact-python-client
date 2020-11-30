# -*- coding: utf-8 -*-

"""
This module serves the class for wrapping
FullContact Identity Map, Resolve and Delete
API Responses.
"""

from .base.base import BaseApiResponse
from .base.tags_base import BaseTagsResponse


class IdentityMapResponse(BaseApiResponse):
    def get_recordIds(self):
        return self.json().get("recordIds", None) or []


class IdentityResolveResponse(IdentityMapResponse, BaseTagsResponse):
    def get_personIds(self):
        return self.json().get("personIds", None) or []

    def get_partnerIds(self):
        return self.json().get("partnerIds", None) or []


class IdentityDeleteResponse(BaseApiResponse):
    pass
