from typing import Union

from requests import Response


class BaseApiResponse(object):
    SUCCESSFUL_STATUS_CODES = (200, 202, 404)

    def __init__(self, response):
        self.response = response
        self.__set_response_json(response)

    @property
    def is_successful(self) -> bool:
        if self.response is not None and self.response.status_code is not \
                None and self.response.status_code in \
                self.SUCCESSFUL_STATUS_CODES:
            return True
        return False

    def __set_response_json(self, response: Response):
        self.__response_json = response.json() or {}

    def get_status_code(self) -> int:
        r"""
        :return: Status code of the response
        """
        return self.response.status_code or None

    def raw(self) -> Union[dict, list]:
        r"""
        :return: JSON representation of the API response content
        """
        return self.__response_json

    def get_message(self) -> str:
        r"""
        :return: Response error message if unsuccessful
        """
        if type(self.__response_json) == dict and self.__response_json.get(
                "message", None) is not None:
            return self.__response_json.get("message")
        return self.response.reason or "Error"

    def get_headers(self) -> dict:
        r"""
        :return: Response headers
        """
        return self.response.headers or {}
