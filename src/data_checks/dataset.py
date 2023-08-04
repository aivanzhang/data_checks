class Dataset(object):
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)
