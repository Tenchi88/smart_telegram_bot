class DialogManager:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return '<{}.{}> {} user_id={}'.format(
            self.__module__, type(self).__name__, type(self).__name__,
            self.user_id
        )