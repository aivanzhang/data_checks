"""
Context stored alongside the execution of a suite or check
"""


class ExecutionContext:
    def __init__(self):
        self._data = {"sys": {}}

    def set_sys(self, key, value):
        self._data["sys"][key] = value

    def get_sys(self, key):
        return self._data["sys"][key]

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        if key == "sys":
            raise ValueError("Cannot override 'sys' key")
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def items(self):
        return self._data.items()

    def __repr__(self):
        return repr(self._data)

    def __str__(self):
        return str(self._data)
