"""
Metadata Mixin for metadata-related functions
"""

from typing import Dict, Any, Optional
import inspect
from utils.metadata_utils import write_metadata


class MetadataMixin:
    def __init__(self, metadata_dir: Optional[str] = None):
        self.metadata = dict()
        self.metadata_dir = metadata_dir

    def set_metadata_dir(self, metadata_dir: Optional[str]):
        self.metadata_dir = metadata_dir

    def log_metadata(
        self,
        metadata: Dict[str, Any],
        id: Optional[str] = None,
        write_to_file: Optional[str] = None,
        log_to_memory: bool = True,
    ):
        """
        Log metadata with its associated rule
        """
        metadata_id = inspect.stack()[1][3] if id is None else id
        if log_to_memory:
            self.metadata[metadata_id] = metadata
        if write_to_file is not None:
            write_metadata(write_to_file, metadata)

    def write_metadata(self, file: str):
        write_metadata(file, self.metadata)
