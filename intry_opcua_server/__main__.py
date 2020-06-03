import click
import signal
from intry_opcua_server.server import OPCUAServer


@click.command(name="start")
@click.option(
    "-e",
    "--endpoint",
    default="opc.tcp://0.0.0.0:4840/intry4.0/server/",
    help="OPC UA server endpoint",
)
@click.option(
    "-sn", "--server-name", default="OPC UA server name", help="OPC UA server name"
)
def main(endpoint, server_name):
    server = OPCUAServer(endpoint=endpoint, server_name=server_name)
    server.start()

    # register SIGINT to stop the server
    def signal_handler(sig, frame):
        server.stop()

    signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    main()
