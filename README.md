# Flight Connection

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
    "body": "{\"route\": [346, 1218, 3988, 2513], \"aiports\": [\"Munich Airport\", \"Barcelona International Airport\", \"Ministro Pistarini International Airport\", \"San Carlos De Bariloche Airport\"]}"
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
 - pre-Generate graph to represent routes
   - flight distance calculated with Haversine Formula
   - ground travel distance is approximated with applying a factor on Haversine distance
 - flight route is always prefered when finding shortest path