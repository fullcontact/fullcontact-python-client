from .base.schema_base import BaseSchema


class CompanyEnrichSchema(BaseSchema):
    schema_name = "Company Enrich"

    domain: str
    webhookUrl: str

    required_fields = ("domain",)


class CompanySearchSchema(BaseSchema):
    schema_name = "Company Search"

    companyName: str
    sort: str
    location: str
    locality: str
    region: str
    country: str
    webhookUrl: str

    required_fields = ("companyName",)
