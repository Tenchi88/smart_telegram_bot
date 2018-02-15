from user_manager.user import User


class UserManager:
    def __init__(self):
        self.user = {}

    def __repr__(self):
        return '<{}.{}> {}'.format(
            self.__module__, type(self).__name__, type(self).__name__
        )

    def create_user(self, user):
        if user.id in self.user:
            raise TypeError('User with id {id} already exists', user.id)
        self.user[user.id] = User(
            user.id,
            name=user.first_name,
            last_name=user.last_name
        )
        return self.user[user.id]

    def get_user_by_id(self, user_id):
        if user_id in self.user:
            return self.user[user_id]
        return None
