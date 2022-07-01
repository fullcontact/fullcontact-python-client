# FullContact Client

[![PyPI](https://img.shields.io/pypi/v/python-fullcontact?label=PyPi)](https://pypi.org/project/python-fullcontact/)
![flake8](https://github.com/fullcontact/fullcontact-python-client/workflows/flake8/badge.svg)
![pytest](https://github.com/fullcontact/fullcontact-python-client/workflows/pytest/badge.svg)

The official python client library for FullContact V3 API. This client provides an interface to interact with Enrich,
Resolve, Tags, Audience, Verify and Permission APIs. FullContact API Documentation is available
at: https://platform.fullcontact.com/docs

# Table of contents

* [Requirements](#requirements)
* [Adding To Your Project](#adding-to-your-project)
* [Installation](#installation)
* [Migrating from FullContact Client V1.0.0](#migrating-from-fullcontact-client-v100)
* [Usage](#usage)
    * [Importing the client](#importing-the-client)
    * [Basic Usage](#basic-usage)
    * [Client Configuration](#client-configuration)
    * [Person API](#person-api)
        * [enrich()](#fullcontactclientpersonenrich)
        * [enrich_async()](#fullcontactclientpersonenrich_async)
    * [Company API](#company-api)
        * [enrich()](#fullcontactclientcompanyenrich)
        * [enrich_async](#fullcontactclientcompanyenrich_async)
    * [Resolve API](#resolve-api)
        * [map()](#fullcontactclientidentitymap)
        * [map_async()](#fullcontactclientidentitymap_async)
        * [resolve()](#fullcontactclientidentityresolve)
        * [resolve_async()](#fullcontactclientidentityresolve_async)
        * [mapResolve()](#fullcontactclientidentitymapresolve)
        * [mapResolve_async()](#fullcontactclientidentitymapresolve_async)
        * [delete()](#fullcontactclientidentitydelete)
        * [delete_async()](#fullcontactclientidentitydelete_async)
    * [Tags API](#tags-api)
        * [get()](fullcontactclienttagsget)
        * [get_async()](fullcontactclienttagsget_async)
        * [create()](fullcontactclienttagscreate)
        * [create_async()](fullcontactclienttagscreate_async)
        * [delete()](fullcontactclienttagsdelete)
        * [delete_async()](fullcontactclienttagsdelete_async)
    * [Audience](#audience-api)
        * [create()](fullcontactclientaudiencecreate)
        * [create_async()](fullcontactclientaudiencecreate_async)
        * [download()](fullcontactclientaudiencedownload)
        * [download_async()](fullcontactclientaudiencedownload_async)
    * [Permission](#permission-api)
        * [create](#fullcontactclientpermissioncreate)
        * [delete](#fullcontactclientpermissiondelete)
        * [find](#fullcontactclientpermissionfind)
        * [current](#fullcontactclientpermissioncurrent)
        * [verify](#fullcontactclientpermissionverify)
        * [permission-async](#permission-apis-asynchronous-methods)
    * [Verify](#verify-api)
        * [match](#fullcontactclientverifymatch)
        * [match_async](#fullcontactclientverifymatch_async)
        * [signals](#fullcontactclientverifysignals)
        * [signals_async](#fullcontactclientverifysignals_async)
        * [activity](#fullcontactclientverifyactivity)
        * [activity_async](#fullcontactclientverifyactivity_async)

# Requirements

This library requires Python 3.5 or above.

# Adding To Your Project

To add FullContact Python Client library to your project, add the below line to your `requirements.txt` file, or as a
requirement in the `setup.py` file.

```
python-fullcontact==4.0.0
```

# Installation

It is recommended to install the FullContact python client library from [PyPi](https://pypi.org/) using the below
command.

```
pip install python-fullcontact
```

If you'd like to install the development version (with `pytest`), run instead:

```shell
pip install 'python-fullcontact[develop]'
```

It is also possible to install the package from this repo, by running the below commands.

```
pip install git+https://github.com/fullcontact/fullcontact-python-client.git
```

# Migrating from FullContact Client V1.0.0

This version of FullContact Client (V2.0.0) has significant changes in terms of design and features. Hence, it is not
backward compatible with V1.0.0 library. However, migrating from the V1.0.0 client is very easy. In V1.0.0, there used
to be different clients for different APIs (PersonClient, CompanyClient). However with V2.0.0, we have only 1 client,
with different methods.

#### V1.0.0

```python
from fullcontact import PersonClient, CompanyClient

person_client = PersonClient("<your_api_key>")
company_client = CompanyClient("<your_api_key>")
person_client.enrich(**query)
company_client.enrich(**query)
```

This would be changed as below in V2.0.0

#### V2.0.0

```python
from fullcontact import FullContactClient

fullcontact_client = FullContactClient("<your_api_key>")
fullcontact_client.person.enrich(**query)
fullcontact_client.company.enrich(**query)
```

# Usage

## Importing the client

The client is available straight out of the package `fullcontact`.

```python
from fullcontact import FullContactClient
```

## Basic Usage

To use the client library, you need to initialize the client using the API KEY that you have generated
from [FullContact Platform](https://platform.fullcontact.com/developers/api-keys). Once initialized, the client provides
the `Enrich` and `Resolve` capabilities of the V3 FullContact API.

```python
from fullcontact import FullContactClient

fullcontact_client = FullContactClient("<your_api_key>")

# Person Enrich
person_enrich_result = fullcontact_client.person.enrich(email="marquitaross006@gmail.com")

# Company Enrich
company_enrich_result = fullcontact_client.company.enrich(domain="fullcontact.com")

# Identity Map
identity_map_result = fullcontact_client.identity.map(email="marquitaross006@gmail.com", recordId="customer123")

# Identity Resolve
identity_resolve_result = fullcontact_client.identity.resolve(recordId="customer123")

# Identity Map Resolve
identity_mapResolve_result = fullcontact_client.identity.mapResolve(email="marquitaross006@gmail.com", recordId="customer123", generatePid=True)

# Identity Delete
identity_delete_result = fullcontact_client.identity.delete(recordId="customer123")

# Tags Get
tags_get_result = fullcontact_client.tags.get(recordId="customer123")

# Tags Create
tags_create_result = fullcontact_client.tags.create(recordId="customer123",
                                                    tags={"tag1": "value1", "tag2": ["value2", "value3"]})

# Tags Delete
tags_delete_result = fullcontact_client.tags.create(recordId="customer123",
                                                    tags={"tag2": "value2"})

# Audience Create
audience_create_result = fullcontact_client.audience.create(webhookUrl="http://your_webhook_url/",
                                                            tags={"tag1": "value1", "tag2": "value2"})

# Audience Download
audience_download_result = fullcontact_client.audience.download(requestId="<your_requestId>")
audience_download_result.write_to_file("<output_file_path>")

# Permission Create
permission_create_result = fullcontact_client.permission.create(
                                            query={"email": "marquitaross006@gmail.com"},
                                            consentPurposes=[
                                                {
                                                    "purposeId": 2,
                                                    "channel": ["web","phone","mobile","offline","email"],
                                                    "ttl": 1095,
                                                    "enabled": True
                                                }
                                            ],
                                            locale="US",
                                            language="en",
                                            collectionMethod="cookie",
                                            collectionLocation="US",
                                            policyUrl="https://www.fullcontact-test.com/services-privacy-policy/",
                                            termsService="https://www.fullcontact-test.com/content-policy/")  

# Permission Delete
permission_delete_result = fullcontact_client.permission.delete({"email": "marquitaross006@gmail.com"})
# Permission Find
permission_find_result = fullcontact_client.permission.find(email="marquitaross006@gmail.com")

# Permission Current
permission_current_result = fullcontact_client.permission.current(email="marquitaross006@gmail.com")

# Permission Verify
permission_verify_result = fullcontact_client.permission.verify(query={"email": "marquitaross006@gmail.com"},
                                                                purposeId=6, 
                                                                channel="web")
# Verify Match
verify_match_result = fullcontact_client.verify.match(email="marquitaross006@gmail.com")

# Verify Signals
verify_signals_result = fullcontact_client.verify.signals(email="marquitaross006@gmail.com")

# Verify Activity
verify_activity_result = fullcontact_client.verify.activity(email="marquitaross006@gmail.com")

```

## Client Configuration

The FullContact Client allows the configuration of additional headers and retry related values, through init parameters.

#### API Key

API Key is required to Authorize with FullContact API and hence, is a required parameter. This is set using
the `api_key` init parameter for [FullContactClient](#fullcontactclient).

```python
fullcontact_client = FullContactClient("<your_api_key>")
```

#### Headers

The headers `Authorization`, `Content-Type` and `User-Agent` are added automatically and cannot be overridden. Hence,
headers needs to be added only if any additional header needs to be passed to the API. One useful situation for this is
when you need to pass your `Reporting-Key`. The headers can be added by setting the `headers` init parameter
for [FullContactClient](#fullcontactclient).

```python
additional_headers = {"Reporting-Key": "clientXYZ"}
fullcontact_client = FullContactClient(api_key="<your_api_key>", headers=additional_headers)
```

#### Retry

By default, the client retries a request if it receives a `429` or `503` status code. The default retry count is 1 and
the backoff factor (base delay) for exponential backoff is 1 second. Retry can by configured by setting
the `max_retry_count`, `retry_status_codes` and `base_delay` init parameters for [FullContactClient](#fullcontactclient)
. If the value provided for `max_retry_count` is greater than 5, it will be set to 5.

```python
fullcontact_client = FullContactClient(api_key="<your_api_key>", max_retry_count=3, retry_status_codes=(429, 503, 413),
                                       base_delay=2.5)
```

### MultiFieldRequest
Ability to match on one or many input fields. The more contact data inputs you can provide, the better. 
By providing more contact inputs, the more accurate and precise we can get with our identity resolution capabilities.
* `email`: _str_
* `emails`: _List[str]_
* `phone`: _str_
* `phones`: _List[str]_
* `placekey`: _str_
* `location`: _dict_
    * `addressLine1`: _str_
    * `addressLine2`: _str_
    * `city`: _str_
    * `region`: _str_
    * `regionCode`: _str_
    * `postalCode`: _str_
* `name`: _dict_
    * `full`: _str_
    * `given`: _str_
    * `family`: _str_
* `profiles`: _List[dict]_
    * `service`: _str_
    * `username`: _str_
    * `userid`: _str_
    * `url`: _str_
* `maids`: _List[str]_
* `recordId`: _str_
* `personId`: _str_
* `li_nonid`: _str_
* `partnerId`: _str_
* `panoramaId`: _str_


### FullContactClient

class: _fullcontact.FullContactClient_

#### Init parameters:

* `api_key`: _str_ - (required)
* `headers`: _dict_ - [optional]
* `max_retry_count`: _int_ _[default=5]_ - [optional]
* `retry_status_codes`: _List[int]_ _[default=(429, 503)]_ - [optional]
* `base_delay`: _float_ _[default=1.0]_ - [optional]

## Person API

The client library provides methods to interact with V3 Person Enrich API through `FullContactClient.person` object. The
V3 Person Enrich API can be called synchronously using [enrich()](#fullcontactclientpersonenrich) and asynchronously
using [enrich_async()](#fullcontactclientpersonenrich_async). Additional headers can be set on a per-request basis by
setting the parameter `headers` while calling [enrich()](#fullcontactclientpersonenrich)
or [enrich_async()](#fullcontactclientpersonenrich_async). Being a request level parameter, this can be used to override
any header that has been set on the client level.
> Person Enrichment API Documentation: https://platform.fullcontact.com/docs/apis/enrich/multi-field-request

```python
# Synchronous execution
enrich_response = fullcontact_client.person.enrich(email="marquitaross006@gmail.com")
print(enrich_response.get_name())
# Output: {'given': 'Marquita', 'family': 'Ross', 'full': 'Marquita H Ross'}

# Asynchronous execution
enrich_async_response = fullcontact_client.person.enrich_async(email="marquitaross006@gmail.com")
enrich_result = enrich_async_response.result()
print(enrich_result.get_name())


# Output: {'given': 'Marquita', 'family': 'Ross', 'full': 'Marquita H Ross'}

# Asynchronous execution using callback
def print_name_from_result(result: concurrent.Futures.Future):
    enrich_result = result.result()
    print(enrich_result.get_name())


fullcontact_client.person.enrich_async(email="marquitaross006@gmail.com").add_done_callback(print_name_from_result)
# Output: {'given': 'Marquita', 'family': 'Ross', 'full': 'Marquita H Ross'}
```

### FullContactClient.person.enrich()

class: _fullcontact.api.person_api.PersonApi_

#### Parameters:

* `**query`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

`query` takes in [MultiFieldReq](#multifieldrequest). Other supported fields for query:

* `webhookUrl`: _str_
* `confidence`: _str_
* `dataFilter`: _List[str]_
* `infer`: _bool_
* `maxMaids`: _int_

#### Returns:

#### PersonEnrichResponse

class: _fullcontact.response.person_response.PersonEnrichResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_summary()`: _dict_ - Summary from Person Enrich Response
* `get_details()`: _dict_ - Details from Person Enrich Response
* `get_name()`: _dict_ - Name from Person Enrich Response
* `get_age()`: _dict_ - Age from Person Enrich Response
* `get_gender()`: _str_ - Gender from Person Enrich Response
* `get_demographics()`: _dict_ - Demographics from Person Enrich Response
* `get_emails()`: _List[str]_ - Emails from Person Enrich Response
* `get_phones()`: _List[str]_ - Phones from Person Enrich Response
* `get_profiles()`: _List[dict]_ - Profiles from Person Enrich Response
* `get_locations()`: _List[dict]_ - Locations from Person Enrich Response
* `get_employment()`: _List[dict]_ - Employments from Person Enrich Response
* `get_photos()`: _List[dict]_ - Photos from Person Enrich Response
* `get_education()`: _List[dict]_ - Education
* `get_urls()`: _List[dict]_ - URLs from Person Enrich Response
* `get_interests()`: _List[dict]_ - Interests from Person Enrich Response
* `get_household()`: _dict_ - Household details from Person Enrich Response
* `get_finance()`: _dict_ - Finance details from Person Enrich Response
* `get_census()`: _dict_ - Census details from Person Enrich Response
* `get_identifiers()`: _dict_ - Identifiers from Person Enrich Response
* `get_extended()`: _dict_ - All Extended data

### FullContactClient.person.enrich_async()

class: _fullcontact.api.person_api.PersonApi_
Same as that of [FullContactClient.person.enrich()](#fullcontactclientpersonenrich)

#### Returns:

#### Future[PersonEnrichResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _PersonEnrichResponse_ - [PersonEnrichResponse](#personenrichresponse) object received once execution is
  completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

## Company API

The client library provides methods to interact with V3 Company Enrich API
through `FullContactClient.company` object. The V3 Company Enrich API can be called synchronously
using [enrich()](#fullcontactclientcompanyenrich) and asynchronously
using [enrich_async()](#fullcontactclientcompanyenrich_async).
Additional headers can be set on a per-request basis by
setting the parameter `headers` while calling [enrich()](#fullcontactclientcompanyenrich))

Being a request level parameter, this can be used to override any header that has been set on the client level.
> Company Enrichment API Documentation: https://platform.fullcontact.com/docs/apis/enrich/company-enrichment

```python
# Synchronous enrich execution
enrich_response = fullcontact_client.company.enrich(domain="fullcontact.com")
print(enrich_response.get_summary())
""" Output: {'name': 'FullContact Inc',
 'location': '1755 Blake Street Suite 450 Denver CO, 80202 USA',
 'twitter': 'https://twitter.com/fullcontact',
 'linkedin': 'https://www.linkedin.com/company/fullcontact-inc-',
 'facebook': None,
 'bio': "Solving the world's contact information problem!",
 'logo': 'https://img.fullcontact.com/static/7329d91237b7970b984d56c2497c80c0_7abd96cd75e5587b39b9f15dce07d7ebe8dc31accecf1b0f2a617ada34498633',
 'website': 'https://www.fullcontact.com',
 'founded': 2010,
 'employees': 300,
 'locale': 'en',
 'category': 'Other',
 'updated': '2020-05-31'} """

# Asynchronous enrich execution
enrich_async_response = fullcontact_client.company.enrich_async(domain="fullcontact.com")
enrich_result = enrich_async_response.result()
print(enrich_result.get_summary())
```

### FullContactClient.company.enrich()

class: _fullcontact.api.company_api.CompanyApi_

#### Parameters:

* `**query`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

Supported fields for query:

* `domain`: _str_
* `webhookUrl`: _str_

#### Returns:

#### CompanyEnrichResponse

class: _fullcontact.response.company_response.CompanyEnrichResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_summary()`: _dict_ - Summary from Company Enrich Response
* `get_details()`: _dict_ - Details from Company Enrich Response

### FullContactClient.company.enrich_async()

class: _fullcontact.api.company_api.CompanyClient_

#### Parameters:

Same as that of [FullContactClient.company.enrich()](#fullcontactclientcompanyenrich)

#### Returns:

#### Future[CompanyEnrichResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _CompanyEnrichResponse_ - [CompanyEnrichResponse](#companyenrichresponse) object received once execution
  is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

## Resolve API

The client library provides methods to interact with V3 Resolve API (`identity.map`, `identity.resolve`, `identity.mapResolve`,
and `identity.delete` endpoints) through `FullContactClient.identity` object. The V3 Resolve API can be accessed using
the methods [map()](#fullcontactclientidentitymap), [resolve()](#fullcontactclientidentityresolve), [mapResolve()](#fullcontactclientidentitymapresolve),
and [delete()](#fullcontactclientidentitydelete), respectively. These APIs can be accessed using the async version these
functions, [map_async()](#fullcontactclientidentitymap_async)
, [resolve_async()](#fullcontactclientidentityresolve_async), [mapResolve_async()](#fullcontactclientidentitymapresolve_async),
and [delete_async()](#fullcontactclientidentitydelete_async). Additional headers can be set on a per-request basis by
setting the parameter `headers` while calling these methods.     
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Resolve API Documentation: https://platform.fullcontact.com/docs/apis/resolve/multi-field-request

```python
# Synchronous map execution
map_response = fullcontact_client.identity.map(email="marquitaross006@gmail.com", recordId="customer123")
print(map_response.get_recordIds())
# Output: ['customer123']

# Synchronous resolve execution
resolve_response = fullcontact_client.identity.resolve(email="marquitaross006@gmail.com")
print(resolve_response.get_recordIds())
# Output: ['customer123']

# Synchronous mapResolve execution
mapResolve_response = fullcontact_client.identity.mapResolve(email="marquitaross006@gmail.com", recordId="customer123")
print(mapResolve_response.get_recordIds())
print(mapResolve_response.get_personIds())
# Output: 
# ['customer123']
# ['OdcKOTonyt5diGjjf-CXHrn84Zr_PcPGmqj1NYSiCR_U-J7v']

# Synchronous delete execution
delete_response = fullcontact_client.identity.delete(recordId="customer123")
print(delete_response.is_successful)
# Output: True

# Asynchronous map execution
map_async_response = fullcontact_client.identity.map_async(email="marquitaross006@gmail.com", recordId="customer123")
map_response = map_async_response.result()
print(map_response.get_recordIds())
# Output: ['customer123']

# Asynchronous resolve execution
resolve_async_response = fullcontact_client.identity.resolve_async(email="marquitaross006@gmail.com")
resolve_response = resolve_async_response.result()
print(resolve_response.get_recordIds())
# Output: ['customer123']

# Asynchronous mapResolve execution
mapResolve_async_response = fullcontact_client.identity.mapResolve_async(email="marquitaross006@gmail.com", recordId="customer123")
mapResolve_response = mapResolve_async_response.result()
print(mapResolve_response.get_recordIds())
# Output: ['customer123']

# Asynchronous delete execution
delete_async_response = fullcontact_client.identity.delete_async(recordId="customer123")
delete_response = delete_async_response.result()
print(delete_response.is_successful)
# Output: True
```

### FullContactClient.identity.map()

class: _fullcontact.api.resolve_api.ResolveClient_

#### Parameters:

* `**fields`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

`fields` takes in [MultiFieldReq](#multifieldrequest). Other supported fields for mapping:

* `tags`: _List[str]_
* `generatePid`: bool

#### Returns:

#### IdentityMapResponse

class: _fullcontact.response.resolve_response.IdentityMapResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_recordIds()`: _List[str]_ - List of recordIds from Map response

### FullContactClient.identity.map_async()

class: _fullcontact.api.resolve_api.ResolveClient_

#### Parameters:

Same as that of [FullContactClient.identity.map()](#fullcontactclientidentitymap)

#### Returns:

#### Future[IdentityMapResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _IdentityMapResponse_ - [IdentityMapResponse](#identitymapresponse) object received once execution is
  completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

### FullContactClient.identity.resolve()

class: _fullcontact.api.resolve_api.ResolveApi_

#### Parameters:

* `**fields`: _kwargs_ - (required)
* `include_tags`: `_bool_ - [optional]
  > If `include_tags` is set to True, the response will include tags in the response.
* `headers`: _dict_ - [optional]

Supported fields for mapping:
Same as that of [FullContactClient.identity.map()](#fullcontactclientidentitymap), but with one more extra field

* `personId`: _str_

> Note: recordId and personId cannot be used together to resolve. Only one of these fields can be used in a request.

#### Returns:

#### IdentityResolveResponse

class: _fullcontact.response.resolve_response.IdentityResolveResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_recordIds()`: _List[str]_ - List of recordIds from Resolve response
* `get_personIds()`: _List[str]_ - List of personIds from Resolve response
* `get_partnerIds()`: _List[str]_ - List of partnerIds from Resolve response
* `get_tags()`: _Dict_ - A dict of tags, if `include_tags` was set to True in the request

### FullContactClient.identity.resolve_async()

class: _fullcontact.api.resolve_api.ResolveApi_

#### Parameters:

Same as that of [FullContactClient.identity.resolve()](#fullcontactclientidentityresolve)

#### Returns:

#### Future[IdentityResolveResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _IdentityResolveResponse_ - [IdentityResolveResponse](#identityresolveresponse) object received once
  execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.


### FullContactClient.identity.mapResolve()

class: _fullcontact.api.resolve_api.ResolveClient_

#### Parameters:

* `**fields`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

`fields` takes in [MultiFieldReq](#multifieldrequest). Other supported fields for mapping:

* `tags`: _List[str]_
* `generatePid`: bool

#### Returns:

#### IdentityResolveResponse

class: _fullcontact.response.resolve_response.IdentityResolveResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_recordIds()`: _List[str]_ - List of recordIds from Map response

### FullContactClient.identity.mapResolve_async()

class: _fullcontact.api.resolve_api.ResolveClient_

#### Parameters:

Same as that of [FullContactClient.identity.mapResolve()](#fullcontactclientidentitymapresolve)

#### Returns:

#### Future[IdentityResolveResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _IdentityResolveResponse_ - [IdentityResolveResponse](#identityresolveresponse) object received once execution is
  completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

### FullContactClient.identity.delete()

class: _fullcontact.api.resolve_api.ResolveApi_

#### Parameters:

* `recordId`: _str_ - (required)
* `headers`: _dict_ - [optional]

#### Returns:

#### IdentityDeleteResponse

class: _fullcontact.response.resolve_response.IdentityDeleteResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict. Empty dict will be returned on successful delete.
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers

### FullContactClient.identity.delete_async()

class: _fullcontact.api.resolve_api.ResolveApi_

#### Parameters:

Same as that of [FullContactClient.identity.delete()](#fullcontactclientidentitydelete)

#### Returns:

#### Future[IdentityDeleteResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _IdentityDeleteResponse_ - [IdentityDeleteResponse](#identitydeleteresponse) object received once
  execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

## Tags API

The client library provides methods to interact with Customer Tags API (`tags.get`, `tags.create` and `tags.delete`
endpoints) through `FullContactClient.tags` object. The Tags API can be accessed using the
methods [get()](#fullcontactclienttagsget), [create()](#fullcontactclienttagscreate)
and [delete()](#fullcontactclienttagsdelete), respectively. These APIs can be accessed using the async version these
functions, [get_async()](#fullcontactclienttagsget_async), [create_async()](#fullcontactclienttagscreate_async)
and [delete_async()](#fullcontactclienttagsdelete_async). Additional headers can be set on a per-request basis by
setting the parameter `headers` while calling these methods.     
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Tags API Documentation: https://platform.fullcontact.com/docs/apis/resolve/customer-tags

```python
# Synchronous create execution
create_response = fullcontact_client.tags.create(recordId="customer123",
                                                 tags={"segment": "highspender"})
print(create_response.json())
# Output: {'recordId': 'customer123', 'tags': [{'key': 'segment', 'value': 'highspender'}]}

# Synchronous get execution
get_response = fullcontact_client.tags.get(recordId="customer123")
print(get_response.get_tags())
# Output: {'segment': ['highspender']}

# Synchronous delete execution
delete_response = fullcontact_client.tags.delete(recordId="customer123",
                                                 tags={"segment": "highspender"})
print(delete_response.get_status_code())
# Output: 204

# Asynchronous create execution
create_async_response = fullcontact_client.tags.create_async(recordId="customer123",
                                                             tags={"segment": "highspender"})
create_response = create_async_response.result()
print(create_response.json())
# Output: {'recordId': 'customer123', 'tags': [{'key': 'segment', 'value': 'highspender'}]}

# Asynchronous get execution
get_async_response = fullcontact_client.tags.get_async(recordId="customer123")
get_response = get_async_response.result()
print(get_response.get_tags())
# Output: {'segment': ['highspender']}

# Asynchronous delete execution
delete_async_response = fullcontact_client.tags.delete_async(recordId="customer123",
                                                             tags={"segment": "highspender"})
delete_response = delete_async_response.result()
print(delete_response.get_status_code())
# Output: 204
```

### FullContactClient.tags.create()

class: _fullcontact.api.tags_api.TagsApi_

#### Parameters:

* `recordId`: _str_ - (required)
* `tags`: _dict_ - (required)
  > Tags dict has to be in the format {tag1_key: tag1_value, tag2_key: [tag2_value1, tag2_value2], ...}. Tag value can be a string or a list of strings to support multiple values.
* `headers`: _dict_ - [optional]

#### Returns:

#### TagsCreateResponse

class: _fullcontact.response.tags_response.TagsCreateResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers

### FullContactClient.tags.create_async()

class: _fullcontact.api.tags_api.TagsApi_

#### Parameters:

Same as that of [FullContactClient.tags.create()](#fullcontactclienttagscreate)

#### Returns:

#### Future[TagsCreateResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _TagsCreateResponse_ - [TagsCreateResponse](#tagecreateresponse) object received once execution is
  completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

### FullContactClient.tags.get()

class: _fullcontact.api.tags_api.TagsApi_

#### Parameters:

* `**identifiers`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

Supported `identifiers` to get tags:

* `recordId`: _str_
* `partnerId`: _str_

#### Returns:

#### TagsGetResponse

class: _fullcontact.response.tags_response.TagsGetResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_tags()`: _dict_ - Tags from the response in format _{tag1_key: tag1_value, tag2_key, tag2_value, ...}_
* `get_recordId()`: _str_ - `recordId` from the response
* `get_partnerId()`: _str_ - `partnerId` from the response

### FullContactClient.tags.get_async()

class: _fullcontact.api.tags_api.TagsApi_

#### Parameters:

Same as that of [FullContactClient.tags.get()](#fullcontactclienttagsget)

#### Returns:

#### Future[TagsGetResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _TagsGetResponse_ - [TagsGetResponse](#tagsgetresponse) object received once execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

### FullContactClient.tags.delete()

class: _fullcontact.api.tags_api.TagsApi_

#### Parameters:

* `recordId`: _str_ - (required)
* `tags`: _dict_ - (required)
  > Tags dict has to be in the format {tag1_key: tag1_value, tag2_key: tag2_value, ...}
* `headers`: _dict_ - [optional]

#### Returns:

#### TagsDeleteResponse

class: _fullcontact.response.tags_response.TagsDeleteResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict. Empty dict will be returned on successful delete.
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers

### FullContactClient.tags.delete_async()

class: _fullcontact.api.tags_api.TagsApi_

#### Parameters:

Same as that of [FullContactClient.tags.delete()](#fullcontactclienttagsdelete)

#### Returns:

#### Future[TagsDeleteResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _TagsDeleteResponse_ - [TagsDeleteResponse](#tagsdeleteresponse) object received once execution is
  completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

## Audience API

The client library provides methods to interact with Audience Tags API (`audience.create` and `audience.download`
endpoints) through `FullContactClient.audience` object. The Audience API can be accessed using the
methods [create()](#fullcontactclientaudiencecreate) and [download()](#fullcontactclientaudiencedownload), respectively.
These APIs can be accessed using the async version these
functions, [create_async()](#fullcontactclientaudiencecreate_create)
and [download_async()](#fullcontactclientaudiencedownload_async). Additional headers can be set on a per-request basis
by setting the parameter `headers` while calling these methods.     
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Tags API Documentation: https://platform.fullcontact.com/docs/apis/resolve/customer-tags

```python
# Synchronous create execution
create_response = fullcontact_client.audience.create(webhookUrl="http://your_webhookUrl/",
                                                     tags={"segment": "highspender"})
print(create_response.json())
# Output: {'requestId': 'c7273de7-e717-4cab-9fe0-213ab3796636'}

# Synchronous download execution
download_response = fullcontact_client.audience.download(requestId="c7273de7-e717-4cab-9fe0-213ab3796636")
download_response.write_to_file("/path/to/output_file.json.gz")
print(download_response.get_status_code())
# Output: 200

# Asynchronous create execution
create_async_response = fullcontact_client.audience.create(webhookUrl="http://your_webhookUrl/",
                                                           tags={"segment": "highspender"})
create_response = create_async_response.result()
print(create_response.json())
# Output: {'requestId': 'c7273de7-e717-4cab-9fe0-213ab3796636'}

# Asynchronous download execution
download_async_response = fullcontact_client.audience.download_async(requestId="c7273de7-e717-4cab-9fe0-213ab3796636")
download_response = download_async_response.result()
download_response.write_to_file("/path/to/output_file.json.gz")
print(download_response.get_status_code())
# Output: 200
```

### FullContactClient.audience.create()

class: _fullcontact.api.tags_api.AudienceApi_

#### Parameters:

* `webhookUrl`: _str_ - (required)
* `tags`: _dict_ - (required)
  > Tags dict has to be in the format {tag1_key: tag1_value, tag2_key: tag2_value, ...}
* `headers`: _dict_ - [optional]

#### Returns:

#### AudienceCreateResponse

class: _fullcontact.response.audience_response.AudienceCreateResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_requestId()`: _str_ - `requestId` created for the request

### FullContactClient.audience.create_async()

class: _fullcontact.api.audience_api.AudienceApi_

#### Parameters:

Same as that of [FullContactClient.audience.create()](#fullcontactclientaudiencecreate)

#### Returns:

#### Future[AudienceCreateResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _AudienceCreateResponse_ - [AudienceCreateResponse](#audiencecreateresponse) object received once
  execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

### FullContactClient.audience.download()

class: _fullcontact.api.audience_api.AudienceApi_

#### Parameters:

* `requestId`: _str_ - (required)
* `headers`: _dict_ - [optional]

#### Returns:

#### AudienceDownloadResponse

class: _fullcontact.response.audience_response.AudienceDownloadResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `write_to_file(file)`: _bool_ - Writes the downloaded file contents to the input file/fileObj
    * Param `file` : _str_/_FileObject_ - It can the path to a file as string or a bytes writable file object. The file
      will be of format `.json.gz` if the download was successful. This can be confirmed using the `is_successful` flag.
  > An easy way to create a bytes writable file object is by using io.BytesIO

### FullContactClient.audience.download_async()

class: _fullcontact.api.audience_api.AudienceApi_

#### Parameters:

Same as that of [FullContactClient.audience.download()](#fullcontactclientaudiencedownload)

#### Returns:

#### Future[AudienceDownloadResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _AudienceDownloadResponse_ - [AudienceDownloadResponse](#audiencedownloadresponse) object received once
  execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

## Permission API

The client library provides methods to interact with Permission
through `FullContactClient.permission` object. Additional headers can be set on a per-request basis
by setting the parameter `headers` while calling these methods.     
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Permission APIs Documentation: https://platform.fullcontact.com/docs/apis/permission/introduction

class: _fullcontact.api.permission_api.PermissionApi_

```python
# Synchronous create execution
permission_create_response = fullcontact_client.permission.create(
                            query={"email": "cutomer1@fullcontact.com"},
                            consentPurposes=[
                                {
                                    "purposeId": 2,
                                    "channel": ["web","phone","mobile","offline","email"],
                                    "ttl": 1095,
                                    "enabled": True
                                },
                                {
                                    "purposeId": 5,
                                    "channel": ["web","phone","mobile","offline","email"],
                                    "ttl": 1095,
                                    "enabled": True
                                }
                            ],
                            locale="US",
                            language="en",
                            collectionMethod="cookie",
                            collectionLocation="US",
                            policyUrl="https://www.fullcontact-test.com/services-privacy-policy/",
                            termsService="https://www.fullcontact-test.com/content-policy/"
                            )
print(permission_create_response.get_status_code())
# Output: 202

# Synchronous delete execution
permission_delete_response = fullcontact_client.permission.delete(query={"email": "cutomer1@fullcontact.com"})
print(permission_delete_response.get_status_code())
# Output: 202

# Synchronous find execution
permission_find_response = fullcontact_client.permission.find(query={"email": "cutomer1@fullcontact.com"})
print(permission_find_response.json())
'''
Output:
[
    {
        "permissionType": "create",
        "permissionId": "0089ced6-eaa8-4ac4-a6b2-de9d16928461",
        "consentPurposes": [
            {
                "ttl": null,
                "enabled": True,
                "channel": "web",
                "purposeId": 6,
                "purposeName": "Content selection, delivery & reporting",
                "timestamp": 1614855618604
            }
        ],
        "locale": "US",
        "ipAddress": "127.0.0.1",
        "language": "en",
        "collectionMethod": "cookie",
        "collectionLocation": "ae",
        "policyUrl": "https://www.fullcontact-test.com/services-privacy-policy/",
        "termsService": "https://www.fullcontact-test.com/content-policy/",
        "timestamp": None,
        "created": 1614855618604
    },
    {
        "permissionType": "delete",
        "permissionId": "0089ced6-eaa8-4ac4-a6b2-de9d169284rt4",
        "consentPurposes": [
            {
                "ttl": null,
                "enabled": True,
                "channel": "web",
                "purposeId": 2,
                "purposeName": "Content selection, delivery & reporting",
                "timestamp": 1614855618607
            }
        ],
        "locale": "US",
        "ipAddress": "127.0.0.1",
        "language": "en",
        "collectionMethod": "cookie",
        "collectionLocation": "ae",
        "policyUrl": "https://www.fullcontact-test.com/services-privacy-policy/",
        "termsService": "https://www.fullcontact-test.com/content-policy/",
        "timestamp": None,
        "created": 1614855618607
    }
]
'''
# Synchronous Current execution
permission_current_response = fullcontact_client.permission.current(query={"email": "cutomer1@fullcontact.com"})
print(permission_current_response.json())
'''
Output:
{
    "3": {
        "offline": {
            "ttl": 1095,
            "enabled": True,
            "channel": "offline",
            "purposeId": 3,
            "purposeName": "Personalized Content Profile",
            "timestamp": 1614837134541
        },
        "phone": {
            "ttl": 1095,
            "enabled": True,
            "channel": "phone",
            "purposeId": 3,
            "purposeName": "Personalized Content Profile",
            "timestamp": 1614837134541
        },
        "mobile": {
            "ttl": 1095,
            "enabled": True,
            "channel": "mobile",
            "purposeId": 3,
            "purposeName": "Personalized Content Profile",
            "timestamp": 1614837134541
        },
        "email": {
            "ttl": 1095,
            "enabled": True,
            "channel": "email",
            "purposeId": 3,
            "purposeName": "Personalized Content Profile",
            "timestamp": 1614837134541
        }
    },
    "6": {
        "web": {
            "ttl": null,
            "enabled": True,
            "channel": "web",
            "purposeId": 6,
            "purposeName": "Content selection, delivery & reporting",
            "timestamp": 1614856047618
        }
    }
}
'''
# Synchronous Verify execution
permission_verify_response = fullcontact_client.permission.verify(query={"email": "cutomer1@fullcontact.com"},
                                                                purposeId=6, 
                                                                channel="web")
print(permission_verify_response.json())
'''
Output:
{
    "ttl": 1024,
    "enabled": true,
    "channel": "web",
    "purposeId": 6,
    "purposeName": "Content selection, delivery & reporting",
    "timestamp": 1614856047613
}
'''
```

### FullContactClient.permission.create()

class: _fullcontact.schema.permission_schema.PermissionCreateRequestSchema_

#### Parameters:

* `**query`: _kwargs_ - [required]
* `headers`: _dict_ - [optional]

Supported fields in `query`:
- `query`: [MultifieldReq](#multifieldrequest) - [required]
- `consentPurposes`: List[PurposeRequestSchema] - [required]
- `locale`: str
- `ipAddress`: str
- `language`: str
- `collectionMethod`: str - [required]
- `collectionLocation`: str - [required]
- `policyUrl`: str - [required]
- `termsService`: str - [required]
- `tcf`: str
- `timestamp`: int

#### PurposeRequestSchema

- `purposeId`: int - [required]
- `channel`: List[str]
- `ttl`: int
- `enabled`: bool  - [required]

#### Returns:

class: _fullcontact.response.permission_response.PermissionCreateResponse_

A basic API response with response code as `202` if successful.

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers

### FullContactClient.permission.delete()

class: _fullcontact.schema.permission_schema.PermissionDeleteRequestSchema_

#### Parameters:

* `**query`: _kwargs_ - [required]
* `headers`: _dict_ - [optional]

`query` takes a [MultiFieldReq](#multifieldrequest)

#### Returns:

class: _fullcontact.response.permission_response.PermissionDeleteResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers

### FullContactClient.permission.find()

class: _fullcontact.schema.permission_schema.PermissionFindRequestSchema_

#### Parameters:

* `**query`: _kwargs_ - [required]
* `headers`: _dict_ - [optional]

`query` takes a [MultiFieldReq](#multifieldrequest)

#### Returns:

class: _fullcontact.response.permission_response.PermissionFindResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers

### FullContactClient.permission.current()

class: _fullcontact.schema.permission_schema.PermissionCurrentRequestSchema_

#### Parameters:

same as that of [FullContactClient.permission.find()](#fullcontactclientpermissionfind)

#### Returns:

class: _fullcontact.response.permission_response.PermissionCurrentResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_consent_for_purposeId(self, purposeId: int)`: _dict_ - of Consent set for the purposeId

### FullContactClient.permission.verify()

class: _fullcontact.schema.permission_schema.PermissionVerifyRequestSchema_

#### Parameters:

* `**query`: _kwargs_ - [required]
* `headers`: _dict_ - [optional]

Supported fields in `query`:
- `query`: [MultifieldReq](#multifieldrequest) - [required]
- `purposeId`: int - [required]
- `channel`: str - [required]

#### Returns:

class: _fullcontact.response.permission_response.PermissionVerifyResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers

### Permission APIs Asynchronous methods
Client Library also support corresponding async methods for Permission APIs such as:
- `permission.create_async()`
- `permission.delete_async()`
- `permission.find_async()`
- `permission.current_async()`
- `permission.verify_async()`

All these takes same parameters as their synchronous counterparts but return a `Future` instead.

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

## Verify API

The client library provides methods to interact with V3 Verfiy API (`verify.match`, `verify.signals` and `verify.activity` 
endpoints) through `FullContactClient.verify` object. The V3 Verify API can be accessed using
the methods [match()](#fullcontactclientverifymatch), [signals()](#fullcontactclientverifysignals) and 
[activity()](#fullcontactclientverifyactivity), respectively. These APIs can be accessed using the async version these
functions, [match_async()](#fullcontactclientverifymatch_async), [signals_async()](#fullcontactclientverifysignals_async) and
[activity_async()](#fullcontactclientverifyactivity_async). Additional headers can be set on a per-request basis by
setting the parameter `headers` while calling these methods.     
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Verify API Documentation: https://docs.fullcontact.com/docs/verify-overview

```python
# Synchronous match execution
match_response = fullcontact_client.verify.match(email="bart.lorang@fullcontact.com")
print(match_response.json())
# Output: {'email': True}

# Synchronous signals execution
signals_response = fullcontact_client.verify.signals(email="marquitaross006@gmail.com")
print(signals_response.json())
'''
Output: 
{ 'personIds': ['L0yG2Mp8Z4TVHxJK92GAxjWsTX6lrSfMBsQKvRsy5NzKnTm6'], 
  'maids': [{'id': '0N3ZIUBF-RPCI-GO59-O29M-S3I3U0A8I9WUN', 'type': 'idfa', 'firstSeenMs': 0, 'lastSeenMs': 0, 'observations': 1, 'confidence': 1.0}], 
  'name': {'givenName': 'Marquita', 'familyName': 'Ross'}, 
  'nonIds': [{'id': '0C-83f57c786a0b_-4a39efab23731c7EBC', 'firstSeenMs': 0, 'lastSeenMs': 0, 'observations': 1, 'confidence': 1.0}], 
  'socialProfiles': {'twitterUrl': 'https://twitter.com/marqross91', 'linkedInUrl': 'https://www.linkedin.com/in/marquita-ross-5b6b72192'}, 
  'demographics': {'age': 42, 'ageRange': '40-49', 'gender': 'Female'}, 
  'employment': {'current': True, 'company': 'Mostow Co.', 'title': 'Senior Petroleum Manager'}
}
'''

# Synchronous activity execution
activity_response = fullcontact_client.verify.activity(email="bart.lorang@fullcontact.com")
print(activity_response.json())
# Output: {'emails': 0.03}

# Asynchronous match execution
match_async_response = fullcontact_client.verify.match_async(email="bart.lorang@fullcontact.com")
match_response = match_async_response.result()
print(match_response.json())
# Output: {'email': True}

# Asynchronous signals execution
signals_async_response = fullcontact_client.verify.signals_async(email="marquitaross006@gmail.com")
signals_response = signals_async_response.result()
print(signals_response.json())
'''
Output: 
{ 'personIds': ['L0yG2Mp8Z4TVHxJK92GAxjWsTX6lrSfMBsQKvRsy5NzKnTm6'], 
  'maids': [{'id': '0N3ZIUBF-RPCI-GO59-O29M-S3I3U0A8I9WUN', 'type': 'idfa', 'firstSeenMs': 0, 'lastSeenMs': 0, 'observations': 1, 'confidence': 1.0}], 
  'name': {'givenName': 'Marquita', 'familyName': 'Ross'}, 
  'nonIds': [{'id': '0C-83f57c786a0b_-4a39efab23731c7EBC', 'firstSeenMs': 0, 'lastSeenMs': 0, 'observations': 1, 'confidence': 1.0}], 
  'socialProfiles': {'twitterUrl': 'https://twitter.com/marqross91', 'linkedInUrl': 'https://www.linkedin.com/in/marquita-ross-5b6b72192'}, 
  'demographics': {'age': 42, 'ageRange': '40-49', 'gender': 'Female'}, 
  'employment': {'current': True, 'company': 'Mostow Co.', 'title': 'Senior Petroleum Manager'}
}
'''

# Asynchronous activity execution
activity_async_response = fullcontact_client.verify.activity_async(email="bart.lorang@fullcontact.com")
activity_response = activity_async_response.result()
print(activity_response.json())
# Output: {'emails': 0.03}

```

### FullContactClient.verify.match()

class: _fullcontact.api.verify_api.VerifyClient_

#### Parameters:

* `**query`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

`query` takes in [MultiFieldReq](#multifieldrequest).

#### Returns:

#### VerifyMatchResponse

class: _fullcontact.response.verify_response.MatchResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_city()`: _bool_ - city flag from Verify Match Response
* `get_region()`: _bool_ - region flag from Verify Match Response
* `get_country()`: _bool_ - country flag from Verify Match Response
* `get_continent()`: _bool_ - continent flag from Verify Match Response
* `get_postalCode()`: _bool_ - postalCode flag from Verify Match Response
* `get_familyName()`: _bool_ - familyName flag from Verify Match Response
* `get_givenName()`: _bool_ - givenName flag from Verify Match Response
* `get_phone()`: _bool_ - phone flag from Verify Match Response
* `get_maid()`: _bool_ - maid flag from Verify Match Response
* `get_email()`: _bool_ - email flag from Verify Match Response
* `get_social()`: _bool_ - social flag from Verify Match Response
* `get_nonId()`: _bool_ - nonId flag from Verify Match Response

### FullContactClient.verify.match_async()

class: _fullcontact.api.verify_api.VerifyClient_

#### Parameters:

Same as that of [FullContactClient.verify.match()](#fullcontactclientverifymatch)

#### Returns:

#### Future[VerifyMatchResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _VerifyMatchResponse_ - [VerifyMatchResponse](#verifymatchresponse) object received once execution is
  completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.

### FullContactClient.verify.signals()

class: _fullcontact.api.verify_api.VerifyClient_

#### Parameters:

* `**query`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

`query` takes in [MultiFieldReq](#multifieldrequest).

#### Returns:

#### VerifySignalsResponse

class: _fullcontact.response.verify_response.VerifySignalResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_personIds()`: List[str] - List of personIds from Signals response
* `get_name()`: _dict_ - Name from Verify Signals response
* `get_emails()`: List[_dict_] - List of email objects from Verify Signals response
* `get_phones()`: List[_dict_] - List of phone objects from Verify Signals response
* `get_maids()`: List[_dict_] - List of maids objects from Verify Signals response
* `get_nonIds()`: List[_dict_] - List of nonIds objects from Verify Signals response
* `get_panoIds()`: List[_dict_] - List of panoIds objects from Verify Signals response
* `get_ipAddresses()`: List[_dict_] - List of ipAddress objects from Verify Signals response
* `get_socialProfiles()`: List[str] - List of Social Profiles from Verify Signals response
* `get_demographics()`: _dict_ - Demographics from Verify Signals response
* `get_employment()`: _dict_ - Employment from Verify Signals response
* `get_locations()`: List[_dict_] - List of location object from Verify Signals response

### FullContactClient.verify.signals_async()

class: _fullcontact.api.verify_api.VerifyClient_

#### Parameters:

Same as that of [FullContactClient.verify.signals()](#fullcontactclientverifysignals)

#### Returns:

#### Future[VerifySignalsResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _VerifySignalsResponse_ - [VerifySignalsResponse](#verifysignalsresponse) object received once
  execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.


### FullContactClient.verify.activity()

class: _fullcontact.api.verify_api.VerifyClient_

#### Parameters:

* `**query`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

`query` takes in [MultiFieldReq](#multifieldrequest).

#### Returns:

#### VerifyActivityResponse

class: _fullcontact.response.verify_response.VerifyActivityResponse_

#### Instance variables

* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object

#### Methods:

* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers
* `get_emails()`: _float_ - email activity score from Verify Activity Response

### FullContactClient.verify.activity_async()

class: _fullcontact.api.verify_api.VerifyClient_

#### Parameters:

Same as that of [FullContactClient.verify.activity()](#fullcontactclientverifyactivity)

#### Returns:

#### Future[VerifyActivityResponse]

class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects

#### Useful Methods:

* `result()`: _VerifyActivityResponse_ - [VerifyActivityResponse](#verifyactivityresponse) object received once execution is
  completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.
