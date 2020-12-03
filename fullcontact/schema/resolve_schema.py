# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Identity Map, Resolve and Delete API requests.
"""
from typing import List

from .base.schema_base import BaseRequestSchema
from .person_schema import MultiFieldRequestSchema
from .tags_schema import TagRequestSchema
from ..exceptions import FullContactException


class IdentityMapRequestSchema(MultiFieldRequestSchema):
    schema_name = "Identity Map"
    tags: List[TagRequestSchema]


class IdentityResolveRequestSchema(MultiFieldRequestSchema):
    schema_name = "Identity Resolve"

    personId: str

    queryable_fields = MultiFieldRequestSchema.queryable_fields + ("recordId", "personId",)

    def validate(self, data: dict) -> dict:
        validated_data = super(IdentityResolveRequestSchema, self).validate(data)
        if "personId" in validated_data and "recordId" in validated_data:
            raise FullContactException("Both recordId and personId are provided, please provide only one.")

        return validated_data


class IdentityDeleteRequestSchema(BaseRequestSchema):
    schema_name = "Identity Delete"

    recordId: str

    required_fields = ("recordId",)
