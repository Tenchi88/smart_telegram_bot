class User:
    def __init__(self, user_id, name=None, last_name=None):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name

    def __repr__(self):
        return '<{}.{}> {} id {user_id} {name} {last_name}'.format(
            self.__module__, type(self).__name__, type(self).__name__,
            user_id=self.user_id, name=self.name, last_name=self.last_name
        )
