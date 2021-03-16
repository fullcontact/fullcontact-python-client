"""
This module serves the  class for validating
FullContact Permission APIs requests.
"""

from typing import List

from .base.schema_base import BaseRequestSchema
from .person_schema import MultiFieldRequestSchema


class PurposeRequestSchema(BaseRequestSchema):
    schema_name = "Purpose Request"

    purposeId: int
    channel: List[str]
    ttl: int
    enabled: bool

    required_fields = ("purposeId", "enabled")


class PermissionRequestSchema(BaseRequestSchema):
    schema_name = "Permission Request"

    consentPurposes: List[PurposeRequestSchema]
    locale: str
    ipAddress: str
    language: str
    collectionMethod: str
    collectionLocation: str
    policyUrl: str
    termsService: str
    tcf: str
    timestamp: int

    required_fields = ("consentPurposes", "policyUrl", "termsService", "collectionMethod", "collectionLocation")


class PermissionCreateRequestSchema(PermissionRequestSchema):
    schema_name = "Permission Create"

    query: MultiFieldRequestSchema

    required_fields = PermissionRequestSchema.required_fields + ("query",)


class PermissionDeleteRequestSchema(MultiFieldRequestSchema):
    schema_name = "Permission Delete"


class PermissionFindRequestSchema(MultiFieldRequestSchema):
    schema_name = "Permission Find"


class PermissionCurrentRequestSchema(MultiFieldRequestSchema):
    schema_name = "Permission Current"


class PermissionVerifyRequestSchema(BaseRequestSchema):
    schema_name = "Permission Verify"

    query: MultiFieldRequestSchema
    purposeId: int
    channel: str

    required_fields = ("purposeId", "channel", "query")
