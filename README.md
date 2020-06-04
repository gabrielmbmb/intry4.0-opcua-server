# InTry 4.0 - OPC UA Server

An OPC UA server created to simulate data acquisition from different sensors. The simulation 
is based on reading a set of CSVs with data from different sensors that will be used to update 
the value of the variables exposed by the server.

## Docker

A Dockerfile is provided in order to build a Docker image. The image can be built with the following command:

    docker build . -t <tag>

The configuration can be provided via environment variables:

* __*OPCUA_SERVER_ENDPOINT*__: the server endpoint where the server will be served.
* __*OPCUA_SERVER_NAME*__: the server name.
* __*OPCUA_SERVER_CSV_DIR*__: path to directory containing CSVs with sensor data.
* __*OPCUA_SERVER_LOGGING_LEVEL*__: log level.

## Author

* Gabriel Martín Blázquez <gmartin_b@usal.es>