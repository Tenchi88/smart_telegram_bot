from nodes.answer_message import AnswerMessage


class Caller:
    def __init__(self):
        self.status = ''

    def final(self):
        return AnswerMessage(
            text='Благодарю вас за уделенное время. Всего доброго. До '
                 'свидания.\n[Статус: {}]'.format(self.status),
            go_to='final'
        )

    def wrong_data(self, message, answer_params):
        self.status = 'Некорректные данные, физ.лицо'
        return '[Некорректные данные, физ.лицо]'

    def fired(self, message, answer_params):
        return 'Подскажите, пожалуйста, Вы можете предоставить контактные ' \
               'данные сотрудника, с кем можно пообщаться по этому вопросу?'

    def new_contact(self, message, answer_params):
        return 'Уточните, пожалуйста, ФИО и контактный номер телефона?'
    #TODO add new contact parser

    def not_actual(self, message, answer_params):
        self.status = 'Неактуальный номер'
        return self.final()

    def ask_recall(self, message, answer_params):
        return 'Скажите, пожалуйста, когда Вам удобно перезвонить?'

    def recall(self, message, answer_params):
        self.status = 'Отложенный'
        return self.final()

    def no_recall(self, message, answer_params):
        return self.final()

    def contract_terminated(self, message, answer_params):
        return 'Скажите, пожалуйста, по какой причине?'

    def exchange(self, message, answer_params):
        return AnswerMessage(
            text='Я предлагаю обменятся вам контактами, чтобы мы могли сделать ' \
                 'Вам интересное предложение',
            go_to='check_person'
        )

    def wrong_contact(self, message, answer_params):
        self.status = 'Некорректные контактые данные'
        return self.final()

    def check_person(self, message, answer_params):
        return 'Скажите, пожалуйста, вы явлетесь контактным лицом по ' \
               'договору на услуги связи между компанией ХХХ (Наименование ' \
               'смотрим в анкете) и Ростелеком?'

    def ask_contact(self, message, answer_params):
        return 'Подскажите, пожалуйста, с кем можно пообщаться по этому ' \
               'вопросу? Уточните, пожалуйста, ФИО и контактный номер ' \
               'Вашего коллеги?'

    def no_contact(self, message, answer_params):
        self.status = 'Некорректные контактные данные'
        return self.final()

    def add_contact(self, message, answer_params):
        self.status = 'Уточняем новый контакт'
        return self.final()

    def switch_person(self, message, answer_params):
        self.status = 'Переключение на другой контакт'
        return self.final()

    def get_name(self, message, answer_params):
        return 'Скажите, пожалуйста, как я могу к вам обращаться? ' \
               'Уточните, пожалуйста, Вашу Фамилию Имя Отчество?'

    def get_position(self, message, answer_params):
        return '{ИО}, уточните, пожалуйста: Вашу должность?'

    def check_email(self, message, answer_params):
        #TODO check email in db
        return AnswerMessage(
            text='{ИО}, уточните, пожалуйста, уктуален ли email-адрес '
                 'ХХХХ@ХХХ.ХХХ ?',
            go_to='email_correct'
        )

    def email_wrong(self, message, answer_params):
        return '{ИО}, уточните, пожалуйста: Ваш email-адрес, по которому ' \
               'вам удобнее получать письма от Ростелеком? (это может быть ' \
               'как ваш личный email, так и рабочий)'

    def fill_in_email(self, message, answer_params):
        return '{ИО}, уточните, пожалуйста: Ваш email-адрес, по которому ' \
               'вам удобнее получать письма от Ростелеком? (это может быть ' \
               'как ваш личный email, так и рабочий)'

    def email_correct(self, message, answer_params):
        return AnswerMessage(
            text='{ИО}, уточните, пожалуйста: Есть ли у вас дополнительный '
                 'номер для связи?',
            go_to='get_2_number'
        )

    def get_2_number(self, message, answer_params):
        return '{ИО}, уточните, пожалуйста: Есть ли у вас дополнительный ' \
               'номер для связи?'

    def add_2_number(self, message, answer_params):
        return AnswerMessage(
            text='{ИО}, уточните, пожалуйста: Есть ли у вас дополнительный '
               'email для связи?',
            go_to='no_2_number'
        )

    def no_2_number(self, message, answer_params):
        return AnswerMessage(
            text='{ИО}, уточните, пожалуйста: Есть ли у вас дополнительный '
               'email для связи?',
            go_to='get_2_email'
        )

    def get_2_email(self, message, answer_params):
        return self.final()

    def add_2_email(self, message, answer_params):
        self.status = 'Успешный вызов'
        return self.final()

    def no_2_email(self, message, answer_params):
        self.status = 'Успешный вызов'
        return self.final()
