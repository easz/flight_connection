# Flight Connection

## Requirement

Install Python3 (e.g. with [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-python.html))

Install necessary python requirements:

~~~
pip install -r requirements.txt
pip install -r requirements-dev.txt
~~~

### Quick Start

~~~
$ npm install serverless

$ serverless plugin install -n serverless-python-requirements

$ serverless invoke local --function find_connection --data '{"from":"MUC", "to": "BRC"}'
~~~

The result of local invocation would be something like this...

~~~
Running "serverless" from node_modules
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"route\": [\"MUC\", \"BCN\", \"EZE\", \"BRC\"], \"explain\": \"A route with 3 legs is found\", \"aiports\": [\"Munich Airport\", \"Barcelona International Airport\", \"Ministro Pistarini International Airport\", \"San Carlos De Bariloche Airport\"]}"
}
~~~

### Data Source

https://openflights.org/data.html

The data is not really up to date.

### Tools / Python

 - networkx (alt.: igraph / graph-tool)
 - pandas
 - scikit-learn

### Detail

 - Use Serverless (e.g. AWS Lambda) to set up HTTP/REST
 - pre-generate graph to represent routes (see [Notebook](sandbox.ipynb))
   - flight distance calculated with Haversine Formula
   - ground travel distance is approximated with applying a factor on Haversine distance
 - flight route is always prefered when finding shortest path
 - The structure of input data:
~~~
    {
      from: <IATA or ICAO code of the departure airport>,
      to: <IATA or ICAO code of the destination airport>,
      max_flight_legs: <[Optional] maximal flight legs. Default: 4>,
      max_ground_legs: <[Optional] maximal ground legs. Default: 1>
    }
~~~
  - The structure of output data
~~~
    {
      "statusCode": <HTTP status code>,
      "headers": {
          "Content-Type": "application/json"
      },
      "body": {
        "route": <a list of airport IATA codes>,
        "aiports": <a list of corresponding airport name>,
        "explain": <explanation text>
    }
~~~