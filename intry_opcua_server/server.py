import time
import logging
import pandas as pd
from typing import List
from opcua import Server, ua
from intry_opcua_server.files import get_csvs_in_dir
from intry_opcua_server.util import str_to_date


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
        object_name(:obj:`str`): name of the OPC UA object that will be created to hold
            all variables. Defaults to 'variables'.
        logger(:obj:`logging.Logger`): logger to be used. Defaults to None.

    Attributes:
        _server (opcua.Server): the OPC UA server.
        endpoint (str): OPC UA server endpoint.
        _ns_index (): the namespace index where all the variables will be added.
        _object ()
        _stop (bool): flag variable that controls the infinite loop of variable
            updating.
    """

    def __init__(
        self,
        endpoint: str = "opc.tcp://0.0.0.0:4840/intry4.0/server/",
        server_name: str = "InTry 4.0 - OPC UA Server",
        security_policy: List[ua.SecurityPolicyType] = None,
        ns_uri: str = "urn:intry:opcua:server",
        object_name: str = "variables",
        logger=None,
    ):
        if security_policy is None:
            _security_policy = [
                ua.SecurityPolicyType.NoSecurity,
                ua.SecurityPolicyType.Basic256Sha256_Sign,
                ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ]

        self._server = Server()
        self.endpoint = endpoint
        self._server.set_endpoint(self.endpoint)
        self._server.set_security_policy(_security_policy)
        self._ns_index = self._server.register_namespace(ns_uri)
        self._object = self._server.nodes.objects.add_object(
            self._ns_index, object_name
        )
        self._logger = logger or logging.getLogger(__name__)
        self._stop = False

    def _add_variable(self, name, value):
        """Adds a variable to the OPC UA server.

        Args:
            name (:obj:`str`): name of the variable.
            value (int or float): initial value of the variable.

        Returns:
            opcua.common.node.Node: the created variable in the OPC UA server.
        """
        return self._object.add_variable(self._ns_index, name, value)

    def variable_values_from_csvs(self, csv_dir):
        """Creates variables inside the OPC UA server from the CSVs contained in the
        specified directory. Then, each row of the provided CSVs will be read to update
        the value of each variable.

        csv_dir (str): path of the directory containing CSVs.
        """
        csvs = get_csvs_in_dir(csv_dir)
        self._logger.debug(f"CSV files inside {csv_dir}: {len(csvs)}")

        variable_name_node = {}
        for (index, csv) in enumerate(csvs):
            if self._stop:
                break

            self._logger.debug(f"Reading file {csv}")
            df = pd.read_csv(csv, index_col="date")

            # If first CSV, create variables in the OPC UA Server
            if index == 0:
                self._logger.debug(
                    f"First csv readed: {csv}. Creating {len(df.columns)} OPC UA variables from it..."
                )

                for column in df.columns:
                    first_value = df[column].iloc[0]
                    # remove the first row because its going used for initial value
                    df = df.iloc[1:]
                    self._logger.debug(
                        f"Adding variable [{column}] with initial value <{first_value}>"
                    )
                    variable_name_node[column] = self._add_variable(column, first_value)

            # iterate over the rows in the dataframe for updating the value of each variable
            time_between_update = 0
            last_index = None
            for (index, row) in df.iterrows():
                if self._stop:
                    break

                # Calculate the time to sleep between each update with the date of the
                # last row and this row.
                if last_index is not None:
                    time_between_update = (
                        str_to_date(index) - str_to_date(last_index)
                    ).total_seconds()

                time.sleep(time_between_update)
                self._logger.debug(
                    f"Time of {time_between_update} elapsed. Updating variable values..."
                )
                for (column, node) in variable_name_node.items():
                    node.set_value(row[column])

                last_index = index

    def start(self):
        """Starts the OPC UA server execution."""
        self._logger.info(f"Starting OPC UA server. Listening on {self.endpoint}")
        self._server.start()

    def stop(self):
        """Stops the OPC UA server execution."""
        self._logger.info("Stopping OPC UA server...")
        self._stop = True
        self._server.stop()
