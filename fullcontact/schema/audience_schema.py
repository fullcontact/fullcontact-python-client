# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Audience Create and Download API requests.
"""

from typing import List

from .base.schema_base import BaseRequestSchema
from .tags_schema import TagRequestSchema


class AudienceCreateRequestSchema(BaseRequestSchema):
    schema_name = "Audience Create"

    webhookUrl: str
    tags: List[TagRequestSchema]

    required_fields = ("webhookUrl", "tags")


class AudienceDownloadRequestSchema(BaseRequestSchema):
    schema_name = "Audience Download"

    requestId: str

    required_fields = ("requestId",)
