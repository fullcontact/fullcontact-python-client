# FullContact Client
The official python client library for FullContact V3 API. This client provides an interface to perform Person Enrich, Company Enrich and Company Search operations.   
FullContact API Documentation is available at: https://dashboard.fullcontact.com/api-ref

# Table of contents
* [Requirements](#requirements)
* [Installation](#installation)
* [Basic Usage](#basic-usage)
* [PersonClient](#personclient)
    * [Methods](#methods)
        * [enrich](#enrichheadersnone-delay1-max_retries5-query)
        * [enrich_async](#enrich_asyncheadersnone-delay1-max_retries5-query)
    * [Query](#query)
        * [Valid enrich parameters](#valid-query-parameters)
    * [Response](#response)
        * [PersonEnrichResponse](#personenrichresponse)
        * [Future](#future)
* [CompanyClient](#companyclient)
    * [Methods](#methods-1)
        * [enrich](#enrichheadersnone-delay1-max_retries5-query-1)
        * [enrich_async](#enrich_asyncheadersnone-delay1-max_retries5-query-1)
        * [search](#searchheadersnone-delay1-max_retries5-query)
        * [search_async](#search_asyncheadersnone-delay1-max_retries5-query)
    * [Query](#query-1)
        * [Valid enrich parameters](#valid-query-parameter-for-enrich)
        * [Valid search parameters](#valid-query-parameters-for-search)
    * [Response](#response-1)
        * [CompanyEnrichResponse](#companyenrichresponse)
        * [CompanySearchResponse](#companysearchresponse)
        * [Future](#future-1)
* [Examples](#examples)
    * [PersonClient](#personclient-1)
    * [CompanyClient](#companyclient-1)

# Requirements
This library requires Python 3.5 and above. 

# Installation
It is recommended to install the FullContact python client library from [PyPi](https://pypi.org/) using the below command.
```
pip install python-fullcontact
```
It is also possible to install the package by cloning this repo, by running the below commands.
```
git clone git@github.com:fullcontact/fullcontact-python-client.git
pip install -e fullcontact-python-client
```

# Basic Usage
**PersonClient**   
[PersonClient](#personclient) can be initialized and used as below.
```python
import os
from fullcontact import PersonClient

person_client = PersonClient(os.environ.get('FULLCONTACT_API_KEY'))
person_response = person_client.enrich(email="marquitaross006@gmail.com")
```
More examples for [PersonClient](#personclient) usage can be found in [Examples](#personclient-1) section.

**CompanyClient**   
[CompanyClient](#companyclient) can be initialized and used as below.
```python
import os
from fullcontact import CompanyClient

company_client = CompanyClient(os.environ.get('FULLCONTACT_API_KEY'))
company_enrich_response = company_client.enrich(domain="fullcontact.com")
company_search_response = company_client.search(companyName="fullcontact")
```
More examples for [CompanyClient](#companyclient) usage can be found in [Examples](#companyclient-1) section.

# PersonClient
This class provides an interface to the V3 Person Enrich endpoint. Once the client library is installed, `PersonClient` can be directly imported from it and an instance can be created using the API Key,as follows.
```python
from fullcontact import PersonClient
person_client = PersonClient(<API_KEY>)
```
## Methods

### enrich(_headers=None_, _delay=1_, _max_retries=5_, _**query_)
* **Parameters:**
    * **headers** _[dict]_ _(optional)_ - Any custom header that you wish to add to the request should be provided through this parameter as a dictionary. `Authorization` and `Content-Type` headers are added automatically, and need not be specified explicitly.
    
        > An example use of this is to add Reporting Key, if required.   
        > `headers = {"Reporting-Key": "clientXYZ"}`

    * **delay** _[int]_ _(optional)_ - Delay in seconds to retry, in case of response status code 429 or 503. This value will be used as the base delay in exponential backoff. Default value is 1.
    * **max_retries** _[int]_ _(optional)_ - Maximum number of retries, in case of response status code 429 or 503. Maximum value allowed for this is 5.
    * **query** _[kwargs]_ _(required)_ - This is the query for performing person enrich operation and hence, is a required parameter. It should be provided as keyword arguments.
* **Returns:** [`PersonEnrichResponse`](#personenrichresponse) object
* **Return type:** [`fullcontact.response.person_response.PersonEnrichResponse`](#personenrichresponse)

### enrich_async(_headers=None_, _delay=1_, _max_retries=5_, _**query_)
This method has the same parameters as the [`enrich()`](#enrichheadersnone-delay1-max_retries5-query) method, but works asynchronously using a [`concurrent.futures.thread.ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor).
* **Parameters:** Same as the parameters of [`enrich()`](#enrichheadersnone-delay1-max_retries5-query) method.
* **Returns:** [`Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object. Result is delivered through [`Future.result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) method, once done.
* **Return type:** [`concurrent.futures.Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future)

## Query
For person enrich operation, the query has to be provided as _kwargs_. The query parameters are aligned with the [FullContact Enrich API Multi Field Request](https://dashboard.fullcontact.com/api-ref#multi-field-request)

> If you have a dict query, that can be converted to _kwargs_ by prepending ** to it.   
> `person_client.enrich(**{"email": "abc@xyz.com", "phone": "1234567890"})`

### Valid query parameters:
* **email** _[str]_ - One email address of the contact. Can accept cleartext, an MD5 or SHA-256 hash representation of the email address to query. Be certain to lowercase and trim the email address prior to hashing. There is a limit of 10 hashed emails.
* **emails** _[list(str)]_ - One or many email addresses of the contact. Can accept cleartext, an MD5 or SHA-256 hash representation of the email address to query. Be certain to lowercase and trim the email address prior to hashing.
* **phone** _[str]_ - Phone number of the contact. For international numbers a country code is required.
* **phones** _[list(str)]_ - One or many phone numbers of the contact. For international numbers a country code is required.
* **profiles** _[list(dict)]_ - A list of profiles. Below are the supported parameters for a profile.
    * **service** _[str]_ - Service type of the profiles on the social platform. Either of username or userid has to be specified with service.
    * **username** _[str]_ - Username of the profile on the social platform. Service has to be specified with username.
    * **userid** _[str]_ - User ID of the profile on the social platform. Service has to be specified with userid.
    * **url** _[str]_ - URL to the profile on the social platform. None of the other profile parameters can be specified with url.
* **name** _[dict]_ - Name of the individual. Only queryable when provided in conjunction with location.
    * **full** _[str]_ - Full name of the contact (givenName, familyName).
    * **given** _[str]_ - The given name (first name) of the individual.
    * **family** _[str]_ - The family name (last name) of the individual.
* **location** _[dict]_ - Postal address of the individual. Only queryable when provided in conjunction with name.
    * **addressLine1** _[str]_ - The first address line of postal address.
    * **addressLine2** _[str]_ - The second address line of postal address.
    * **city** _[str]_ - The city of postal address.
    * **region** _[str]_ - The region of postal address.
    * **regionCode** _[str]_ - The region code of postal address.
    * **postalCode** _[str]_ - The postal code of postal address. Can accept Zip + 4 or Zip.
* **maids** _list(str)_ - One or more Mobile Advertising IDs (MAIDs) for an individual, as a list.

**Additional optional parameters that can be passed in query:**
* **confidence** _[str]_ _(optional)_ - Acceptable values are 'LOW', 'MED', 'HIGH', and 'MAX'. If this parameter is not specified, the API defaults to the value 'HIGH'.

    > The higher the confidence, the higher the likelihood that the data returned is accurate. If the confidence level of the data to be returned does not meet or exceed the parameter provided, then the result will not be a match. Generally, setting this value higher results in more accurate data, but fewer matches, while setting the value lower results in more matches and data, but lower quality and accuracy.

* **infer** _[bool]_ _(optional)_ - Flag for enabling or disabling inferences. If this parameter is not specified, the API defaults to `True`.
* **dataFilter** _list(str)_ _(optional)_ - A specific set of insight bundles can be provided in this parameter as a list, to tailor the result and only receive data back for specific Insights Bundles that are already enabled on your account.
* **webhookUrl** _[str]_ _(optional)_ - If a valid webhook url is passed through this parameter, the request will be queued and result will be POSTed to the provided webhook URL, once the processing has been completed.

**Valid combinations for `profiles`, `name` and `location`:**
* `profiles`: A list of dictionaries of the above mentioned specification has to be provided to query by `profiles`. Only the below mentioned combinations are accepted:
    * `service` + `username`
    * `service` + `userid`
    * `url`
* `location`: A dictionary with above mentioned specification has to be provided, along with a valid `name` to query by `location`. Only the below mentioned combinations are accepted:
    * `addressLine1` + `city` + `region`
    * `addressLine1` + `city` + `regionCode`
    * `addressLine1` + `postalCode`
* `name`: A dictionary with above mentioned specification has to be provided, along with a valid `location` to query by `name`. Only the below mentioned combinations are accepted:
    * `full`
    * `given` + `family`


## Response
The response of [`enrich()`](#enrichheadersnone-delay1-max_retries5-query) method is a [`PersonEnrichResponse`](#personenrichresponse) object of type [`fullcontact.response.person_response.PersonEnrichResponse`](#personenrichresponse). The responses are aligned with the [Person Enrichment Response](https://dashboard.fullcontact.com/api-ref#person-enrichment).

The response of [`enrich_async()`](#enrich_asyncheadersnone-delay1-max_retries5-query) method is a [`Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object of type [`concurrent.futures.Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future). If successful, the [`Future.result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) will return a [`PersonEnrichResponse`](#personenrichresponse).

### PersonEnrichResponse
`PersonEnrichResponse` provides the below instance variables and methods
* **is_successful** _[bool]_ - `True` if the response status code is 200, 202 or 404. Else, `False`.
* **response** _[requests.Response]_ - The actual Response object received from `requests.post` operation, that makes the API call. This may be helpful in debugging.
* **get_status_code()** -> _[int]_ - Returns the HTTP status code received.
* **get_message()** -> _[str]_ - Returns the error message received from the API and the HTTP status message otherwise.
* **get_headers()** -> _[dict]_ - Returns the response headers as a dictionary.
* **raw()** -> _[dict]_ - Returns the response body converted to a dictionary.
* **get_summary()** -> _[dict]_ - Returns a dictionary with the Person summary extracted from raw response. This is the person response without the `details` in it.
* **get_details()** -> _[dict]_ - Returns the details from the person summary as a dictionary.
* **get_name()** -> _[dict]_ - Returns the name, if available in the response, as a dictionary.
* **get_age()** -> _[dict]_ - Returns the age, if available in the response, as a dictionary.
* **get_gender()** -> _[str]_ - Returns the gender, if available in the response, as a string.
* **get_demographics()** -> _[dict]_ - Returns the demographics, if available in the response, as a dictionary.
* **get_emails()** -> _[list(str)]_ - Returns the emails, if available in the response, as a list of strings.
* **get_phones()** -> _[list(str)]_ - Returns the phones, if available in the response, as a list of strings.
* **get_profiles()** -> _[list(dict)]_ - Returns the profiles, if available in the response, as a list of dictionaries.
* **get_locations()** -> _[list(dict)]_ - Returns the locations, if available in the response, as a list of dictionaries.
* **get_employment()** -> _[list(dict)]_ - Returns the employment details, if available in the response, as a list of dictionaries.
* **get_photos()** -> _[list(dict)]_ - Returns the photos, if available in the response, as a list of dictionaries.
* **get_education()** -> _[list(dict)]_ - Returns the education details, if available in the response, as a list of dictionaries.
* **get_urls()** -> _[list(dict)]_ - Returns the URLs, if available in the response, as a list of dictionaries.
* **get_interests()** -> _[list(dict)]_ - Returns the interests, if available in the response, as a list of dictionaries.
* **get_household()** -> _[dict]_ - Returns the household details, if available in the response, as a dictionary.
* **get_finance()** -> _[dict]_ - Returns the finance details, if available in the response, as a dictionary.
* **get_census()** -> _[dict]_ - Returns the census details, if available in the response, as a dictionary.

### Future
The [Future](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object returned by the [`enrich_async()`](#enrich_asyncheadersnone-delay1-max_retries5-query) method provides a method [`result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) to retrieve the result once the processing is done. The output of this [`result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) method will be a [`PersonEnrichResponse`](#personenrichresponse).    
For details on Future objects, please refer: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future



# CompanyClient
This class provides an interface to the V3 Company Enrich and Search endpoints. Once the client library is installed, `CompanyClient` can be directly imported from it and an instance can be created using the API Key, as follows.
```python
from fullcontact import CompanyClient
company_client = CompanyClient(<API_KEY>)
```
## Methods

### enrich(_headers=None_, _delay=1_, _max_retries=5_, _**query_)
This method has the same parameters as [`PersonClient.enrich()`](#enrichheadersnone-delay1-max_retries5-query), but hits FullContact Company Enrich API instead of Person Enrich API and accepts different fields for query.
* **Parameters:** Same as [`PersonClient.enrich()`](#enrichheadersnone-delay1-max_retries5-query), but the supported fields in `query` are different. Supported fields are mentioned in the next section.
* **Returns:** [`CompanyEnrichResponse`](#companyenrichresponse) object
* **Return type:** [`fullcontact.response.company_response.CompanyEnrichResponse`](#companyenrichresponse)

### enrich_async(_headers=None_, _delay=1_, _max_retries=5_, _**query_)
This method has the same parameters as the [`enrich()`](#enrichheadersnone-delay1-max_retries5-query-1) method, but works asynchronously using a [`concurrent.futures.thread.ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor).
* **Parameters:** Same as the parameters of [`enrich()`](#enrichheadersnone-delay1-max_retries5-query-1) method.
* **Returns:** [`Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object. Result is delivered through [`Future.result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) method, once done.
* **Return type:** [`concurrent.futures.Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future)

### search(_headers=None_, _delay=1_, _max_retries=5_, _**query_)
This method has the same parameters as [`enrich()`](#enrichheadersnone-delay1-max_retries5-query-1), but hits FullContact Company Search API instead of Company Enrich API and accepts different fields for query.
* **Parameters:** Same as [`enrich()`](#enrichheadersnone-delay1-max_retries5-query-1), but the supported fields in [`query`](#valid-query-parameter-for-search) are different.
* **Returns:** [`CompanySearchResponse`](#companysearchresponse) object
* **Return type:** [`fullcontact.response.company_response.CompanySearchResponse`](#companysearchresponse)

### search_async(_headers=None_, _delay=1_, _max_retries=5_, _**query_)
This method has the same parameters as the [`search()`](#searchheadersnone-delay1-max_retries5-query) method, but works asynchronously using a [`concurrent.futures.thread.ThreadPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor).
* **Parameters:** Same as the parameters of [`search()`](#searchheadersnone-delay1-max_retries5-query) method.
* **Returns:** [`Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object. Result is delivered through [`Future.result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) method, once done.
* **Return type:** [`concurrent.futures.Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future)

## Query
For company enrich and search operations, the query has to be provided as _kwargs_. The query parameters are aligned with the [FullContact Company Enrichment Requests](https://dashboard.fullcontact.com/api-ref#multi-field-request)

### Valid query parameter for enrich:
* **domain** _[str]_ - The domain name of the company to lookup.

### Valid query parameters for search:
* **companyName** _[str]_ _(required)_ - The name of the company to search for.
* **sort** _[str]_ _(optional)_ - Controls how results will be sorted. Valid values: `traffic`, `relevance`, `employees`
* **location** _[str]_ _(optional)_ - If provided, only companies matching given location will be returned.
* **locality** _[str]_ _(optional)_ - If provided, only companies matching given locality/city will be returned.
* **region** _[str]_ _(optional)_ - If provided, only companies matching given region/state will be returned.
* **country** _[str]_ _(optional)_ - If provided, only companies matching given country will be returned.

**Additional optional parameters that can be passed in enrich/search query:**
* **webhookUrl** _[str]_ _(optional)_ - If a valid webhook url is passed through this parameter, the request will be queued and result will be POSTed to the provided webhook URL, once the processing has been completed.

## Response
The responses of [`enrich()`](#enrichheadersnone-delay1-max_retries5-query-1) and [`search()`](#searchheadersnone-delay1-max_retries5-query) methods are [`CompanyEnrichResponse`](#companyenrichresponse) of type [`fullcontact.response.company_response.CompanyEnrichResponse`]((#companyenrichresponse)) and [`CompanySearchResponse`](#companysearchresponse) object of type [`fullcontact.response.company_response.CompanySearchResponse`](#companysearchresponse), respectively. The responses are aligned with the [Company Enrichment/Search Response](https://dashboard.fullcontact.com/api-ref#company-enrichment).

The response of [`enrich_async()`](#enrich_asyncheadersnone-delay1-max_retries5-query-1) or [`search_async()`](#search_asyncheadersnone-delay1-max_retries5-query) method is a [`Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object of type [`concurrent.futures.Future`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future). If successful, the [`Future.result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) will return a [`CompanyEnrichResponse`](#companyenrichresponse) or a [`CompanySearchResponse`](#companysearchresponse), based on the method.

### CompanyEnrichResponse
`CompanyEnrichResponse` provides the below instance variables and methods
* **is_successful** _[bool]_ - `True` if the response status code is 200, 202 or 404. Else, `False`.
* **response** _[requests.Response]_ - The actual Response object received from `requests.post` operation, that makes the API call. This may be helpful in debugging.
* **get_status_code()** -> _[int]_ - Returns the HTTP status code received.
* **get_message()** -> _[str]_ - Returns the error message received from the API and the HTTP status message otherwise.
* **get_headers()** -> _[dict]_ - Returns the response headers as a dictionary.
* **raw()** -> _[dict]_ - Returns the response body converted to a dictionary.
* **get_summary()** -> _[dict]_ - Returns a dictionary with the Company summary extracted from raw response. This is the company enrich response without the `details` in it.
* **get_details()** -> _[dict]_ - Returns the details from the company summary as a dictionary.

### CompanySearchResponse
`CompanySearchResponse` provides the below instance variables and methods
* **is_successful** _[bool]_ - `True` if the response status code is 200, 202 or 404. Else, `False`.
* **response** _[requests.Response]_ - The actual Response object received from `requests.post` operation, that makes the API call. This may be helpful in debugging.
* **get_status_code()** -> _[int]_ - Returns the HTTP status code received.
* **get_message()** -> _[str]_ - Returns the error message received from the API and the HTTP status message otherwise.
* **get_headers()** -> _[dict]_ - Returns the response headers as a dictionary.
* **raw()** -> _[list]_ or _[dict]_ - Returns the response body with search results converted to a list if successful and otherwise, a dictionary with response converted to a dictionary.

### Future
The [Future](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future) object returned by the [`enrich_async()`](#enrich_asyncheadersnone-delay1-max_retries5-query-1) or [`search_async()`](#search_asyncheadersnone-delay1-max_retries5-query) method provides a method [`result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) to retrieve the result once the processing is done. The output of this [`result()`](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future.result) method will be a [`CompanyEnrichResponse`](#companyenrichresponse) or a [`CompanySearchResponse`](#companysearchresponse).    
For details on Future objects, please refer: https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future

# Examples
## PersonClient
* **Initialization**
```python
import os
from fullcontact import PersonClient

person_client = PersonClient(os.environ.get('FULLCONTACT_API_KEY'))
```
* **Synchronous simple query**
```python
person_response = person_client.enrich(email="marquitaross006@gmail.com")

print(person_response.get_summary())
{
  "fullName": "Marquita H Ross",
  "ageRange": "37-47",
  "gender": "Female",
  "location": "San Francisco, California, United States",
  "title": "Senior Petroleum Manager",
  "organization": "Mostow Co.",
  "twitter": "https://twitter.com/marqross91",
  "linkedin": "https://www.linkedin.com/in/marquita-ross-5b6b72192",
  "facebook": null,
  "bio": "Senior Petroleum Manager at Mostow Co.",
  "avatar": "https://img.fullcontact.com/sandbox/1gagrO2K67_oc5DLG_siVCpYVE5UvCu2Z.png",
  "website": "http://marquitaas8.com/",
  "isSandboxProfile": true,
  "updated": "1970-01-01"
}
```
* **Synchronous multifield query**
```python
person_response = person_client.enrich(**{
  "emails": [
    "marquitaross006@gmail.com"
  ],
  "phones": [
    "+14105551773"
  ]
})

print(person_response.get_summary())
{
  "fullName": "Marquita H Ross",
  "ageRange": "37-47",
  "gender": "Female",
  "location": "San Francisco, California, United States",
  "title": "Senior Petroleum Manager",
  "organization": "Mostow Co.",
  "twitter": "https://twitter.com/marqross91",
  "linkedin": "https://www.linkedin.com/in/marquita-ross-5b6b72192",
  "facebook": null,
  "bio": "Senior Petroleum Manager at Mostow Co.",
  "avatar": "https://img.fullcontact.com/sandbox/1gagrO2K67_oc5DLG_siVCpYVE5UvCu2Z.png",
  "website": "http://marquitaas8.com/",
  "isSandboxProfile": true,
  "updated": "1970-01-01"
}
```
* **Synchronous query by name and address with insights bundle**
```python
query = {
  "name": {
    "given": "Marquita",
    "family": "Ross"
  },
  "location": {
    "addressLine1": "313 North Gainsway Street",
    "city": "San Francisco",
    "region": "California"
  }
}

person_response = person_client.enrich(dataAddon=["location"], **query)

print(person_response.get_summary())
{
  "fullName": "Marquita H Ross",
  "ageRange": "37-47",
  "gender": "Female",
  "location": "San Francisco, California, United States",
  "title": "Senior Petroleum Manager",
  "organization": "Mostow Co.",
  "twitter": "https://twitter.com/marqross91",
  "linkedin": "https://www.linkedin.com/in/marquita-ross-5b6b72192",
  "facebook": null,
  "bio": "Senior Petroleum Manager at Mostow Co.",
  "avatar": "https://img.fullcontact.com/sandbox/1gagrO2K67_oc5DLG_siVCpYVE5UvCu2Z.png",
  "website": "http://marquitaas8.com/",
  "isSandboxProfile": true,
  "updated": "1970-01-01"
}
```
* **Asynchronous queries**
```python
import concurrent.futures

from fullcontact.exceptions import FullContactException

queries = [
  {
    "email": "marquitaross006@gmail.com"
  },
  {
    "email": "ispangler@yandex.com",
    "phone": "+12075550145"
  },
  {
    "phone": "+14105551773"
  }
]

futures = [ person_client.enrich_async(query) for query in queries ]

for future in concurrent.futures.as_completed(futures):
  try:
    data = future.result()
  except FullContactException as fc_exception:
    print("FullContactException occurred: %s" % str(fc_exception))
  except Exception as other_exception:
    print("Some error occurred: %s" % str(other_exception))

```
## CompanyClient
* **Initialization**
```python
import os
from fullcontact import CompanyClient

company_client = CompanyClient(os.environ.get('FULLCONTACT_API_KEY'))
```

* **Synchronous enrich query**
```python
company_enrich_response = company_client.enrich(domain="fullcontact.com")

print(company_enrich_response.get_summary())
{
  "name": "FullContact Inc.",
  "location": "1755 Blake Street Suite 450 Denver CO, 80202 USA",
  "twitter": "https://twitter.com/fullcontact",
  "linkedin": "https://www.linkedin.com/company/fullcontact-inc-",
  "facebook": null,
  "bio": "FullContact is the most powerful fully-connected contact management platform for professionals and enterprises who need to master their contacts and be awesome with people.",
  "logo": "https://img.fullcontact.com/static/bb796b303166bd928f6c0968f15d4a4e_7ef85b2a563abd95ae07e815da2db916a5f8de4d82702388e546a66adc9eac44",
  "website": "https://www.fullcontact.com",
  "founded": 2010,
  "employees": 351,
  "locale": "en",
  "category": "Other",
  "dataAddOns": [
    {
      "id": "keypeople",
      "name": "Key People",
      "enabled": true,
      "applied": true,
      "description": "Displays information about people of interest at this company.",
      "docLink": "http://docs.fullcontact.com/api/#key-people"
    }
  ],
  "updated": "2020-04-03"
}
```
* **Synchronous search query**
```python
query = {
  "companyName": "fullcontact",
  "sort": "relevance",
  "location": "Colorado, USA",
  "locality": "Denver",
  "region": "Colorado",
  "country": "United States"
}

company_search_response = company_client.search(**query)

print(company_search_response.raw())
[
  {
    "lookupDomain": "blog.fullcontact.com",
    "orgName": "FullContact, Inc.",
    "logo": "https://d2ojpxxtu63wzl.cloudfront.net/v1/thumbnail?size=128&url=https://img.fullcontact.com/static/6a43815ada39ec64b22d4589c11360b0_ac6d3981bba92f9df1c232eb98ad255a821acb3bbf66334c079b27f438b93653",
    "location": {
      "locality": "Denver",
      "region": {
        "name": "Colorado",
        "code": "CO"
      },
      "country": {
        "name": "United States",
        "code": "US"
      }
    },
    "score": 1
  },
  {
    "lookupDomain": "tryfullcontact.com",
    "orgName": "FullContact, Inc.",
    "logo": "https://d2ojpxxtu63wzl.cloudfront.net/v1/thumbnail?size=128&url=https://img.fullcontact.com/static/d82fa6b4ff10b53af598b274bb9cafbc_f739aa5936447143d4fdcb242a112c62dcfba5c13400dfbcdc9b685ade1409f8",
    "location": {
      "locality": "Denver",
      "region": {
        "name": "Colorado",
        "code": "CO"
      },
      "country": {
        "name": "United States",
        "code": "US"
      }
    },
    "score": 0.976352277344633
  }
]
```

* **Asynchronous enrich query**
```python
company_enrich_future = company_client.enrich_async(domain="fullcontact.com")
company_enrich_response = company_enrich_future.result()

print(company_enrich_response.get_summary())
{
  "name": "FullContact Inc.",
  "location": "1755 Blake Street Suite 450 Denver CO, 80202 USA",
  "twitter": "https://twitter.com/fullcontact",
  "linkedin": "https://www.linkedin.com/company/fullcontact-inc-",
  "facebook": null,
  "bio": "FullContact is the most powerful fully-connected contact management platform for professionals and enterprises who need to master their contacts and be awesome with people.",
  "logo": "https://img.fullcontact.com/static/bb796b303166bd928f6c0968f15d4a4e_7ef85b2a563abd95ae07e815da2db916a5f8de4d82702388e546a66adc9eac44",
  "website": "https://www.fullcontact.com",
  "founded": 2010,
  "employees": 351,
  "locale": "en",
  "category": "Other",
  "dataAddOns": [
    {
      "id": "keypeople",
      "name": "Key People",
      "enabled": true,
      "applied": true,
      "description": "Displays information about people of interest at this company.",
      "docLink": "http://docs.fullcontact.com/api/#key-people"
    }
  ],
  "updated": "2020-04-03"
}
```

* **Asynchronous search query**
```python
query = {
  "companyName": "fullcontact",
  "sort": "relevance",
  "location": "Colorado, USA",
  "locality": "Denver",
  "region": "Colorado",
  "country": "United States"
}

company_search_future = company_client.search_async(**query)
company_search_response = company_search_future.result()

print(company_search_response.raw())
[
  {
    "lookupDomain": "blog.fullcontact.com",
    "orgName": "FullContact, Inc.",
    "logo": "https://d2ojpxxtu63wzl.cloudfront.net/v1/thumbnail?size=128&url=https://img.fullcontact.com/static/6a43815ada39ec64b22d4589c11360b0_ac6d3981bba92f9df1c232eb98ad255a821acb3bbf66334c079b27f438b93653",
    "location": {
      "locality": "Denver",
      "region": {
        "name": "Colorado",
        "code": "CO"
      },
      "country": {
        "name": "United States",
        "code": "US"
      }
    },
    "score": 1
  },
  {
    "lookupDomain": "tryfullcontact.com",
    "orgName": "FullContact, Inc.",
    "logo": "https://d2ojpxxtu63wzl.cloudfront.net/v1/thumbnail?size=128&url=https://img.fullcontact.com/static/d82fa6b4ff10b53af598b274bb9cafbc_f739aa5936447143d4fdcb242a112c62dcfba5c13400dfbcdc9b685ade1409f8",
    "location": {
      "locality": "Denver",
      "region": {
        "name": "Colorado",
        "code": "CO"
      },
      "country": {
        "name": "United States",
        "code": "US"
      }
    },
    "score": 0.976352277344633
  }
]
```
