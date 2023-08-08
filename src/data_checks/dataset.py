class Dataset(object):
    def __init__(self, data_dict: dict):
        self.__dict__.update(data_dict)
