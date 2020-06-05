# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Identity Map, Resolve and Delete API requests.
"""
from .base.schema_base import BaseSchema
from .person_schema import MultiFieldRequestSchema
from ..exceptions import FullContactException


class IdentityMapRequestSchema(MultiFieldRequestSchema):
    schema_name = "Identity Map"


class IdentityResolveRequestSchema(MultiFieldRequestSchema):
    schema_name = "Identity Resolve"

    personId: str

    queryable_fields = MultiFieldRequestSchema.queryable_fields + ("recordId", "personId",)

    def validate(self, data: dict) -> dict:
        validated_data = super(IdentityResolveRequestSchema, self).validate(data)
        if "personId" in validated_data and "recordId" in validated_data:
            raise FullContactException("Both recordId and personId are provided, please provide only one.")

        return validated_data


class IdentityDeleteRequestSchema(BaseSchema):
    schema_name = "Identity Delete"

    recordId: str

    required_fields = ("recordId",)
