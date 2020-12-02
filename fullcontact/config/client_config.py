# -*- coding: utf-8 -*-

"""
This module serves the class for setting
FullContact Client configuration, that can be
used while making API requests.
"""

from concurrent.futures.thread import ThreadPoolExecutor
from typing import List

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from fullcontact.exceptions import FullContactException


class ClientConfig(object):
    r"""
    Class that provides the client configuration to be
    used with the BaseApi subclass.
    """
    MAX_RETRY_ATTEMPTS = 5

    DEFAULT_RETRY_ATTEMPTS = 1
    DEFAULT_RETRY_DELAY = 1.0
    DEFAULT_RETRY_STATUS_CODES = (429, 503)

    def __init__(self,
                 api_key: str,
                 retry_attempts: int = DEFAULT_RETRY_ATTEMPTS,
                 retry_status_codes: List[int] = DEFAULT_RETRY_STATUS_CODES,
                 retry_delay: float = DEFAULT_RETRY_DELAY
                 ):
        r"""
        Initialize the config object.

        :param api_key: Used for Authorization
        :param retry_attempts: The maximum number of retries to be attempted,
        in case of the provided retry_status_codes. The value is capped at 5.
        :param retry_status_codes: The list of status codes for which retry
        should be attempted.
        :param retry_delay: The base delay/backoff factor for exponential backoff.
        """
        if api_key is not None and type(api_key) != str:
            raise TypeError("Parameter 'api_key' should be of type 'str'")
        if api_key is None or api_key.strip() == "":
            raise FullContactException("Invalid/Empty API Key provided.")

        self.__api_key = api_key
        self.__http_session = self._build_http_session(
            retry_attempts,
            retry_status_codes,
            retry_delay
        )
        self.__executor = ThreadPoolExecutor()

    def _build_http_session(self,
                            retry_attempts: int,
                            retry_status_codes: List[int],
                            retry_delay: float) -> Session:

        r"""
        Build the HTTP Session with a retry strategy using an HTTP Adapter.

        :param retry_attempts: The maximum number of retries to be attempted,
        in case of the provided retry_status_codes. The value is capped at 5.
        :param retry_status_codes: The list of status codes for which retry
        should be attempted.
        :param retry_delay: The base delay/backoff factor for exponential backoff.
        """
        max_retry_attempts = retry_attempts \
            if retry_attempts < self.MAX_RETRY_ATTEMPTS \
            else self.MAX_RETRY_ATTEMPTS

        retry = Retry(
            total=2 * self.MAX_RETRY_ATTEMPTS,
            read=False,
            status=max_retry_attempts,
            status_forcelist=retry_status_codes,
            backoff_factor=retry_delay
        )
        http_adapter = HTTPAdapter(max_retries=retry)
        http_session = Session()
        http_session.mount("https://", http_adapter)
        return http_session

    def get_http_session(self) -> Session:
        return self.__http_session

    def get_executor(self) -> ThreadPoolExecutor:
        return self.__executor

    def get_api_key(self) -> str:
        return self.__api_key
