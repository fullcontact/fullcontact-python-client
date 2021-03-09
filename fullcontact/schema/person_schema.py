# -*- coding: utf-8 -*-

"""
This module serves the  class for validating
FullContact Person Enrich API requests.
"""

from typing import List

from .base.schema_base import BaseRequestSchema, BaseCombinationRequestSchema
from ..exceptions import FullContactException


class LocationRequestSchema(BaseCombinationRequestSchema):
    schema_name = "Location"

    addressLine1: str
    addressLine2: str
    city: str
    region: str
    regionCode: str
    postalCode: str

    field_combinations = (
        ("addressLine1", "city", "region"),
        ("addressLine1", "city", "regionCode"),
        ("addressLine1", "postalCode")
    )


class NameRequestSchema(BaseCombinationRequestSchema):
    schema_name = "Name"

    full: str
    given: str
    family: str

    field_combinations = (
        ("given", "family"),
        ("full",)
    )


class ProfileRequestSchema(BaseCombinationRequestSchema):
    schema_name = "Profile"

    service: str
    username: str
    userid: str
    url: str

    field_combinations = (
        ("service", "username"),
        ("service", "userid"),
        ("url",)
    )


class MultiFieldRequestSchema(BaseRequestSchema):
    schema_name = "Multi Field"
    email: str
    emails: List[str]
    phone: str
    phones: List[str]
    location: LocationRequestSchema
    name: NameRequestSchema
    profiles: List[ProfileRequestSchema]
    maids: List[str]
    recordId: str
    li_nonid: str
    partnerId: str
    recordId: str
    personId: str

    queryable_fields = ("email", "emails",
                        "phone", "phones",
                        "location", "name",
                        "profiles", "maids",
                        "li_nonid", "partnerId",
                        "recordId", "personId")

    def validate(self, data: dict) -> dict:
        r"""
        Validate the input data.

        :param data: dict data to be validated
        :return: validated data
        Validation will be done using the base class method. In addition,
        a check for the minimum combination for location and name
        would be checked
        """
        validated_data = super(MultiFieldRequestSchema, self).validate(data)

        single_queryable_fields = set(self.queryable_fields).difference(["name", "location"])

        is_location_present = validated_data.get('location', None) is not None

        is_name_present = validated_data.get('name', None) is not None

        if not self._is_single_queryable(single_queryable_fields, validated_data) and \
                (is_location_present or is_name_present) and \
                not (is_location_present and is_name_present):
            raise FullContactException("Location and Name have to be queried together")

        return validated_data


class PersonRequestSchema(MultiFieldRequestSchema):
    schema_name = "Person"

    webhookUrl: str
    confidence: str
    dataFilter: List[str]
    infer: bool
