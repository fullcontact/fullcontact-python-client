"""
This module serves the class for wrapping
FullContact Permission Create, Delete,
Find, Current, Verify API Responses.
"""

from .base.base import BaseApiResponse


class PermissionCreateResponse(BaseApiResponse):
    pass


class PermissionDeleteResponse(BaseApiResponse):
    pass


class PermissionFindResponse(BaseApiResponse):
    pass


class PermissionCurrentResponse(BaseApiResponse):
    def get_consent_for_purposeId(self, purposeId: int):
        return self.json().get(purposeId, None) or {}


class PermissionVerifyResponse(BaseApiResponse):
    pass
