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
* **Parameters:** Same as [`enrich()`](#enrichheadersnone-delay1-max_retries5-query-1), but the supported fields in `query` are different. Supported fields are mentioned in the next section.
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

### Valid query parameter for search:
* **companyName** _[str]_ _(required)_ - The name of the company to search for.
* ** sort** _[str]_ _(optional)_ - Controls how results will be sorted. Valid values: `traffic`, `relevance`, `employees`
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
