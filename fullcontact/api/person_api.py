# -*- coding: utf-8 -*-

"""
This module serves the class for making
FullContact Person Enrich API requests.
"""

from .base.enrich_base_api import EnrichBaseApi
from ..response.person_response import PersonEnrichResponse
from ..schema.person_schema import PersonRequestSchema


class PersonApi(EnrichBaseApi):
    r"""
    Class that provides methods to perform
    Person Enrich operations, with MultiField Capabilities.
    """
    _enrich_endpoint = "person.enrich"
    _enrich_request = PersonRequestSchema()
    _enrich_response = PersonEnrichResponse
