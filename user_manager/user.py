import random


class User:
    def __init__(
            self,
            user_id: str,
            name: str=None,
            last_name: str=None
    ):
        self.user_id = user_id
        self.name = name
        self.last_name = last_name
        self.auth_code = str(random.randint(1000, 9999))
        self.auth_ok = False
        self.balance = random.randint(-300, 1000)

    def __repr__(self):
        return '<{}.{}> {} id {user_id} {name} {last_name}'.format(
            self.__module__, type(self).__name__, type(self).__name__,
            user_id=self.user_id, name=self.name, last_name=self.last_name
        )

    def enter_auth_code(self, code):
        if code == self.auth_code:
            self.auth_ok = True
        return self.auth_ok

    def gen_auth_code(self):
        self.auth_ok = False
        self.auth_code = str(random.randint(1000, 9999))
        self.balance = random.randint(-300, 1000)

    def get_balance(self, message, answer_params):
        if self.auth_ok:
            if self.balance >= 0:
                return 'Ваш баланс равен: {} рублей'.format(self.balance)
            else:
                return 'По вашему счету имеется задолжность: {} ' \
                       'рублей'.format(self.balance)
        else:
            return 'Необходимо авторизоваться чтобы узнать баланс. ' \
                   'Для начала авторизации отправьте команду /auth'
