from .base.schema_base import BaseRequestSchema


class EmailVerificationRequestSchema(BaseRequestSchema):
    schema_name = "Email Verification"
    email: str

    required_fields = ("email",)
