# -*- coding: utf-8 -*-

"""
This module serves the base class for all
FullContact API request classes.
"""
from abc import ABCMeta
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep

import requests

from ...exceptions import FullContactException


class ApiBase(object, metaclass=ABCMeta):
    """
    This class acts as the abstract base for all FullContact API Enrich
    subclasses. All the functions and attributes common to all
    FullContact API subclasses should be defined here.
    """
    _BASE_URL = "https://api.fullcontact.com/v3/"
    _DEFAULT_RETRY_COUNT = 1
    _MAX_RETRY_COUNT = 5
    _DEFAULT_DELAY = 1
    _EXPONENTIAL_WAIT_MULTIPLIER = 2
    _RETRY_STATUS_CODES = (429, 503)

    def __init__(self, api_key: str = None):
        r"""
        Initialize the search object with an API Key.

        :param api_key: Used for Authorization
        """
        if api_key is None or api_key.strip() == "":
            raise FullContactException("Invalid/Empty API Key provided.")
        self._api_key = api_key
        self._executor = ThreadPoolExecutor()

    def _exponential_wait(self,
                          base_delay: int = _DEFAULT_DELAY,
                          failure_count: int = _DEFAULT_RETRY_COUNT
                          ):
        r"""
        Exponential back-off wait
        :param base_delay: base delay
        :param failure_count: Failure count, used as the exponent/power
        """
        sleep_time = base_delay * self._EXPONENTIAL_WAIT_MULTIPLIER ^ failure_count
        sleep(sleep_time)

    def _get_from_api(self,
                      url: str = None,
                      headers: dict = None,
                      data: dict = None,
                      delay: int = _DEFAULT_DELAY,
                      max_retries: int = _DEFAULT_RETRY_COUNT,
                      failure_count: int = 0
                      ) -> requests.Response:
        r"""
        Send POST request to API based on parameters
        :param url: url to POST request to
        :param headers: headers to be passed. Authorization and Content-Type
        are added if not provided.
        :param data: body of the request to be sent
        :param delay: base delay for exponential back-off
        :param max_retries: maximum number of retries
        :param failure_count: number of failures occurred so far,
        used for exponential back-off
        :return: Response object

        Method type is always POST for the requests.
        """
        headers = headers or {}
        data = data or {}

        if max_retries > self._MAX_RETRY_COUNT:
            max_retries = self._MAX_RETRY_COUNT

        if failure_count > 0:
            self._exponential_wait(
                base_delay=delay,
                failure_count=failure_count
            )

        if "Authorization" not in headers:
            headers["Authorization"] = "Bearer %s" % self._api_key
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        response = requests.post(url=url, json=data, headers=headers)

        if response.status_code in self._RETRY_STATUS_CODES and failure_count < max_retries:
            response = self._get_from_api(
                url=url,
                headers=headers,
                max_retries=max_retries,
                failure_count=failure_count + 1
            )

        return response
