class Dataset(object):
    def __init__(self, data_dict: dict):
        self.__dict__.update(data_dict)

    def __getitem__(self, key: str):
        return self.__dict__[key]
