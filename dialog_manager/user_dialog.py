import copy
from telegram.message import Message as TelegramMessage
from nodes.answer_message import AnswerMessage

from user_manager.user import User
from nodes.nodes_tree import NodesTree
import nodes.external_node_functions


class UserDialog:
    def __init__(
            self,
            user: User,
            nodes_tree: NodesTree
    ):
        self.user = user
        self.nodes_tree = copy.deepcopy(nodes_tree)
        self.messages = []
        self.mode = 'normal'
        self.allowed_commands = ['auth']
        self.available_modes = {
            'normal': self.on_text_message,
            'auth_requested': self.check_user_id_and_send_code,
            'user_auth': self.user_auth
        }

    def __repr__(self):
        return '<{}.{}> {} with user \n{user}'.format(
            self.__module__, type(self).__name__, type(self).__name__,
            user=self.user
        )

    def user_auth(self, msg):
        if self.user.enter_auth_code(msg):
            self.mode = 'normal'
            return AnswerMessage(
                text='Аутентификация прошла успешно. Теперь вам доступны все '
                     'сервисы.'
            )
        return AnswerMessage(
            text='Ошибка аутентификация попробуйте ввести код-пароль еще раз. '
                 'Для повторной отправки кода на ваш e-mail отправьте команду '
                 '/auth'
        )

    def auth(self):
        self.mode = 'auth_requested'
        return AnswerMessage(
            text='Пожалуйста, введите ваш номер лицевого счета'
        )

    def check_user_id_and_send_code(self, msg):
        # TODO check user info, find e-mail
        # TODO send PIN to e-mail
        self.mode = 'user_auth'
        self.user.gen_auth_code()
        return AnswerMessage(
            text='Код аутентификации отправлен на ваш e-mail указанный в личном'
                 ' кабинете: '
                 '{}'.format(self.user.auth_code)
        )

    def on_text_message(self, msg):
        # parse text messages
        answer = self.nodes_tree.parse_message(msg)
        if answer.function is not None:
            print('function:', answer)
            answer = eval(
                'self.user.' + answer.function
            )(message=msg, answer_params=answer)
            if type(answer) is AnswerMessage:
                return answer
            return AnswerMessage(text=answer)
        return answer

    def on_message(
            self,
            message: TelegramMessage
    ):
        msg = message.text
        print(self.user, msg)
        # TODO save msg to db
        self.messages.append(msg)
        # self.logger.add_user_message(update.message)

        # parse commands
        if (
                len(message.entities)
                and message.entities[0].type == 'bot_command'
        ):
            if message.text[1:] in self.allowed_commands:
                answer = eval('self.{}()'.format(message.text[1:]))
            else:
                answer = AnswerMessage('Недопустимая команда')

        else:
            if msg == 'отмена':
                self.mode = 'normal'
                answer = self.nodes_tree.go_to_root(msg)
            else:
                answer = self.available_modes[self.mode](msg)

        print(answer)
        return answer, self.nodes_tree.current_node_name
