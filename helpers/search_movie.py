movies = {
    'Идеальное убийство':
        {
            'genre': ['триллер', 'драма'],
            'actors': ['Майкл Дуглас', 'Гвинет Пэлтроу', 'Вигго Мортенсен'],
            'director': ['Эндрю Дэвис']
        },
    'Траффик':
        {
            'genre': ['криминал', 'драма', 'триллер'],
            'actors': [
                'Майкл Дуглас', 'Бенисио дель Торо',
                'Дон Чидл', 'Кэтрин Зета-Джонс',
                'Дэннис Куэйд'
            ],
            'director': ['Стивен Содерберг']
        },
    'Человек-муравей':
        {
            'genre': ['боевик'],
            'actors': [
                'Майкл Дуглас', 'Пол Радд',
                'Эванджелин Лилли', 'Кори Столл',
                'Майкл Пенья'
            ],
            'director': ['Пейтон Рид']
        },
    'Патрик Мелроуз':
        {
            'genre': ['драма'],
            'actors': [
                'Бенедикт Камбербэтч', 'Дженнифер Джейсон Ли',
                'Хелен Флинт'
            ],
            'director': ['Стивен Смоллвуд']
        },
    'Мстители: Война бесконечности':
        {
            'genre': ['фантастика', 'фэнтези', 'боевик', 'приключения'],
            'actors': [
                'Роберт Дауни', 'Крис Хемсворт',
                'Марк Руффало', 'Крис Эванс',
                'Бенедикт Камбербэтч'
            ],
            'director': ['Энтони Руссо', 'Джо Руссо']
        },
    'Тор: Рагнарёк':
        {
            'genre': ['фантастика', 'комедия', 'боевик', 'приключения'],
            'actors': [
                'Том Хиддлстон', 'Крис Хемсворт',
                'Марк Руффало', 'Энтони Хопкинс',
                'Бенедикт Камбербэтч'
            ],
            'director': ['Тайка Вайтити']
        },
    'Игра в имитацию':
        {
            'genre': ['драма'],
            'actors': [
                'Бенедикт Камбербэтч', 'Кира Найтли'

            ],
            'director': ['Мортен Тильдум']
        },
}


def find_movie(genres, names):
    res = []
    for movie in movies:
        genre_ok, name_ok = True, True
        info = '_' + movie + '_  ('

        genre_ok = False
        for movie_genre in movies[movie]['genre']:
            if movie_genre.lower() in genres:
                info += '*' + movie_genre + '*, '
                genre_ok = True
            else:
                info += movie_genre + ', '
        if not genre_ok and len(genres):
            continue
        info = info[:-2] + ')\n'

        name_ok = False
        info += 'Режиссер: '
        for director in movies[movie]['director']:
            if director.lower() in [v['full'] for v in names]:
                if not name_ok:
                    name_ok = True
                info += '*' + director + '*, '
            else:
                info += director + ', '
        info = info[:-2] + '\n'
        info += 'Актеры: '
        for actor in movies[movie]['actors']:
            if actor.lower() in [v['full'] for v in names]:
                info += '*' + actor + '*, '
                name_ok = True
            else:
                info += actor + ', '
        info = info[:-2] + '\n'
        if not name_ok and len(names):
            continue
        else:
            res.append(info)
    return res[:3]


if __name__ == '__main__':
    gen = []
    act = ['майкл дуглас']
    print(find_movie(gen, act))
