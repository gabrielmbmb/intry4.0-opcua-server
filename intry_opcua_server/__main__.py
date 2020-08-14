import os
import click
import signal
import logging
from intry_opcua_server.server import OPCUAServer
from intry_opcua_server.files import file_exists, write_bytes_to_file
from intry_opcua_server.selfsigned import generate_selfsigned_cert

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
@click.option(
    "-lr",
    "--last-row-file",
    default="/var/intry-opcua-server/last_row.json",
    help="Name of the file in which the last row published by the server will be saved",
)
@click.option(
    "-ce",
    "--certificate",
    default="/var/intry-opcua-server/cert.der",
    help="Path of the certificate file",
)
@click.option(
    "-pk",
    "--private-key",
    default="/var/intry-opcua-server/key.pem",
    help="Path of the private key file",
)
@click.option(
    "-mt", "--min-time", default=30, help="Min time elapsed between variable updates"
)
def main(
    endpoint,
    server_name,
    csv_dir,
    logging_level,
    last_row_file,
    certificate,
    private_key,
    min_time,
):
    # Get config from environment variables. If not provided takes the default value.
    _endpoint = os.getenv("OPCUA_SERVER_ENDPOINT", endpoint)
    _server_name = os.getenv("OPCUA_SERVER_NAME", server_name)
    _csv_dir = os.getenv("OPCUA_SERVER_CSV_DIR", csv_dir)
    _logging_level = os.getenv("OPCUA_SERVER_LOGGING_LEVEL", logging_level)
    _last_row_file = os.getenv("OPCUA_LAST_ROW_FILE", last_row_file)
    _certificate = os.getenv("OPCUA_CERTIFICATE", certificate)
    _private_key = os.getenv("OPCUA_PRIVATE_KEY", private_key)
    _min_time = os.getenv("OPCUA_MIN_TIME", min_time)

    # Set logger level
    logger.setLevel(_logging_level)

    if not file_exists(_certificate) and not file_exists(_private_key):
        cert_der, pk_pem = generate_selfsigned_cert("intry-opcua-server")
        write_bytes_to_file(cert_der, _certificate)
        write_bytes_to_file(pk_pem, _private_key)

    # Create OPC UA Server
    server = OPCUAServer(
        endpoint=_endpoint,
        server_name=_server_name,
        last_row_file=_last_row_file,
        logger=logger,
        certificate=_certificate,
        private_key=_private_key,
        min_time=_min_time,
    )
    server.start()

    # register SIGINT to stop the server
    def signal_handler(sig, frame):
        server.stop()

    signal.signal(signal.SIGINT, signal_handler)

    # Start exposing variables from CSVs via OPC UA Server
    server.variable_values_from_csvs(_csv_dir)


if __name__ == "__main__":
    main()
