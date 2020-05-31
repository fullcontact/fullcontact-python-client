# -*- coding: utf-8 -*-

"""
This module serves the class for wrapping
FullContact Identity Map, Resolve and Delete
API Responses.
"""

from .base.base import BaseApiResponse


class IdentityMapResponse(BaseApiResponse):
    def get_recordIds(self):
        return self.json().get("recordIds", None) or []


class IdentityResolveResponse(IdentityMapResponse):
    def get_personIds(self):
        return self.json().get("personIds", None) or []


class IdentityDeleteResponse(BaseApiResponse):
    pass
