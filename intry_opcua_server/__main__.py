import os
import click
import signal
import logging
from intry_opcua_server.server import OPCUAServer

# Create a logging formatter
log_format = "[%(asctime)s][%(levelname)s]: %(message)s"
formatter = logging.Formatter(log_format)

# Create a logger
logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


@click.command()
@click.option(
    "-e",
    "--endpoint",
    default="opc.tcp://0.0.0.0:4840/intry4.0/server/",
    help="OPC UA server endpoint",
)
@click.option(
    "-sn", "--server-name", default="OPC UA server name", help="OPC UA server name"
)
@click.option(
    "-cd",
    "--csv-dir",
    default="./csvs",
    help="The path of the directory containing the CSVs from which variables will be created in the OPC UA server",
)
@click.option(
    "-ll",
    "--logging-level",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
)
def main(endpoint, server_name, csv_dir, logging_level):
    # Get config from environment variables. If not provided takes the default value.
    _endpoint = os.getenv("OPCUA_SERVER_ENDPOINT", endpoint)
    _server_name = os.getenv("OPCUA_SERVER_NAME", server_name)
    _csv_dir = os.getenv("OPCUA_SERVER_CSV_DIR", csv_dir)
    _logging_level = os.getenv("OPCUA_SERVER_LOGGING_LEVEL", logging_level)

    # Set logger level
    logger.setLevel(_logging_level)

    # Create OPC UA Server
    server = OPCUAServer(endpoint=_endpoint, server_name=_server_name, logger=logger)
    server.start()

    # register SIGINT to stop the server
    def signal_handler(sig, frame):
        server.stop()

    signal.signal(signal.SIGINT, signal_handler)

    # Start exposing variables from CSVs via OPC UA Server
    server.variable_values_from_csvs(_csv_dir)


if __name__ == "__main__":
    main()
