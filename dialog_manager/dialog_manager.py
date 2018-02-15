from user_manager.user_manager import UserManager
from dialog_manager.user_dialog import UserDialog
from nodes.nodes_tree_generator import NodesTreeGenerator


class DialogManager:
    def __init__(self, nodes_tree):
        self.users = UserManager()
        self.dialog = {}

        self.nodes_tree = nodes_tree
        self.nodes_tree.train_tree(self.nodes_tree.root_node)
        print('Classifiers are trained')

    def __repr__(self):
        return '<{}.{}> {}'.format(
            self.__module__, type(self).__name__, type(self).__name__
        )

    def create_user_dialog(self, user_info):
        print('user_id {user_id}'.format(user_id=user_info.id))
        user = self.users.get_user_by_id(user_info.id)
        if user is None:
            user = self.users.create_user(user_info)
        self.dialog[user_info.id] = UserDialog(user, self.nodes_tree)
        return self.dialog[user_info.id]

    # todo change to dict
    def get_user_dialog(self, user):
        if user.id in self.dialog:
            return self.dialog[user.id]
        return self.create_user_dialog(user)

    def parse_message(self, message):
        dialog = self.get_user_dialog(
            message.from_user
        )
        msg = message.text
        print(dialog.user, msg)
        # self.logger.add_user_message(update.message)
        if msg == 'отмена':
            answer = dialog.nodes_tree.go_to_root(msg)
        else:
            answer = dialog.nodes_tree.parse_message(msg)
        print(answer)
        return answer, dialog.nodes_tree.current_node_name
