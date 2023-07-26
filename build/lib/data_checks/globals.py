from typing import Dict, Callable, Any

# Stores all available global rules
rule_registry: Dict[str, Callable[..., Any]] = {}
