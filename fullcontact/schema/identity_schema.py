# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Identity Map, Resolve and Delete API requests.
"""

from .person_schema import PersonSummarySchema


class IdentityMapSchema(PersonSummarySchema):
    schema_name = "Identity Map"


class IdentityResolveSchema(PersonSummarySchema):
    schema_name = "Identity Resolve"

    personId: str

    queryable_fields = PersonSummarySchema.queryable_fields + ("personId",)


class IdentityDeleteSchema(PersonSummarySchema):
    schema_name = "Identity Delete"

    recordId: str

    required_fields = ("recordId",)
