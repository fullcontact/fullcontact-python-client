""" Recipe script which uses the FullContact Python library to resolve contact identifiers to personIds. In this case, the input file is presumed to have a header representing a valid Multifield request (https://github.com/fullcontact/fullcontact-python-client#multifieldrequest).

This script assumes the names of the input and output are "input.csv" and "output.csv", respectively.
"""

#!/usr/bin/env python3
import csv
import os

from fullcontact import FullContactClient

# Fetch API Key from env variable "FC_API_KEY"
API_KEY = os.environ.get('FC_API_KEY')

# Define input, output file names
input_file = './input.csv'
output_filename= './output.csv'
outputs = []

fullcontact_client = FullContactClient(api_key=API_KEY)
with open(input_file, encoding='utf-8') as csvf:
    csv_reader = csv.DictReader(csvf)
    
    for row in csv_reader:
        try:
	    # Pass all row K:V pairings to API.
            future = fullcontact_client.identity.resolve_async(**row)
            result = future.result()
            personIds = result.get_personIds()
            row['personIds'] = personIds
        except Exception as e:
	    # Generic exception handling. Should be more granular in a production env
            print('something went wrong: ', e)
            row['personIds'] = []
        outputs.append(row)

with open(output_filename, 'w', newline='') as output_file:
    # Define header based on one row's keys
    keys = outputs[0].keys()
    out_writer = csv.DictWriter(output_file, keys)
    out_writer.writeheader()
    for row in outputs:
        out_writer.writerow(row)

