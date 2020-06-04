import os
from typing import List


def get_csvs_in_dir(path: str) -> List[str]:
    """Gets a list of csv files inside the specified path.

    Args:
        path (str): path to directory containing csv files.

    Returns:
        list: containing paths to csv files contained in the specified path.
    """
    if os.path.isfile(path):
        pass

    csvs = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csvs.append(os.path.join(path, file))

    return csvs
