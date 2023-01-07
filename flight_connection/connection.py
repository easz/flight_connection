import math
import pandas as pd
import networkx as nx

df_airports = pd.read_pickle('data/df_airports.pkl')
#df_routes = pd.read_pickle('data/df_routes.pkl')
#df_flight_route_graph = pd.read_pickle('data/df_flight_route_graph.pkl')
#df_ground_route_graph = pd.read_pickle('data/df_ground_route_graph.pkl')
df_route_graph = pd.read_pickle('data/df_route_graph.pkl')

#g_flight_routes = nx.from_pandas_edgelist(df_flight_route_graph,
#                                   source="Source airport ID",
#                                   target="Destination airport ID",
#                                   edge_attr=True)
#g_ground_routes = nx.from_pandas_edgelist(df_ground_route_graph,
#                                   source="Source airport ID",
#                                   target="Destination airport ID",
#                                   edge_attr=True)
g_routes = nx.from_pandas_edgelist(df_route_graph,
                                   source="Source airport ID",
                                   target="Destination airport ID",
                                   edge_attr=True)

def find_airport(df_airports=df_airports, id: int = None, code: str = None, attribtes: list = ['Airport ID', 'Name', 'Latitude', 'Longitude']):
  """Find airport information.

    Parameters:
    df_airports (DataFrame): airports DataFrame.
                            Available columns are "Airport ID",
                            "Name", "City", "Country", "IATA",
                            "ICAO", "Latitude", "Longitude", "Altitude",
                            "Timezone", "DST", "Tz database time zone",
                            "Type", "Source"
    id (int): airport ID
    code (str): airport IATA or	ICAO code
    attribtes (list): desired attribtes to query

    Returns:
    dict: attribtes in dict
  """
  if id is not None:
    r = df_airports[df_airports['Airport ID'] == id]
  elif code is not None:
    r = df_airports[(df_airports['IATA'] == code) | (df_airports['ICAO'] == code)]
  return r.iloc[0][list(set(attribtes))].to_dict() if r.size else None

def find_shortest_connection(df_airports=df_airports, g_routes=g_routes,
                             departure_id=None, destination_id=None,
                             departure_code=None, destination_code=None,
                             max_legs=4):
  """Find available connection with the shortest distance.

    Parameters:
    df_airports (DataFrame): airports DataFrame.
                            Available columns are "Airport ID",
                            "Name", "City", "Country", "IATA",
                            "ICAO", "Latitude", "Longitude", "Altitude",
                            "Timezone", "DST", "Tz database time zone",
                            "Type", "Source"
    g_flight_routes (Graph): Graph of flight connections.
    departure_id (int): departure airport ID
    destination_id (int): destination airport ID
    departure_code (str): departure airport IATA or	ICAO code
    destination_code (str): destination airport IATA or	ICAO code

    Returns:
    list: a list of airport IDs to represent the avaiable connection.
  """
  max_legs = max_legs or 4

  if departure_id is None and departure_code is not None:
    info = find_airport(df_airports=df_airports, code=departure_code, attribtes=['Airport ID'])
    departure_id = info.get('Airport ID') if info is not None else None
  if destination_id is None and destination_code is not None:
    info = find_airport(df_airports=df_airports, code=destination_code, attribtes=['Airport ID'])
    destination_id = info.get('Airport ID') if info is not None else None

  def weight(a, b, c):
    # we prefer flight
    f = c.get('flight_distance', math.nan)
    g = c.get('ground_distance', math.nan)
    d = f if not math.isnan(f) else g
    return d

  if departure_id is not None and destination_id is not None:
    try:
      route = list(map(lambda i: int(i),
                   nx.shortest_path(
                     g_routes,
                     source=departure_id,
                     target=destination_id,
                     weight=weight)))
      return route if len(route)-1 <= max_legs else None
    except nx.NodeNotFound:
      pass
    except nx.NetworkXNoPath:
      pass
  return None