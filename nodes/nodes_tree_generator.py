# coding: utf-8

import json
import jsonschema
import os
from nodes.classification_node import ClassificationNode
from nodes.nodes_tree import NodesTree
from nodes.answer_message import AnswerMessage

from classifiers.classifier_simple_td_idf import ClassifierSimpleTFIDF
from classifiers.classifier_base import ClassifierBase
from classifiers.classifier_equal import ClassifierEqual


class NodesTreeGenerator(object):
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
        with open(json_config, 'r') as config:
            self.json_data = json.load(config)

    def show_children_tree(self, node=None, prefix=' ▶', first_cycle=True):
        if first_cycle:
            node = self.json_data
            self.validate_tree(node)
            print('\n{} children tree:'.format(node['name']))

        print('{} Node \'{}\' with pattern \'{}\''.format(
            prefix, node['name'], node['data_set'])
        )

        if 'answer' in node.keys() and 'text' in node['answer'].keys():
            print(
                '\t' + prefix.replace('▶', 'Q') + ' ' + node['answer']['text']
            )

        if 'sub_nodes' not in node.keys() or node['sub_nodes'] is None:
            return
        for sub in node['sub_nodes']:
            self.show_children_tree(
                sub, prefix='\t' + prefix, first_cycle=False
            )

        if first_cycle:
            print('')

    @staticmethod
    def _get_data_set(json_node, data_set_type):
        if data_set_type is None:
            return None
        return data_set_type(json_node['data_set'])

    @staticmethod
    def _get_val_if_exists(_dict, key):
        return _dict[key] if key in _dict.keys() else None

    @staticmethod
    def _get_answer(answer):
        return AnswerMessage(
            text=NodesTreeGenerator._get_val_if_exists(
                answer, 'text'),
            file=NodesTreeGenerator._get_val_if_exists(
                answer, 'file'),
            function_=NodesTreeGenerator._get_val_if_exists(
                answer, 'function')
        )

    def gen_full_tree(self, data_set_type=None):
        return NodesTree(self._gen_children_tree(
            json_node=self.json_data,
            data_set_type=data_set_type
        )
        )

    def _gen_children_tree(
            self, json_node, data_set_type=None
    ):
        self.validate_node(json_node)
        new_node = ClassificationNode(
            json_node['name'],
            data_set=self._get_data_set(json_node, data_set_type),
            classifier=eval(json_node['classifier'])(),
            answer=NodesTreeGenerator._get_answer(json_node['answer'])
        )

        if json_node['sub_nodes'] is not None:
            for next_json_node in json_node['sub_nodes']:
                next_node = self._gen_children_tree(
                    next_json_node,
                    data_set_type=new_node.classifier.DataSet
                )
                new_node.add_sub_node(next_node)

        return new_node

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