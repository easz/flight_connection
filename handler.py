import json
import flight_connection.api

def find_connection(input, context):
    # the input data should be either a json string or dict obj
    req = json.loads(input) if isinstance(input, str) else input
    # call actual bacend
    return flight_connection.api.find_connection(req)