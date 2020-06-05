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

