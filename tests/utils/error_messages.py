class ErrorMessages(object):
    NO_QUERYABLE_INPUTS = "No queryable inputs given"

    COMPANY_ENRICH_NOT_QUERYABLE = "For Company Enrich query, domain is required."
    COMPANY_SEARCH_NOT_QUERYABLE = "For Company Search query, companyName is required."

    PERSON_ENRICH_INVALID_LOCATION = "Possible combinations to query by Location are:\n" \
                                     "addressLine1 + city + region\n" \
                                     "addressLine1 + city + regionCode\n" \
                                     "addressLine1 + postalCode"

    PERSON_ENRICH_INVALID_NAME = "Possible combinations to query by Name are:\n" \
                                 "given + family\n" \
                                 "full"

    PERSON_ENRICH_INVALID_NAME_LOCATION = "Location and Name have to be queried together"

    IDENTITY_DELETE_MISSING_ARGUMENT = "delete() missing 1 required positional argument: 'recordId'"

    TAGS_DELETE_MISSING_ARGUMENT = "delete() missing 2 required positional arguments: 'recordId' and 'tags'"
    TAGS_CREATE_MISSING_ARGUMENT = "create() missing 2 required positional arguments: 'recordId' and 'tags'"

    AUDIENCE_CREATE_MISSING_ARGUMENT = "create() missing 2 required positional arguments: 'webhookUrl' and 'tags'"
    AUDIENCE_DOWNLOAD_MISSING_ARGUMENT = "download() missing 1 required positional argument: 'requestId'"

    VERIFICATION_EMAIL_MISSING_ARGUMENT = "email() missing 1 required positional argument: 'email'"
