# FullContact Client
[![PyPI](https://img.shields.io/pypi/v/python-fullcontact?label=PyPi)](https://pypi.org/project/python-fullcontact/)
![flake8](https://github.com/fullcontact/fullcontact-python-client/workflows/flake8/badge.svg)
![pytest](https://github.com/fullcontact/fullcontact-python-client/workflows/pytest/badge.svg)

The official python client library for FullContact V3 API. This client provides an interface to perform Person Enrich, Company Enrich and Company Search operations.   
FullContact API Documentation is available at: https://dashboard.fullcontact.com/api-ref


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
        * [search()](#fullcontactclientcompanysearch)
        * [search_async()](#fullcontactclientcompanysearch_async)
    * [Resolve API](#resolve-api)
        * [map()](#fullcontactclientidentitymap)
        * [map_async()](#fullcontactclientidentitymap_async)
        * [resolve()](#fullcontactclientidentityresolve)
        * [resolve_async()](#fullcontactclientidentityresolve_async)
        * [delete()](#fullcontactclientidentitydelete)
        * [delete_async()](#fullcontactclientidentitydelete_async)


# Requirements
This library requires Python 3.5 or above. 


# Adding To Your Project
To add FullContact Python Client library to your project, add the below line to your `requirements.txt` file, or as a requirement in the `setup.py` file.
```
python-fullcontact==2.0.0
```


# Installation
It is recommended to install the FullContact python client library from [PyPi](https://pypi.org/) using the below command.
```
pip install python-fullcontact
```
It is also possible to install the package from this repo, by running the below commands.
```
pip install git+https://github.com/fullcontact/fullcontact-python-client.git
```


# Migrating from FullContact Client V1.0.0
This version of FullContact Client (V2.0.0) has significant changes in terms of design and features. Hence, it is not backward compatible with V1.0.0 library.
However, migrating from the V1.0.0 client is very easy.
In V1.0.0, there used to be different clients for different APIs (PersonClient, CompanyClient). However with V2.0.0, we have only 1 client, with different methods.
#### V1.0.0
```python
from fullcontact import PersonClient, CompanyClient
person_client = PersonClient("<your_api_key>")
company_client = CompanyClient("<your_api_key>")
person_client.enrich(**query)
company_client.enrich(**query)
company_client.search(**query)
```
This would be changed as below in V2.0.0

#### V2.0.0
```python
from fullcontact import FullContactClient
fullcontact_client = FullContactClient("<your_api_key>")
fullcontact_client.person.enrich(**query)
fullcontact_client.company.enrich(**query)
fullcontact_client.company.search(**query)
```


# Usage
## Importing the client
The client is available straight out of the package `fullcontact`.
```python
from fullcontact import FullContactClient
```


## Basic Usage
To use the client library, you need to initialize the client using the API KEY that you have generated from [FullContact Developer Dashboard](https://dashboard.fullcontact.com).
Once initialized, the client provides the `Enrich` and `Resolve` capabilities of the V3 FullContact API.
```python
from fullcontact import FullContactClient

fullcontact_client = FullContactClient("<your_api_key>")

# V3 Person Enrich
person_enrich_result = fullcontact_client.person.enrich(email="marquitaross006@gmail.com")

# V3 Company Enrich
company_enrich_result = fullcontact_client.company.enrich(domain="fullcontact.com")

# V3 Company Search
company_search_results = fullcontact_client.company.search(companyName="fullcontact")

# V3 Identity Map
identity_map_result = fullcontact_client.identity.map(email="marquitaross006@gmail.com", recordId="customer123")

# V3 Identity Resolve
identity_resolve_result = fullcontact_client.identity.resolve(recordId="customer123")

# V3 Identity Delete
identity_delete_result = fullcontact_client.identity.delete(recordId="customer123")
```


## Client Configuration
The FullContact Client allows the configuration of additional headers and retry related values, through init parameters.

#### API Key
API Key is required to Authorize with FullContact API and hence, is a required parameter.
This is set using the `api_key` init parameter for [FullContactClient](#fullcontactclient).

```python
fullcontact_client = FullContactClient("<your_api_key>")
```

#### Headers
The headers `Authorization`, `Content-Type` and `User-Agent` are added automatically and cannot be overridden. Hence, headers needs to be added only if any additional header needs to be passed to the API.
One useful situation for this is when you need to pass your `Reporting-Key`.
The headers can be added by setting the `headers` init parameter for [FullContactClient](#fullcontactclient).

```python
additional_headers = {"Reporting-Key": "clientXYZ"}
fullcontact_client = FullContactClient(api_key="<your_api_key>", headers=additional_headers)
```

#### Retry
By default, the client retries a request if it receives a `429` or `503` status code. The default retry count is 1 and the backoff factor (base delay) for exponential backoff is 1 second.
Retry can by configured by setting the `max_retry_count`, `retry_status_codes` and `base_delay` init parameters for [FullContactClient](#fullcontactclient).
If the value provided for `max_retry_count` is greater than 5, it will be set to 5.

```python
fullcontact_client = FullContactClient(api_key="<your_api_key>", max_retry_count=3, retry_status_codes=(429, 503, 413), base_delay=2.5)
```

### FullContactClient
class: _fullcontact.FullContactClient_
#### Init parameters:
* `api_key`: _str_ - (required)
* `headers`: _dict_ - [optional]
* `max_retry_count`: _int_ _[default=5]_ - [optional]
* `retry_status_codes`: _List[int]_ _[default=(429, 503)]_ - [optional]
* `base_delay`: _float_ _[default=1.0]_ - [optional]


## Person API
The client library provides methods to interact with V3 Person Enrich API through `FullContactClient.person` object.
The V3 Person Enrich API can be called synchronously using [enrich()](#fullcontactclientpersonenrich) and asynchronously using [enrich_async()](#fullcontactclientpersonenrich_async).
Additional headers can be set on a per-request basis by setting the parameter `headers` while calling [enrich()](#fullcontactclientpersonenrich) or [enrich_async()](#fullcontactclientpersonenrich_async).
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Person Enrichment API Documentation: https://dashboard.fullcontact.com/api-ref#person-enrichment

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

Supported fields for query:
* `email`: _str_
* `emails`: _List[str]_
* `phone`: _str_
* `phones`: _List[str]_
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
* `webhookUrl`: _str_
* `confidence`: _str_
* `dataFilter`: _List[str]_
* `infer`: _bool_

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


### FullContactClient.person.enrich_async()
class: _fullcontact.api.person_api.PersonApi_
Same as that of [FullContactClient.person.enrich()](#fullcontactclientpersonenrich)

#### Returns:
#### Future[PersonEnrichResponse]
class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects
#### Useful Methods:
* `result()`: _PersonEnrichResponse_ - [PersonEnrichResponse](#personenrichresponse) object received once execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.



## Company API
The client library provides methods to interact with V3 Company Enrich and Search APIs through `FullContactClient.company` object.
The V3 Company Enrich API can be called synchronously using [enrich()](#fullcontactclientcompanyenrich) and asynchronously using [enrich_async()](#fullcontactclientcompanyenrich_async).
Similarly, the V3 Company Search API can be called synchronously using [search()](#fullcontactclientcompanysearch) and asynchronously using [search_async()](#fullcontactclientcompanysearch_async).
Additional headers can be set on a per-request basis by setting the parameter `headers` while calling [enrich()](#fullcontactclientcompanyenrich)), [enrich_async()](#fullcontactclientcompanyenrich_async), [search()](#fullcontactclientcompanysearch) or [search_async()](#fullcontactclientcompanysearch_async).  
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Company Enrichment API Documentation: https://dashboard.fullcontact.com/api-ref#company-enrichment

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
 'dataAddOns': [{'id': 'keypeople',
   'name': 'Key People',
   'enabled': True,
   'applied': True,
   'description': 'Displays information about people of interest at this company.',
   'docLink': 'http://docs.fullcontact.com/api/#key-people'}],
 'updated': '2020-05-31'} """

# Synchronous search execution
search_response = fullcontact_client.company.search(companyName="fullcontact")
print(search_response.json()[0])
""" Output: {'lookupDomain': 'fullcontact.com',
 'orgName': 'FullContact Inc',
 'logo': 'https://d2ojpxxtu63wzl.cloudfront.net/v1/thumbnail?size=128&url=https://img.fullcontact.com/static/7329d91237b7970b984d56c2497c80c0_7abd96cd75e5587b39b9f15dce07d7ebe8dc31accecf1b0f2a617ada34498633',
 'location': {'locality': 'Denver',
  'region': {'name': 'CO'},
  'country': {'name': 'USA'}}} """

# Asynchronous enrich execution
enrich_async_response = fullcontact_client.company.enrich_async(domain="fullcontact.com")
enrich_result = enrich_async_response.result()
print(enrich_result.get_summary())

# Asynchronous search execution
search_async_response = fullcontact_client.company.search_async(companyName="fullcontact")
search_result = search_async_response.result()
print(search_result.json()[0])
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
* `result()`: _CompanyEnrichResponse_ - [CompanyEnrichResponse](#companyenrichresponse) object received once execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.


### FullContactClient.company.search()
class: _fullcontact.api.company_api.CompanyApi_
#### Parameters:
* `**query`: _kwargs_ - (required)
* `headers`: _dict_ - [optional]

Supported fields for query:
* `companyName`: _str_
* `sort`: _str_
* `location`: _str_
* `locality`: _str_
* `region`: _str_
* `country`: _str_
* `webhookUrl`: _str_

#### Returns:
#### CompanySearchResponse
class: _fullcontact.response.company_response.CompanySearchResponse_

#### Instance variables
* `is_successful`: _bool_ - Success flag
* `response`: _requests.Response_ - Raw _requests.Response_ object
#### Methods:
* `json()`: _dict_ - Response JSON as dict
* `get_message()`: _str_ - Response message or HTTP status message
* `get_headers()`: _dict_ - Response headers


### FullContactClient.company.search_async()
class: _fullcontact.api.company_api.CompanyClient_
#### Parameters:
Same as that of [FullContactClient.company.search()](#fullcontactclientcompanysearch)

#### Returns:
#### Future[CompanySearchResponse]
class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects
#### Useful Methods:
* `result()`: _CompanySearchResponse_ - [CompanySearchResponse](#companysearchresponse) object received once execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.


## Resolve API
The client library provides methods to interact with V3 Resolve API (`identity.map`, `identity.resolve` and `identity.delete` endpoints) through `FullContactClient.identity` object.
The V3 Resolve API can be accessed using the methods [map()](#fullcontactclientidentitymap), [resolve()](#fullcontactclientidentityresolve) and [delete()](#fullcontactclientidentitydelete), respectively.
These APIs can be accessed using the async version these functions, [map_async()](#fullcontactclientidentitymap_async), [resolve_async()](#fullcontactclientidentityresolve_async) and [delete_async()](#fullcontactclientidentitydelete_async).
Additional headers can be set on a per-request basis by setting the parameter `headers` while calling these methods.     
Being a request level parameter, this can be used to override any header that has been set on the client level.
> Resolve API Documentation: https://dashboard.fullcontact.com/api-ref#resolve-2

```python
# Synchronous map execution
map_response = fullcontact_client.identity.map(email="marquitaross006@gmail.com", recordId="customer123")
print(map_response.get_recordIds())
# Output: ['customer123']

# Synchronous resolve execution
resolve_response = fullcontact_client.identity.resolve(email="marquitaross006@gmail.com")
print(resolve_response.get_recordIds())
# Output: ['customer123']

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

Supported fields for mapping:
* `email`: _str_
* `emails`: _List[str]_
* `phone`: _str_
* `phones`: _List[str]_
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
* `recordId`: _str_ - (required)

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
* `result()`: _IdentityMapResponse_ - [IdentityMapResponse](#identitymapresponse) object received once execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.


### FullContactClient.identity.resolve()
class: _fullcontact.api.resolve_api.ResolveApi_ 
#### Parameters:
* `**fields`: _kwargs_ - (required)
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


### FullContactClient.identity.resolve_async()
class: _fullcontact.api.resolve_api.ResolveApi_
#### Parameters:
Same as that of [FullContactClient.identity.resolve()](#fullcontactclientidentityresolve)

#### Returns:
#### Future[IdentityResolveResponse]
class: _concurrent.Futures.Future_
> More on _concurrent.Futures.Future_: https://docs.python.org/3/library/concurrent.futures.html#future-objects
#### Useful Methods:
* `result()`: _IdentityResolveResponse_ - [IdentityResolveResponse](#identityresolveresponse) object received once execution is completed
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
* `result()`: _IdentityDeleteResponse_ - [IdentityDeleteResponse](#identitydeleteresponse) object received once execution is completed
* `add_done_callback(fn)`: _None_ - Add a callback function to be executed on successful execution.
