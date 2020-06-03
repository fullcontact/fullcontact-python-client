class ErrorMessages(object):
    PERSON_ENRICH_NOT_QUERYABLE = "No queryable inputs given (" \
                                  "for example: email, emails, phone, phones," \
                                  " location, name, profiles, maids, recordId, personId)"

    PERSON_ENRICH_INVALID_LOCATION = "Possible combinations to query by Location are:\n" \
                                     "addressLine1 + city + region\n" \
                                     "addressLine1 + city + regionCode\n" \
                                     "addressLine1 + postalCode"

    PERSON_ENRICH_INVALID_NAME = "Possible combinations to query by Name are:\n" \
                                 "given + family\n" \
                                 "full"

    PERSON_ENRICH_INVALID_NAME_LOCATION = "Location and Name have to be queried together"

    IDENTITY_MAP_NOT_QUERYABLE = "No queryable inputs given " \
                                 "(for example: email, emails, phone, phones, location, name, profiles, maids)"

    IDENTITY_RESOLVE_NOT_QUERYABLE = "No queryable inputs given " \
                                     "(for example: email, emails, phone, phones, location, name, profiles, maids, " \
                                     "recordId, personId)"

    IDENTITY_DELETE_MISSING_ARGUMENT = "delete() missing 1 required positional argument: 'recordId'"

