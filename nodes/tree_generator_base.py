# -*- coding: utf-8 -*-

import json
import jsonschema
import os


class TreeGeneratorBase:
    schema = {
        'type': 'object',
        'required': ['name', 'classifier', 'answer'],
        'properties': {
            'name': {'type': 'string'},
            'classifier': {'type': 'string'},
            'data_set': {'types': ('string', 'none')},
            'answer': {
                'type': 'object',
                'required': ['text'],
                'properties': {
                    'text': {'type': 'string'},
                    'file': {'type': 'string'},
                    'function': {'type': 'string'}
                }
            },
            'sub_nodes': {'types': ('array', 'none')}
        }
    }

    def __init__(self, json_config):
        self.json_data = None
        self.set_config(json_config)

    def __repr__(self):
        return '<{}>'.format(
            type(self).__name__)

    def set_config(self, json_config):
        if json_config is None or not os.path.isfile(json_config):
            raise ValueError('Path to .json config file has to be specified.'
                             'Wrong path: {}'.format(json_config))
        with open(json_config, 'r', encoding='utf-8') as config:
            self.json_data = json.load(config)

    def validate_node(self, json_node):
        if not jsonschema.Draft3Validator(self.schema).is_valid(json_node):
            exception_data = ['Validation error in: {}'.format(json_node)]
            for error in sorted(
                    jsonschema.Draft3Validator(self.schema).iter_errors(
                        json_node
                    ),
                    key=str
            ):
                exception_data.append(error.message)
            raise ValueError(exception_data)

    def validate_tree(self, json_node):
        self.validate_node(json_node)
        if json_node['sub_nodes'] is not None:
            for next_json_node in json_node['sub_nodes']:
                self.validate_tree(next_json_node)

    @staticmethod
    def _get_val_if_exists(_dict, key):
        return _dict[key] if key in _dict.keys() else None

    @staticmethod
    def _get_answer_with_specified_type(answer, return_type):
        return return_type(
            text=TreeGeneratorBase._get_val_if_exists(
                answer, 'text'),
            file=TreeGeneratorBase._get_val_if_exists(
                answer, 'file'),
            function_name=TreeGeneratorBase._get_val_if_exists(
                answer, 'function')
        )
