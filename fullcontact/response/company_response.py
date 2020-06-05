# -*- coding: utf-8 -*-

"""
This module serves the class for wrapping
FullContact Company Enrich and Search
API Responses.
"""

from .base.base import BaseApiResponse
from .base.enrich_base import BaseEnrichResponse


class CompanyEnrichResponse(BaseEnrichResponse):
    pass


class CompanySearchResponse(BaseApiResponse):
    pass
