from user_manager.user import User
import copy


class UserDialog:
    def __init__(self, user, nodes_tree):
        self.user = user
        self.nodes_tree = copy.deepcopy(nodes_tree)

    def __repr__(self):
        return '<{}.{}> {} with user \n{user}'.format(
            self.__module__, type(self).__name__, type(self).__name__,
            user=self.user
        )
