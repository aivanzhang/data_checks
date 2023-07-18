import globals


def ingestor(name=""):
    """
    Decorator to register a function as an ingestor
    """

    def decorator_wrapper(func):
        globals.ingestor_registry[func.__name__] = func

        def decorator(*args, **kwargs):
            return func(*args, **kwargs)

        return decorator

    return decorator_wrapper


def ingest_from_registry(source: str):
    """
    Get ingestor from registry
    """
    if source in globals.ingestor_registry:
        return globals.ingestor_registry[source]
    else:
        raise ValueError(f"No ingestor found for {source}")
