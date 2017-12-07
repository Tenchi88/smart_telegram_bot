# coding: utf-8

import datetime
import logging
import os.path
import time
import json

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater

from logger.bot_logger import BotLogger
import logger.log_db_adapter
from nodes.nodes_tree_generator import NodesTreeGenerator


class SmartBot:
    def __init__(
        self,
        logic_config='json_configs/simple_example.json',
        telegram_cfg_path='json_configs/telegram.json',
        db_path='db/aiml.db',
        sql_debug=False,
        logging_lvl=logging.WARNING,
    ):
        # Read telegram token
        if os.path.exists(telegram_cfg_path):
            with open(telegram_cfg_path, 'r') as config:
                self.tg_token = json.load(config)['token']
        else:
            raise ValueError(
                'Telegram config file doesn\'t exist :{}'.format(
                    telegram_cfg_path
                )
            )

        self.db_adapter = logger.log_db_adapter.LogDBAdapter(
            db_path=db_path,
            create_tables=True,
            sql_debug=sql_debug
        )
        self.logger = BotLogger(
            db_adapter=self.db_adapter,
            storage_type='sqlite',
            logs_on=True
        )

        # инициализация telegram
        self.updater = Updater(token=self.tg_token)
        self.dispatcher = self.updater.dispatcher

        self.current_class = None

        self.custom_keyboard = None

        tree_generator = NodesTreeGenerator(
            logic_config)
        self.nodes_tree = tree_generator.gen_full_tree()

        # logs on
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging_lvl
        )

        # user message handlers
        self.start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(self.start_handler)

        self.uptime_handler = CommandHandler('uptime', self.uptime)
        self.dispatcher.add_handler(self.uptime_handler)

        self.build_time_handler = CommandHandler('buildtime', self.buildtime)
        self.dispatcher.add_handler(self.build_time_handler)

        self.echo_handler = MessageHandler(Filters.text, self.echo)
        self.dispatcher.add_handler(self.echo_handler)

        self.voice_handler = MessageHandler(Filters.voice, self.voice)
        self.dispatcher.add_handler(self.voice_handler)

        # initial data
        self.run_time = datetime.datetime.now()

        self.source_file = __file__
        self.build_time = os.path.getmtime(self.source_file)

    # command /start
    def start(self, bot, update):
        self.send_message(
            bot,
            update.message.chat_id,
            text=self.nodes_tree.root_node.answer.text
        )

    # command /uptime
    def uptime(self, bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text=u'Время работы: ' + str(
                datetime.datetime.now() - self.run_time)
        )

    # command /buildtime
    def buildtime(self, bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Время последней модификации скрипта[\'{}\']: {}'.format(
                self.source_file,
                str(time.ctime(self.build_time))
            )
        )

    # voice message parser
    @staticmethod
    def voice(bot, update):
        bot.send_message(
            chat_id=update.message.chat_id,
            text=u'Получено аудио от ' + str(update.message.from_user)
        )
        bot.send_message(
            chat_id=update.message.chat_id,
            text=u'длительностью ' + str(update.message.voice.duration)
        )
        bot.send_message(
            chat_id=update.message.chat_id,
            text=u'ID файла: ' + update.message.voice.file_id)
        voice_file = bot.get_file(update.message.voice.file_id)
        voice_file.download(custom_path='voice_tmp.oga')

    def send_message(self, bot, chat_id, text=None, file=None, options=None):
        if options:
            self.custom_keyboard = [val for val in options]
            self.custom_keyboard.append([u'отмена'])
            reply_markup = ReplyKeyboardMarkup(self.custom_keyboard)
        else:
            reply_markup = ReplyKeyboardRemove(remove_keyboard=True)
            self.custom_keyboard = None

        if text:
            self.logger.add_bot_answer(text)
            if options:
                self.logger.add_options(options)
            bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                resize_keyboard=True
            )

        if file is not None:
            if file != '':
                self.logger.add_file(file)
                bot.send_document(
                    chat_id=chat_id,
                    document=file,
                    reply_markup=reply_markup
                )

    # non-command text
    def echo(self, bot, update):
        msg = update.message.text
        self.logger.add_user_message(update.message)
        if msg == 'отмена':
            answer = self.nodes_tree.go_to_root(msg)
        else:
            answer = self.nodes_tree.parse_message(msg)
        self.logger.add_classification(self.nodes_tree.current_node_name)
        self.send_message(
            bot,
            update.message.chat_id,
            text=answer.text,
            file=answer.file,
            options=answer.options
        )

    def run(self):
        try:
            self.updater.start_polling()
        except (KeyboardInterrupt, EOFError, SystemExit):
            print('Stop polling')
            self.updater.idle()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    your_json_config = 'json_configs/base_test.json'
    if os.path.exists(your_json_config):
        chat_bot = SmartBot(logic_config=your_json_config)
    else:
        chat_bot = SmartBot()
    chat_bot.run()
