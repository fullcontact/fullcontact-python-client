# -*- coding: utf-8 -*-

"""
This module serves the class for wrapping
FullContact Person Enrich API Response.
"""

from .base.enrich_base import BaseEnrichResponse


class PersonEnrichResponse(BaseEnrichResponse):
    # An or is used in all the functions below
    # to return default values,
    # as the API could return None/null values

    def get_name(self) -> dict:
        return self.get_details().get("name", None) or {}

    def get_age(self) -> dict:
        return self.get_details().get("age", None) or {}

    def get_gender(self) -> str:
        return self.get_details().get("gender", None) or ""

    def get_demographics(self) -> dict:
        return self.get_details().get("demographics", None) or {}

    def get_emails(self) -> list:
        return self.get_details().get("emails", None) or []

    def get_phones(self) -> list:
        return self.get_details().get("phones", None) or []

    def get_profiles(self) -> list:
        return self.get_details().get("profiles", None) or []

    def get_locations(self) -> list:
        return self.get_details().get("locations", None) or []

    def get_employment(self) -> list:
        return self.get_details().get("employment", None) or []

    def get_photos(self) -> list:
        return self.get_details().get("photos", None) or []

    def get_education(self) -> list:
        return self.get_details().get("education", None) or []

    def get_urls(self) -> list:
        return self.get_details().get("urls", None) or []

    def get_interests(self) -> list:
        return self.get_details().get("interests", None) or []

    def get_household(self) -> dict:
        return self.get_details().get("household", None) or {}

    def get_finance(self) -> dict:
        return self.get_details().get("finance", None) or {}

    def get_census(self) -> dict:
        return self.get_details().get("census", None) or {}

    def get_identifiers(self) -> dict:
        return self.get_details().get("identifiers", None) or {}
