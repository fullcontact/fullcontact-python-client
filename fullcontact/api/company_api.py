# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Company Enrich
API requests.
"""

from .base.enrich_base_api import EnrichBaseApi
from ..response.company_response import CompanyEnrichResponse
from ..schema.company_schema import CompanyEnrichRequestSchema


class CompanyApi(EnrichBaseApi):
    r"""
    Class that provides methods to perform
    Company Enrich operations.
    """
    _enrich_endpoint = "company.enrich"
    _enrich_request = CompanyEnrichRequestSchema()
    _enrich_response = CompanyEnrichResponse
