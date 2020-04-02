# Python Client
Python client for `FullContact` API.

## Basic Usage
FC Client supports 2 main types of querying; `Person` and `Company`.

#### Supported operations:
- `Person.enrich`
- `Company.enrich`
- `Company.search`

### Person Enrich
Class: `fc_client.Person`

#### Initialization
```
from fc_client import Person
person = Person(api_key=<YOUR_API_KEY>)
```
**Parameters:**
- `api_key`: Mandatory

#### Methods

**Enrich**
```
person.enrich(**query, [headers, retry])
```
Parameters:
- `query`: _kwargs_ - Query to be sent in the request, as kwargs
    - `email`: _str_
    - `emails`: _list[str]_
    - `phone`: _str_
    - `phones`: _list[str]_
    - `location`: _dict_
        - `addressLine1`: _str_
        - `addressLine2`: _str_
        - `city`: _str_
        - `region`: _str_
        - `regionCode`: _str_
        - `postalCode`: _str_
    - `name`: _dict_
        - `full`: _str_
        - `given`: _str_
        - `family`: _str_
    - `profiles`: _list[dict]_
        - `service`: _str_
        - `username`: _str_
        - `userid`: _str_
        - `url`: _str_
    - `webhookUrl`: _str_
- `headers`: _dict_
    - `Reporting-Key`: str
    - `Any additional header key`: str
- `retry`: int - Number of retries in case of failure, such as rate limit.

Returns:
`PersonEnrichResponse` object with the below properties/variables and methods:
- `is_successful`: boolean
- `response`: requests.Response object that was originally received
- `raw()`: dict with person enrich api response contents
- `get_summary()`: dict with person summary from the response
- `get_details()`: dict with details from the response
- `get_message()`: str error message if unsuccessful
- Some additional methods for getting some specific fields from the `details` dict:
    - `get_name()`
    - `get_age()`
    - `get_gender()`
    - `get_demographics()`
    - `get_emails()`
    - `get_phones()`
    - `get_profiles()`
    - `get_locations()`
    - `get_employment()`
    - `get_photos()`
    - `get_education()`
    - `get_urls()`
    - `get_interests()`
    - `get_household()`
    - `get_finance()`
    - `get_census()`
    
**Enrich Async**
```
person.enrich_async(**query, [headers, retry])
```
Parameters:
Same as Enrich

Returns:
- A `concurrent.futures.Future` object
    - Future.result() returns the `PersonEnrichResponse` described in Enrich, once the API call has been finished.
    - Future.exception() returns any exception that occurred during the execution.


### Company Enrich and Search
Class: `fc_client.Company`

#### Initialization
```
from fc_client import Person
company = Company(api_key=<YOUR_API_KEY>)
```
**Parameters:**
- `api_key`: Mandatory

#### Methods

**Enrich**
```
company.enrich(**query, [headers, retry])
```
Parameters:
- `query`: _kwargs_ - Query to be sent in the request, as kwargs
    - `domain`: str
    - `webhookUrl`: str
- `headers`: _dict_
    - `Reporting-Key`: str
    - `Any additional header key`: str
- `retry`: int - Number of retries in case of failure, such as rate limit

Returns:
`CompanyEnrichResponse` object with the below properties/variables and methods:
- `is_successful`: boolean
- `response`: requests.Response object that was originally received
- `raw()`: dict with company enrich api response contents
- `get_summary()`: dict with company summary from the response
- `get_details()`: dict with details from the response
- `get_message()`: str error message if unsuccessful

**Enrich Async**
```
company.enrich_async(**query, [headers, retry])
```
Parameters:
Same as Enrich

Returns:
- A `concurrent.futures.Future` object
    - Future.result() returns the `CompanyEnrichResponse` described in Enrich, once the API call has been finished.
    - Future.exception() returns any exception that occurred during the execution.

**Search**
```
company.search(**query, [headers, retry])
```
Parameters:
- `query`: _kwargs_ - Query to be sent in the request, as kwargs
    - `companyName`: str
    - `sort`: str
    - `location`: str
    - `locality`: str
    - `region`: str
    - `country`: str
    - `webhookUrl`: str
- `headers`: _dict_
    - `Reporting-Key`: str
    - `Any additional header key`: str
- `retry`: int - Number of retries in case of failure, such as rate limit

Returns:
`CompanySearchResponse` object with the below properties/variables and methods:
- `is_successful`: boolean
- `response`: requests.Response object that was originally received
- `raw()`: list of dict with company search api response contents
- `get_message()`: str error message if unsuccessful

**Search Async**
```
company.search_async(**query, [headers, retry])
```
Parameters:
Same as Search

Returns:
- A `concurrent.futures.Future` object
    - Future.result() returns the `CompanySearchResponse` described in Search, once the API call has been finished.
    - Future.exception() returns any exception that occurred during the execution.

## Examples
### Person Enrich
```
from fc_client import Person
person = Person("xxxxxxxxxxxxxxxxx")
response = person.enrich(email="bart@fullcontact.com", name={'full': 'Bart Lorang'})
response_async = person.enrich_async(email="bart@fullcontact.com", name={'full': 'Bart Lorang'})
```

### Company Enrich
```
from fc_client import Company
company = Company("xxxxxxxxxxxxxxxxx")
response = company.enrich(domain="fullcontact.com")
response_async = company.enrich_async(domain="fullcontact.com")
```

### Company Search
```
from fc_client import Company
company = Company("xxxxxxxxxxxxxxxxx")
response = company.search(companyName="fullcontact")
response_async = company.enrich_async(companyName="fullcontact")
```


## Exceptions
All the exceptions raised by the FC client will be subclasses of `fc_client.exceptions.FullcontactException`
Any validation error will raise `fc_client.exceptions.ValidationError`, which is also a subclass of `fc_client.exceptions.FullcontactException`