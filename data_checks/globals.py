from typing import Dict, Callable, Any

# Stores all available global ingestors
ingestor_registry: Dict[str, Callable[..., Any]] = {}
