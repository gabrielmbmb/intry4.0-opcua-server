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


def create_path_if_not_exists(path: str):
    """Create a path (directories) if it does not exist

    Args:
        path (:obj:`str`): path
    """
    split = os.path.split(path)
    if not os.path.exists(split[0]):
        os.makedirs(path)


def file_exists(path: str) -> bool:
    """Check if the file exists.

    Args:
        path (:obj:`str`): path
    """
    if os.path.exists(path):
        return True

    return False


def write_bytes_to_file(to_write, path: str):
    """Write the bytes to specified path

    Args:
        to_write (): bytes to write.
        path (:obj:`str`): path of the file.
    """
    with open(path, "wb+") as f:
        f.write(to_write)
