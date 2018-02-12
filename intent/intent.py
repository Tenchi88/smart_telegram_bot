class Intent:
    def __init__(self, name, data_set=None):
        if type(name) is not str:
            raise TypeError('Intent name must be str', name)
        self.name = name
        self.data_set = data_set
        self.entities = {}

    def __repr__(self):
        return '<{}.{}> {} with name {}'.format(
            self.__module__, type(self).__name__, type(self).__name__,
            self.name
        )
