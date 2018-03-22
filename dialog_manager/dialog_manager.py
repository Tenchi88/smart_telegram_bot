from telegram.user import User as TelegramUser
from telegram.message import Message as TelegramMessage

from user_manager.user_manager import UserManager
from dialog_manager.user_dialog import UserDialog
from nodes.nodes_tree import NodesTree
from nodes.answer_message import AnswerMessage
from nodes.classification_node import ClassificationNode


class DialogManager:
    def __init__(self, nodes_tree: NodesTree):
        self.users = UserManager()
        self.dialog = {}

        self.nodes_tree = nodes_tree
        self.nodes_tree.train_tree(self.nodes_tree.root_node)
        print('Classifiers are trained')

    def __repr__(self):
        return '<{}.{}> {}'.format(
            self.__module__, type(self).__name__, type(self).__name__
        )

    def create_user_dialog(self, user_info: TelegramUser) -> UserDialog:
        print('user_id {user_id}'.format(user_id=user_info.id))
        user = self.users.get_user_by_id(user_info.id)
        if user is None:
            user = self.users.create_user(user_info)
        self.dialog[user_info.id] = UserDialog(user, self.nodes_tree)
        return self.dialog[user_info.id]

    # todo change to dict??
    def get_user_dialog(self, user: TelegramUser) -> UserDialog:
        if user.id in self.dialog:
            return self.dialog[user.id]
        return self.create_user_dialog(user)

    def parse_message(
            self,
            message: TelegramMessage
    ) -> (AnswerMessage, ClassificationNode):
        dialog = self.get_user_dialog(
            message.from_user
        )
        return dialog.on_message(message)
