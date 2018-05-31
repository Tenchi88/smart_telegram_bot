from yargy.interpretation import fact
from yargy import rule, and_, Parser
from yargy import or_
from yargy.predicates import caseless, normalized, dictionary

from natasha import NamesExtractor
from natasha.markup import show_markup, show_json


def name_extractor(msg):
    words = msg.split(' ')
    txt = ''
    for w in words:
        w = w[0].upper() + w[1:]
        txt += w + ' '
    txt.strip()

    extractor = NamesExtractor()
    matches = extractor(txt)
    spans = [_.span for _ in matches]
    facts = [_.fact.as_json for _ in matches]
    # show_markup(txt, spans)
    # show_json(facts)
    res = []
    for val in facts:
        if 'last' in val:
            if 'first' in val:
                new_val = val['first']
                if 'middle' in val:
                    new_val += ' ' + val['middle']
                new_val += ' ' + val['last']
            else:
                new_val = val['last']
            val['full'] = new_val
            res.append(val)
    return res


def yargy_get_genre(msg):
    Genre = fact(
        'Genre',
        ['genre']
    )

    GENRES = {
        'ужасы',
        'ужастики',
        'мелодрама',
        'комедия',
        'боевик',
        'триллер',
        'мультик',
        'мультфильм',
        'драма'
    }

    GENRES_NAME = dictionary(GENRES)
    GENRES_WORDS = or_(
        rule(normalized('жанр')),
        rule(normalized('раздел'))
    )
    GENRE_PHRASE = or_(
        rule(
            GENRES_NAME,
            GENRES_WORDS.optional()
        ),
        rule(
            GENRES_WORDS.optional(),
            GENRES_NAME
        )
    ).interpretation(
        Genre.genre.inflected()
    ).interpretation(
        Genre
    )

    res = []
    parser = Parser(GENRE_PHRASE)
    for match in parser.findall(msg):
        res.append(match.fact.genre)
    return res


def yargy_get_channel(msg):
    Channel = fact(
        'Channel',
        ['name']
    )

    CNANNELS = {
        'Первый',
        'Россия',
        'ТВЦ',
        'НТВ',
        'ТНТ',
        'СТС',
        'Культура',
        'Дождь',
        'Спас'
    }
    CNANNELS_NAME = dictionary(CNANNELS)
    CHANNEL_WORDS = or_(
        rule(normalized('канал')),
        rule(normalized('программа'))
    )
    CHANNEL_PHRASE = or_(
        rule(
            CHANNEL_WORDS,
            CNANNELS_NAME
        ),
        rule(
            CNANNELS_NAME,
            CHANNEL_WORDS.optional()
        )
    ).interpretation(
        Channel.name.inflected()
    ).interpretation(
        Channel
    )

    res = []
    parser = Parser(CHANNEL_PHRASE)
    for match in parser.findall(msg):
        # print(match.fact)
        for channel in CNANNELS:
            if channel.lower() in match.fact.name:
                res.append(channel)
    return res


def yargy_smart_home(msg):
    Do = fact(
        'Entity',
        ['action', 'object', 'place']
    )

    Actions = dictionary({
        'Включи',
        'Отключи',
        'Выключи'
    })

    Objects = dictionary({
        'Лампочку',
        'Свет',
        'Розетку',
        'Видеокамеру',
        'Камеру'
    })

    ObjectsList = or_(
        rule(Objects),
        rule(Objects, Objects),
    )

    Prep = dictionary(
        {
            'в',
            'на'
        }
    )

    Place = dictionary({
        'Гостевой',
        'Ванной',
        'спальной',
        'спальне',
        'холле',
        'коридоре',
        'кухне'
    })

    Room = {
        'комната'
    }

    ActionPhrase = or_(
        rule(
            Actions.interpretation(Do.action.normalized()),
            Objects.interpretation(Do.object.normalized()),
            Prep.optional(),
            Place.interpretation(Do.place.normalized()),
            rule(normalized('комната')).optional()
        ),
        rule(
            Actions.interpretation(Do.action.normalized()),
            Objects.interpretation(Do.object.normalized()),
            Prep.optional(),
            Place.interpretation(Do.place.normalized())
        ),
        rule(
            Prep.optional(),
            Place.interpretation(Do.place.normalized()),
            rule(normalized('комната')).optional(),
            Actions.interpretation(Do.action.normalized()),
            Objects.interpretation(Do.object.normalized())
        )
    ).interpretation(
        Do
    )

    res = []
    parser = Parser(ActionPhrase)
    for match in parser.findall(msg):
        res.append(
            {
                'Действие': match.fact.action,
                'Объект': match.fact.object,
                'Место': match.fact.place,
            }
        )
    return res


if __name__ == '__main__':
    txt = 'хочу найти боевик с майлом дугласом'
    names = yargy_get_genre(txt)
    print(names)
