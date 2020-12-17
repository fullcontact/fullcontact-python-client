from typing import List

from .api.company_api import CompanyApi as _CompanyApi
from .api.person_api import PersonApi as _PersonApi
from .api.resolve_api import ResolveApi as _ResolveApi
from .api.tags_api import TagsApi as _TagsApi
from .api.audience_api import AudienceApi as _AudienceApi
from .api.verification_api import VerificationApi as _EmailVerificationApi
from .config.client_config import ClientConfig as _ClientConfig


class FullContactClient(object):
    r"""
    Wrapper class with individual clients initialized
    as member variables. This is to help the users
    use all the clients with a single initialization.
    """

    def __init__(self,
                 api_key: str,
                 headers: dict = None,
                 max_retry_count: int = _ClientConfig.MAX_RETRY_ATTEMPTS,
                 retry_status_codes: List[int] = _ClientConfig.DEFAULT_RETRY_STATUS_CODES,
                 base_delay: float = _ClientConfig.DEFAULT_RETRY_DELAY
                 ):
        r"""
        Initialize the config object.

        :param api_key: Used for Authorization
        :param headers: additional_headers to be passed. Authorization and Content-Type
        are added if not provided.
        :param max_retry_count: The maximum number of retries to be attempted,
        in case of the provided retry_status_codes. The value is capped at 5.
        :param retry_status_codes: The list of status codes for which retry
        should be attempted.
        :param base_delay: The base delay/backoff factor for exponential backoff.
        """
        client_config = _ClientConfig(api_key,
                                      max_retry_count,
                                      retry_status_codes,
                                      base_delay)
        self.person = _PersonApi(client_config, headers)
        self.company = _CompanyApi(client_config, headers)
        self.identity = _ResolveApi(client_config, headers)
        self.tags = _TagsApi(client_config, headers)
        self.audience = _AudienceApi(client_config, headers)
        self.verification = _EmailVerificationApi(client_config, headers)
