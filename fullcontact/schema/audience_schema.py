# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Audience Create and Download API requests.
"""

from typing import List

from .base.schema_base import BaseSchema
from .tags_schema import TagRequestSchema


class AudienceCreateRequestSchema(BaseSchema):
    schema_name = "Audience Create"

    webhookUrl: str
    tags: List[TagRequestSchema]

    required_fields = ("webhookUrl", "tags")


class AudienceDownloadRequestSchema(BaseSchema):
    schema_name = "Audience Download"

    requestId: str

    required_fields = ("requestId",)
