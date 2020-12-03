# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Company Enrich and Search API requests.
"""

from .base.schema_base import BaseRequestSchema


class CompanyEnrichRequestSchema(BaseRequestSchema):
    schema_name = "Company Enrich"

    domain: str
    webhookUrl: str

    required_fields = ("domain",)


class CompanySearchRequestSchema(BaseRequestSchema):
    schema_name = "Company Search"

    companyName: str
    sort: str
    location: str
    locality: str
    region: str
    country: str
    webhookUrl: str

    required_fields = ("companyName",)
