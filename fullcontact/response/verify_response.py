# -*- coding: utf-8 -*-

"""
This module serves the class for wrapping
FullContact Verify Match, Activity and Signals
API Responses.
"""

from .base.base import BaseApiResponse


class VerifyActivityResponse(BaseApiResponse):
    def get_emails(self): return self.json().get("emails", None) or None


class VerifyMatchResponse(BaseApiResponse):
    def get_city(self): return self.json().get("city", None) or None
    def get_region(self): return self.json().get("region", None) or None
    def get_country(self): return self.json().get("country", None) or None
    def get_continent(self): return self.json().get("continent", None) or None
    def get_postalCode(self): return self.json().get("postalCode", None) or None
    def get_familyName(self): return self.json().get("familyName", None) or None
    def get_givenName(self): return self.json().get("familyName", None) or None
    def get_phone(self): return self.json().get("phone", None) or None
    def get_maid(self): return self.json().get("maid", None) or None
    def get_email(self): return self.json().get("email", None) or None
    def get_social(self): return self.json().get("social", None) or None
    def get_nonId(self): return self.json().get("nonId", None) or None


class VerifySignalResponse(BaseApiResponse):
    def get_emails(self): return self.json().get("emails", None) or None
    def get_name(self): return self.json().get("name", None) or None
    def get_personIds(self): return self.json().get("personIds", None) or None
    def get_phones(self): return self.json().get("phones", None) or None
    def get_maids(self): return self.json().get("maids", None) or None
    def get_nonIds(self): return self.json().get("nonIds", None) or None
    def get_panoIds(self): return self.json().get("panoIds", None) or None
    def get_ipAddresses(self): return self.json().get("ipAddresses", None) or None
    def get_socialProfiles(self): return self.json().get("socialProfiles", None) or None
    def get_demographics(self): return self.json().get("demographics", None) or None
    def get_employment(self): return self.json().get("employment", None) or None
    def get_locations(self): return self.json().get("locations", None) or None
