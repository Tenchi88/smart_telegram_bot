import random
from user_manager.yargy_ner import (yargy_get_channel, yargy_smart_home,
                                    name_extractor, yargy_get_genre)
from helpers.search_movie import find_movie
from use_cases import caller


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

        # Move it
        self.available_channels = [
            'Первый',
            'Россия 24',
            'ТВЦ',
            'НТВ',
            'ТНТ',
            'СТС',
            'Культура',
            'Дождь',
            'РенТВ'
        ]
        self.available_genres = [
            'новости',
            'новостной',
            'фильмы',
            'комедийный',
            'культура',
            'мультики',
            'мультфильмы',
            'политика',
            'природа',
        ]
        self.available_movie_genres = [
            'ужасы',
            'ужастики',
            'мелодрама',
            'мелодраму',
            'комедия',
            'комедию',
            'боевик',
            'триллер',
            'мультик',
            'мультфильм'
        ]

        self.available_movies = [
            'Форсаж',
            'Гарри Поттер',
            'Большая игра 2017',
            'Стражи Галактики 2',
            'Стражи Галактики',
            'Большая игра',
            'Пираты карибского моря',
        ]

        self.available_series_genre = [
            'ужасы',
            'ужастики',
            'мелодрама',
            'мелодраму',
            'комедия',
            'комедийный',
            'военные сериалы',
            'военный',
            'мультик',
            'мультсериал',
            'ТВ-шоу'
        ]

        self.available_series = [
            'Друзья',
            'Игра престолов',
            'Мир дикого запада',
            'Готэм',
            'Черное зеркало'
        ]

        self.smart_home_status = {
            'Ванная': {
                'Камера': False,
                'Свет': False,
                'Розетка': False,
            },
            'Гостевая': {
                'Камера': False,
                'Свет': False,
                'Розетка': False,
            },
            'Корридор': {
                'Камера': False,
                'Свет': False,
                'Розетка': False,
            },
            'Кухня': {
                'Камера': False,
                'Свет': False,
                'Розетка': False,
            },
            'Спальня': {
                'Камера': False,
                'Свет': False,
                'Розетка': False,
            },
            'Холл': {
                'Камера': False,
                'Свет': False,
                'Розетка': False,
            },
        }

        self.iptv_section = ''

        self.caller = caller.Caller()

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

    def get_channels(self, message, answer_params):
        res = 'Доступны каналы:\n'
        for ch in self.available_channels:
            res += '- ' + ch + '\n'
        return res

    def get_genre(self, message, answer_params):
        for genre in self.available_genres:
            if genre.lower() in message.lower():
                return '[Открывается жанр {}]'.format(genre)
        return 'Жанр не найден'

    def switch_to_channel(self, message, answer_params):
        return 'Включается канал {}'.format(yargy_get_channel(message))
        # for channel in self.available_channels:
        #     if channel.lower() in message.lower():
        #         return '[Включается канал {}]'.format(channel)
        # return 'Канал не найден'

    def what_to_watch(self, message, answer_params):
        answ = ''
        some_answ = False
        if len(self.iptv_section):
            answ = 'Ищем в разделе {}\n'.format(self.iptv_section)
        names = name_extractor(message)
        if len(names):
            answ += 'Ищем по актерам/режиссерам: '
            for n in [v['full'] for v in names]:
                answ += n + ', '
            answ = answ[:-2] + '\n'
            some_answ = True
        genres = yargy_get_genre(message)
        if len(genres):
            answ += 'Ищем по жанрам: '
            for g in genres:
                answ += g + ', '
            answ = answ[:-2] + '\n'
            some_answ = True
        if some_answ:
            search_results = find_movie(genres, names)
            if len(search_results):
                answ = 'Результаты поиска:\n'
                for r in search_results:
                    answ += r + '\n'
                return answ
            return answ
        return answ + 'Ищем в разделе по запросу "{}"'.format(message)

    def get_movie_genre(self, message, answer_params):
        for genre in self.available_movie_genres:
            if genre.lower() in message.lower():
                return '[Открывается жанр {}]'.format(genre)
        return 'Жанр не найден'

    def switch_to_movie(self, message, answer_params):
        for movie in self.available_movies:
            if movie.lower() in message.lower():
                return '[Открывается фильм {}]'.format(movie)
        return 'Фильм не найден'

    def get_series_genre(self, message, answer_params):
        for genre in self.available_series_genre:
            if genre.lower() in message.lower():
                return '[Открывается жанр {}]'.format(genre)
        return 'Жанр не найден'

    def switch_to_series(self, message, answer_params):
        for series in self.available_series:
            if series.lower() in message.lower():
                return '[Открывается сериал {}]'.format(series)
        return 'Сериал не найден'

    def smart_home(self, message, answer_params):
        actions = yargy_smart_home(message)
        res = ''
        for action in actions:
            res += 'Команда: [{}]\nОбъект: [{}]\nМесто: [{}]\n'.format(
                    action['Действие'], action['Объект'], action['Место']
                )
            obj = None
            if action['Объект'] in ['свет', 'лампочка']:
                obj = 'Свет'
            elif action['Объект'] in ['камера', 'видеокамера']:
                obj = 'Камера'
            elif action['Объект'] in ['розетка']:
                obj = 'Розетка'

            place = None
            if action['Место'] in ['ванна', 'ванная']:
                place = 'Ванная'
            elif action['Место'] in ['гостев']:
                place = 'Гостевая'
            elif action['Место'] in ['коридор']:
                place = 'Корридор'
            elif action['Место'] in ['кухня']:
                place = 'Кухня'
            elif action['Место'] in ['спальня']:
                place = 'Спальня'
            elif action['Место'] in ['холл']:
                place = 'Холл'

            act = None
            if action['Действие'] in ['выключить', 'отключить']:
                act = False
            elif action['Действие'] in ['включить']:
                act = True

            if obj is not None and place is not None and act is not None:
                self.smart_home_status[place][obj] = act

        for place in self.smart_home_status:
            state = ''
            if self.smart_home_status[place]['Камера']:
                state += '🎥'
            if self.smart_home_status[place]['Свет']:
                state += '💡'
            if self.smart_home_status[place]['Розетка']:
                state += '🔌'
            if state != '':
                res += '\n{}: {}'.format(place, state)
        return res

    def open_tv(self, message, answer_params):
        self.iptv_section = 'ТВ'
        return '[открылся раздел Телевидение]'

    def open_series(self, message, answer_params):
        self.iptv_section = 'Сериалы'
        return '[Открывается раздел Сериалы]'

    def open_movies(self, message, answer_params):
        self.iptv_section = 'Фильмы'
        return '[Открывается раздел Фильмы]'

    def open_main(self, message, answer_params):
        self.iptv_section = ''
        return '[Открывается Главная страница]'
