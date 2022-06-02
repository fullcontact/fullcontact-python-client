# -*- coding: utf-8 -*-

"""
This module serves the class for validating
FullContact Verification API requests.
"""

from .person_schema import MultiFieldRequestSchema


class VerifyRequestSchema(MultiFieldRequestSchema):
    schema_name = "Verify"
