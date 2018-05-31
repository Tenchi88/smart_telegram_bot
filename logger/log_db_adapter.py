# -*- coding: utf-8 -*-

import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

import datetime

Base = declarative_base()

user_services_table = sqlalchemy.Table(
    'user_services_table', Base.metadata,
    sqlalchemy.Column(
        'user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')
    ),
    sqlalchemy.Column(
        'service_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('services.id')
    )
)


class DialogLogEntry(Base):
    """
    Entry params:
    user_id - user ID
    time - Timestamp
    type - Entry type:
        - user message
        - user voice message
        - bot answer
        - classification
        - answer options
        - file
        - action
    text - Text data(depends on entry type)
    """

    __tablename__ = 'dialog_logs'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.Sequence('log_msg_id_seq'),
        primary_key=True
    )
    dialog_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('dialogs.id'), nullable=False
    )
    time = sqlalchemy.Column(sqlalchemy.String(30))
    type = sqlalchemy.Column(sqlalchemy.String(16))
    text = sqlalchemy.Column(sqlalchemy.Text)

    dialog = relationship('Dialog', back_populates='dialog_logs')

    def __repr__(self):
        return '<DialogLogEntry(id=\'{}\', dialog_id=\'{}\', time=\'{}\',' \
            ' type=\'{}\', text=\'{}\')>'.format(
                self.id, self.dialog_id, self.time, self.type, self.text
            )


class Dialog(Base):
    __tablename__ = 'dialogs'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.Sequence('dialog_id_seq'),
        primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False
    )
    time = sqlalchemy.Column(sqlalchemy.String(30))
    duration = sqlalchemy.Column(sqlalchemy.String(16))
    length = sqlalchemy.Column(sqlalchemy.Integer)

    dialog_logs = relationship('DialogLogEntry', back_populates='dialog')
    user = relationship('User', back_populates='dialogs')

    def __repr__(self):
        return '<Dialog(id=\'{}\', user_id=\'{}\', time=\'{}\', duration' \
            '=\'{}\', length=\'{}\')>'.format(
                self.id, self.user_id, self.time, self.duration, self.length
            )


class User(Base):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.Sequence('user_id_seq'), primary_key=True
    )
    telegram_user_id = sqlalchemy.Column(sqlalchemy.String(12))
    name = sqlalchemy.Column(sqlalchemy.String(64))
    balance = sqlalchemy.Column(sqlalchemy.Float)
    current_dialog_id = sqlalchemy.Column(sqlalchemy.Integer)

    dialogs = relationship('Dialog', back_populates='user')
    services = relationship(
        'Service', secondary=user_services_table, back_populates='users'
    )
    payments = relationship('Payment', back_populates='user')

    def __repr__(self):
        return '<User(id=\'{}\', telegram_user_id=\'{}\', name=\'{}\', ' \
            'balance=\'{}\',  current_dialog_id=\'{}\',' \
            '  services=\'{}\')>'.format(
                self.id, self.telegram_user_id, self.name, self.balance,
                self.current_dialog_id, self.services
            )


class Service(Base):
    __tablename__ = 'services'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.Sequence('service_id_seq'),
        primary_key=True
    )
    name = sqlalchemy.Column(sqlalchemy.String(30))
    description = sqlalchemy.Column(sqlalchemy.Text)
    monthly_payment = sqlalchemy.Column(sqlalchemy.Float)

    users = relationship(
        'User', secondary=user_services_table, back_populates='services'
    )

    def __repr__(self):
        return '<Service(id=\'{}\', name=\'{}\', description=\'{}\', ' \
            'monthly_payment=\'{}\')>'.format(
                self.id, self.name, self.description, self.monthly_payment
            )


class Payment(Base):
    __tablename__ = 'payments'
    id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.Sequence('payment_id_seq'),
        primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=False
    )
    time = sqlalchemy.Column(sqlalchemy.String(30))
    value = sqlalchemy.Column(sqlalchemy.Float)

    user = relationship('User', back_populates='payments')

    def __repr__(self):
        return '<Payment(id=\'{}\', user_id=\'{}\', time=\'{}\', ' \
            'value=\'{}\')>'.format(
                self.id, self.user_id, self.time, self.value
            )


