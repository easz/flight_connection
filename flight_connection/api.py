
import itertools
import json
import math
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
  max_flight_legs = req.get('max_flight_legs', 4)
  max_ground_legs = req.get('max_ground_legs', 1)

  route_ids = connection.find_shortest_connection(departure_code=departure_code,
                                              destination_code=destination_code)

  airports = [connection.find_airport(id=id, attribtes=['Name','IATA']) for id in route_ids] if route_ids is not None else []

  explain = "No route is found"
  roune_codes = [airport['IATA'] for airport in airports]
  route_names = [airport['Name'] for airport in airports]

  if route_ids is not None:
    total_legs = len(route_ids) - 1
    types = [connection.g_routes.get_edge_data(*pair) for pair in itertools.pairwise(route_ids)]
    has_flight = lambda d: math.isnan(d["flight_distance"]) is not True
    flight_legs = len(list(filter(has_flight, types)))
    ground_legs = total_legs - flight_legs
    if flight_legs <= max_flight_legs and ground_legs <= max_ground_legs:
      explain = "A shortest route with {total_legs} leg{s} is found.".format(total_legs=total_legs, s="s" if total_legs > 1 else "")
    else:
      explain = "A shortest route cannot be found due to the limit of leg numbers"
      roune_codes = [] # clear
      route_names = []

  return build_response({
    "route": roune_codes,
    "aiports": route_names,
    "explain": explain
  })