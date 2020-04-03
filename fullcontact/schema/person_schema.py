from typing import List

from .base.schema_base import BaseSchema, BaseCombinationSchema
from ..exceptions import FullContactException


class LocationSchema(BaseCombinationSchema):
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


class NameSchema(BaseCombinationSchema):
    schema_name = "Name"

    full: str
    given: str
    family: str

    field_combinations = (
        ("given", "family"),
        ("full",)
    )


class ProfileSchema(BaseCombinationSchema):
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


class PersonSchema(BaseSchema):
    schema_name = "Person"

    email: str
    emails: List[str]
    phone: str
    phones: List[str]
    location: LocationSchema
    name: NameSchema
    profiles: List[ProfileSchema]
    maids: List[str]
    webhookUrl: str
    confidence: str
    dataFilter: List[str]
    infer: bool

    queryable_fields = ("email", "emails", "phone", "phones", "location", "name", "profiles", "maids")

    def validate(self, data: dict) -> dict:
        r"""
        Validate the input data
        :param data: dict data to be validated
        :return: validated data
        Validation will be done using the base class method. In addition,
        a check for the minumum combination for location and name
        would be checked
        """
        validated_data = super().validate(data)

        is_location_present = validated_data.get('location', None) is not None

        is_name_present = validated_data.get('name', None) is not None

        if (is_location_present or is_name_present) and \
                not (is_location_present and is_name_present):
            raise FullContactException("Location and Name have to be queried together")

        return validated_data
