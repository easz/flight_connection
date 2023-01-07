
import json
from . import connection

def build_response(jsonBody, statusCode=200):
      return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(jsonBody)
    }

def find_connection(req):
  departure_code = req.get('from')
  destination_code = req.get('to')
  max_legs = req.get('max_legs')
  route = connection.find_shortest_connection(departure_code=departure_code,
                                              destination_code=destination_code,
                                              max_legs=max_legs)
  return build_response({
    "route": route,
    "aiports": [connection.find_airport(id=id)['Name'] for id in route] if route is not None else None
  })