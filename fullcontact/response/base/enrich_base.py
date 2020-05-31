# -*- coding: utf-8 -*-

"""
This module serves the base class for wrapping
FullContact Company Enrich response.
"""

from .base import BaseApiResponse


class BaseEnrichResponse(BaseApiResponse):

    def __init__(self, response):
        super().__init__(response)
        self.__set_summary()
        self.__set_details()

    def __set_summary(self):
        if self.is_successful is False:
            self.__summary = {}
        else:
            raw_data = self.json()
            self.__summary = {
                key: raw_data.get(key, None)
                for key in raw_data
                if key != "details"
            }

    def __set_details(self):
        if self.is_successful is False:
            self.__details = {}
        else:
            # Using or to assign default value as the API
            # sometimes sends None/null values
            self.__details = self.json().get("details", None) or {}

    def get_summary(self) -> dict:
        r"""
        :return: Summary from response JSON
        """
        return self.__summary

    def get_details(self) -> dict:
        r"""
        :return: Details from response JSON
        """
        return self.__details
