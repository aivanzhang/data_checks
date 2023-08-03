from typing import Any
from dataclasses import make_dataclass


class Dataset(object):
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)
