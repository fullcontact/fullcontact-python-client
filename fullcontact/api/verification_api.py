from concurrent.futures import Future

from .base.base_api import BaseApi
from ..response.verification_response import EmailVerificationResponse
from ..schema.verification_schema import EmailVerificationRequestSchema


class VerificationApi(BaseApi):
    _BASE_URL = "https://api.fullcontact.com/v2/"

    _email_verification_endpoint = "verification/email"
    _email_verification_request = EmailVerificationRequestSchema()
    _email_verification_response = EmailVerificationResponse

    def email(self, email: str, headers: dict = None) -> _email_verification_response:
        r"""
        Send a GET request to FullContact email verification API with the email

        :param email: The email to be verified
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: requests.Response wrapped in _email_verification_response
        """
        return self._validate_and_get_from_api(
            self._email_verification_request,
            self._email_verification_response,
            self._email_verification_endpoint,
            {
                "email": email
            },
            headers
        )

    def email_async(self, email: str, headers: dict = None) -> Future:
        r"""
        Send a GET request to FullContact email verification API with the email asynchronously

        :param email: The email to be verified
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added automatically.

        :return: Future object. result() will return a requests.Response
        wrapped in _email_verification_response
        """
        return self.config.get_executor().submit(
            self.email,
            email,
            headers
        )
