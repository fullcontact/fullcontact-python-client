# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Identity Map, Resolve and Delete API requests.
"""
from .base.schema_base import BaseSchema
from .person_schema import PersonSummarySchema
from ..exceptions import FullContactException


class IdentityMapSchema(PersonSummarySchema):
    schema_name = "Identity Map"


class IdentityResolveSchema(PersonSummarySchema):
    schema_name = "Identity Resolve"

    personId: str

    queryable_fields = PersonSummarySchema.queryable_fields + ("recordId", "personId",)

    def validate(self, data: dict) -> dict:
        validated_data = super(IdentityResolveSchema, self).validate(data)
        if "personId" in validated_data and "recordId" in validated_data:
            raise FullContactException("Both recordId and personId are provided, please provide only one.")

        return validated_data


class IdentityDeleteSchema(BaseSchema):
    schema_name = "Identity Delete"

    recordId: str

    required_fields = ("recordId",)
