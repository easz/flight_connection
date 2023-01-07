import argparse
import json
import flight_connection.api

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("request", help="request in JSON")

  args = parser.parse_args()

  req = json.loads(args.request)
  resp = flight_connection.api.find_connection(req)

  print(json.dumps(resp, indent=4))