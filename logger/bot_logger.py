# -*- coding: utf-8 -*-

import csv
import os.path
import datetime


class BotLogger:
    def __init__(
            self,
            storage_type='csv',
            logs_on=False,
            db_adapter=None
    ):
        self.logs_on = logs_on

        self.available_storages = ['csv', 'sqlite', 'postgres']
        if storage_type in self.available_storages:
            self.storage_type = storage_type
        else:
            raise ValueError('Wrong storage type: ' + storage_type)

        self.available_entry_types = [
            'user_message',
            'user_voice',
            'bot_answer',
            'classification',
            'answer_options',
            'file',
            'action'
        ]

        self.base_entry = {
            'user_id': None,
            'time': None,
            'type': None,
            'text': None
        }

        self.db_adapter = db_adapter

    def turn_on(self):
        self.logs_on = True

    def turn_off(self):
        self.logs_on = False

    def add_entry(self, entry):
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
            - answer options
        text - Text data(depends on entry type)
        """
        if not self.logs_on:
            return
        if self.storage_type == 'csv':
            # write to csv file
            csv_file_name = str(entry['user_id']) + '.csv'
            write_header = not os.path.exists(csv_file_name)
            with open(csv_file_name, 'a') as csv_file:
                writer = csv.DictWriter(
                    csv_file,
                    delimiter='\t',
                    fieldnames=self.base_entry.keys()
                )
                if write_header:
                    writer.writeheader()
                writer.writerow(entry)
        if self.storage_type == 'sqlite':
            self.db_adapter.add(entry)

    def add_user_message(self, message):
        entry = self.base_entry
        entry['type'] = 'user_message'
        entry['text'] = message.text
        # send time from message
        # entry['time'] = str(message.date)
        # current time
        entry['time'] = str(datetime.datetime.now())
        entry['user_id'] = str(message.from_user.id)

        self.add_entry(entry)

    def add_bot_answer(self, text):
        entry = self.base_entry
        entry['type'] = 'bot_answer'
        entry['text'] = text
        entry['time'] = str(datetime.datetime.now())
        self.add_entry(entry)

    def add_file(self, file):
        entry = self.base_entry
        entry['type'] = 'file'
        entry['text'] = file
        entry['time'] = str(datetime.datetime.now())
        self.add_entry(entry)

    def add_options(self, options):
        entry = self.base_entry
        entry['type'] = 'options'
        entry['text'] = str(options)
        entry['time'] = str(datetime.datetime.now())
        self.add_entry(entry)

    def add_classification(self, classification):
        entry = self.base_entry
        entry['type'] = 'classification'
        entry['text'] = classification
        entry['time'] = str(datetime.datetime.now())
        self.add_entry(entry)
