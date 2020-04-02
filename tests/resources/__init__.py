import inspect
import json
import os


def get_resource_json(json_type, request_type, request_method, test_scenario):
    dirpath = "%s/api_%ss/" % (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), json_type)
    filename = "%s_%s_%s.json" % (request_type, request_method, test_scenario)
    filepath = dirpath + filename
    json_data = {}
    if os.path.exists(filepath):
        with open(filepath) as json_file:
            json_data = json.load(json_file)
    return json_data
