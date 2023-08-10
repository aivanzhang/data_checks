from typing import Any


def write_metadata(file: str, metadata: Any):
    """
    Write metadata to a file
    """
    f = open(file, "w+")
    f.write(str(metadata))
    f.close()
