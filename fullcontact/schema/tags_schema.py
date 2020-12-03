# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Tags Get, Create and Delete API requests.
"""

from typing import List

from .base.schema_base import BaseRequestSchema


class TagRequestSchema(BaseRequestSchema):
    schema_name = "Tag"

    key: str
    value: str

    required_fields = ("key", "value")


class TagsGetRequestSchema(BaseRequestSchema):
    schema_name = "Tags Get"

    recordId: str
    partnerId: str

    queryable_fields = ("recordId", "partnerId")
    

class TagsCreateRequestSchema(BaseRequestSchema):
    schema_name = "Tags Create"

    recordId: str
    tags: List[TagRequestSchema]

    required_fields = ("recordId", "tags")


class TagsDeleteRequestSchema(TagsCreateRequestSchema):
    schema_name = "Tags Delete"
