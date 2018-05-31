from user_manager.yargy_ner import yargy_get_channel, yargy_smart_home

text = '''
Включи первый канал или НТВ
Включи программу россия
Включи культуру
Что показывают по дождю'''
# print(yargy_get_channel(text))


text = '''
Включи лампочку в ванной
включи розетку в гостевой комнате
на кухне включи свет'''
for val in yargy_smart_home(text):
    print(val)
