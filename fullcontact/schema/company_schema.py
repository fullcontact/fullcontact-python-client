# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Company Enrich API requests.
"""

from .base.schema_base import BaseRequestSchema


class CompanyEnrichRequestSchema(BaseRequestSchema):
    schema_name = "Company Enrich"

    domain: str
    webhookUrl: str

    required_fields = ("domain",)
