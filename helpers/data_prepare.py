import json
import io
import re


def prepare(file_name, max_len=None):
    with open(file_name, 'r') as json_file:
        json_data = json.load(json_file)
        print('Общее количество сырых данных:', len(json_data))
        short_len = 15
        print(
            'Отфильтруем слишком короткие сообщения(до {} символов)'.format(
                short_len
            )
        )
        for row in json_data:
            if len(row['Текст сообщения']) < short_len:
                json_data.remove(row)
        print('Число данных после фильтрации:', len(json_data))
        print(json_data[0])
        # преобразование формата
        result_json = {'data': []}
        cur_data = ""
        last_id = 0
        for row in json_data:
            if row['ID пользователя'] != last_id:
                if len(cur_data):
                    result_json['data'].append(cur_data)
                last_id = row['ID пользователя']
                cur_data = ''
            cur_data += re.sub(
                r'([^\s\w]|_)+', '',
                ' ' + row['Текст сообщения'].replace('\r\n', ' ')
            )
            if max_len and len(result_json['data']) > max_len:
                break
        print('Число диалогов:', len(result_json['data']))
        with io.open(
                file_name[:-5] + '_filtered.json', 'w', encoding='utf8'
        ) as res_file:
            json.dump(result_json, res_file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    prepare('../train_sets/payments.json')
    prepare('../train_sets/international_id.json')
    prepare('../train_sets/car_registration.json')
    prepare('../train_sets/driver_licence.json')
    # txt = {'ID обращения': 94617, 'Текст сообщения': 'Andrey:\r\nДоброй ночи!\r\nПроизвел оплату судебной задолженности через госуслуги личный кабинет. Сумма задолженности обозначена 2500 руб.\r\nОплатил полностью. \r\nСудебная задолженность из личного кабинета пропала, но статус в ГИС ГМП : недоплата 2500 руб.\r\nСтоит ли волноваться по поводу статуса? Вопрос погашения задолженности очень срочный.\r\nЗаранее спасибо за ответ!', 'ID пользователя': 62389.0, 'Тематика': 'Платежи (ИПШ)', 'Тема': 'Какие услуги можно оплачивать'}
    # print(txt['Текст сообщения'].replace('\r\n', ' '))
