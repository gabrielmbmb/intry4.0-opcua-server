from typing import List
from opcua import Server, ua


class OPCUAServer:
    """An OPC UA server which reads variables from a csv file and exposes it.

    Args:
        endpoint (:obj:`str`): OPC UA server endpoint. Defaults to
            'opc.tcp://0.0.0.0:4840/intry4.0/server/'.
        server_name (:obj:`str`): OPC UA server name. Defaults to
            'InTry 4.0 OPC UA Server'.
        security_policy (:obj:`list`): Array which contains
            `opcua.ua.SecurityPolicyType` available in the server. Defaults to
            [
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_Sign,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ]
        ns_uri(:obj:`str`): the namespace URI where all the variables will be added.
            Defaults to 'urn:intry4.0:server'.

    Attributes:
        _server (opcua.Server): the OPC UA server.
        _ns_index (): the namespace index where all the variables will be added.
        _stop (bool): flag variable that controls the infinite loop of variable
            updating.
    """

    def __init__(
        self,
        endpoint: str = "opc.tcp://0.0.0.0:4840/intry4.0/server/",
        server_name: str = "InTry 4.0 OPC UA Server",
        security_policy: List[ua.SecurityPolicyType] = None,
        ns_uri: str = "O",
    ):
        if security_policy is None:
            _security_policy = [
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_Sign,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ]

        self._server = Server()
        self._server.set_endpoint(endpoint)
        self._server.set_security_policy(_security_policy)
        self._ns_index = self._server.register_namespace(ns_uri)
        self._stop = False

    def add_variables_from_dataframe(self, df):
        """Adds the variables listed in the dataframe to the OPC UA Server.

        Args:
            df (pandas.core.frame.DataFrame): dataframe with variables to be exposed
                by the OPC UA server.
        """
        pass

    def start(self):
        """Starts the OPC UA server execution."""
        self._server.start()

    def stop(self):
        """Stops the OPC UA server execution."""
        self._stop = True
        self._server.stop()