class LogDBAdapter:
    _time_stamp_format = '%Y-%m-%d %H:%M:%S.%f'

    def __init__(
            self, db_type='sqlite', db_path='test.db',
            create_tables=False, sql_debug=False
    ):
        if not os.path.exists(os.path.dirname(db_path)):
            os.mkdir(os.path.dirname(db_path))
        db_string = '{}:///{}'.format(db_type, db_path)
        self.engine = create_engine(db_string, echo=sql_debug)
        self.metadata = sqlalchemy.MetaData()

        if create_tables:
            Base.metadata.create_all(self.engine)

        self.session_factory = sessionmaker(bind=self.engine)
        self.Session = scoped_session(self.session_factory)
        self.session = self.Session()

    @staticmethod
    def _show_something(get_function, header='', start_from=0):
        print('\n' + header)
        print('------------------------------------------------------')
        for entry in get_function(start_from=start_from):
            print(entry)
        print('------------------------------------------------------\n')

    def show_log(self, start_from=0):
        self._show_something(self.get_log, 'User messages in log:', start_from)

    def show_users(self, start_from=0):
        self._show_something(self.get_users, 'Users in DB:', start_from)

    def show_dialogs(self, start_from=0):
        self._show_something(self.get_dialogs, 'Dialogs in DB:', start_from)

    def show_services(self, start_from=0):
        self._show_something(self.get_services, 'Services in DB:', start_from)

    def show_payments(self, start_from=0):
        self._show_something(self.get_payments, 'Payments in DB:', start_from)

    def get_log(self, start_from=0):
        user_messages = self.session.query(DialogLogEntry).all()
        return user_messages[start_from:]

    def get_users(self, start_from=0):
        users = self.session.query(User).all()
        return users[start_from:]

    def get_dialogs(self, start_from=0):
        dialogs = self.session.query(Dialog).all()
        return dialogs[start_from:]

    def get_services(self, start_from=0):
        services = self.session.query(Service).all()
        return services[start_from:]

    def get_payments(self, start_from=0):
        payments = self.session.query(Payment).all()
        return payments[start_from:]

    def find_user_by_telegram_id(self, telegram_id):
        return self.session.query(User).filter_by(
            telegram_user_id=telegram_id
        ).first()

    def create_user(
            self, telegram_user_id, name=None,
            balance=None, auto_commit=True
    ):
        new_user = User(
            telegram_user_id=telegram_user_id,
            name=name,
            balance=balance
        )
        self.session.add(new_user)
        if auto_commit:
            self.commit()
        return new_user

    def user_with_telegram_id(self, telegram_id):
        user = self.find_user_by_telegram_id(telegram_id)
        if user is not None:
            return user
        # TODO: provide name from telegram account to this place
        return self.create_user(telegram_user_id=telegram_id)

    def find_dialog_by_id(self, dialog_id):
        return self.session.query(Dialog).filter_by(id=dialog_id).first()

    def create_dialog(
            self, user, time=datetime.timedelta(0),
            duration=0, length=0, auto_commit=True
    ):
        new_dialog = Dialog(
            user_id=user.id,
            time=str(time),
            duration=duration,
            length=length
        )
        self.session.add(new_dialog)
        self.commit()
        user.current_dialog_id = new_dialog.id
        if auto_commit:
            self.commit()
        return new_dialog

    def current_user_dialog(self, user, auto_commit=True):
        if user.current_dialog_id is not None:
            return self.find_dialog_by_id(dialog_id=user.current_dialog_id)
        return self.create_dialog(user=user, auto_commit=auto_commit)

    def current_dialog_by_telegram_id(self, telegram_id):
        user = self.user_with_telegram_id(telegram_id=telegram_id)
        current_dialog = self.current_user_dialog(user=user)
        return current_dialog

    def add(self, entry, auto_commit=True):
        current_dialog = self.current_dialog_by_telegram_id(entry['user_id'])
        log_entry = DialogLogEntry(
            dialog_id=current_dialog.id,
            time=entry['time'],
            type=entry['type'],
            text=entry['text']
        )
        self.session.add(log_entry)
        if current_dialog.length == 0:
            current_dialog.time = log_entry.time
        current_dialog.duration = str(
            datetime.datetime.strptime(log_entry.time, self._time_stamp_format)
            - datetime.datetime.strptime(
                current_dialog.time, self._time_stamp_format
            )
        )
        current_dialog.length = current_dialog.length + 1

        if auto_commit:
            self.commit()

    def commit(self):
        self.session.commit()

    def dirty_data(self):
        return self.session.dirty

    def new_data(self):
        return self.session.new

    def print_dirty_data(self):
        print('\nDirty data:')
        print(self.dirty_data())
        print('------------------------------------------------------\n')

    def print_new_data(self):
        print('New data:')
        print(self.new_data())
        print('------------------------------------------------------\n')

    def activate_service_for_user(self, user, service, auto_commit=True):
        print('Activate:', service, 'for', user)
        user.services.append(service)
        if auto_commit:
            self.commit()

    def find_service_by_name(self, service_name):
        return self.session.query(Service).filter_by(name=service_name).first()

    def create_service(
            self, name, description=None,
            monthly_payment=None, auto_commit=True
    ):
        new_service = Service(
            name=name,
            description=description,
            monthly_payment=monthly_payment
        )
        self.session.add(new_service)
        if auto_commit:
            self.commit()
        return new_service

    def create_payment(self, user, value, time=None, auto_commit=True):
        if time is None:
            time = str(datetime.datetime.now())
        new_payment = Payment(
            user_id=user.id,
            time=time,
            value=value
        )
        self.session.add(new_payment)
        if auto_commit:
            self.commit()
        return new_payment

    def check_balance_by_telegram_id(self, telegram_id):
        return self.find_user_by_telegram_id(telegram_id).balance

