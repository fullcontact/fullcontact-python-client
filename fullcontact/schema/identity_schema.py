# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Identity Map, Resolve and Delete API requests.
"""

from typing import List

from .base.schema_base import BaseSchema
from .person_schema import PersonSummarySchema
from ..exceptions import FullContactException


class IdentityMapSchema(PersonSummarySchema):
    schema_name = "Identity Map"


class IdentityResolveSchema(PersonSummarySchema):
    schema_name = "Identity Resolve"

    personId: str

    required_fields = PersonSummarySchema.queryable_fields + ("personId",)
