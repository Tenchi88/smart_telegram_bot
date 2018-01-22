# -*- coding: utf-8 -*-

from nodes.tree_generator_base import TreeGeneratorBase
from nodes_app.models import *


class ModelNodesTreeGenerator(TreeGeneratorBase):
    def __init__(self, json_config):
        super(ModelNodesTreeGenerator, self).__init__(json_config)

    def generate(self, delete_all_nodes=False, delete_all_messages=False):
        if delete_all_nodes:
            Node.objects.all().delete()
        if delete_all_messages:
            AnswerMessage.objects.all().delete()
        self._gen_children_tree(
            json_node=self.json_data,
            data_set_type=None
        )

    @staticmethod
    def _get_answer(answer):
        return ModelNodesTreeGenerator._get_answer_with_specified_type(
            answer,
            AnswerMessage
        )

    def _gen_children_tree(
            self, json_node, data_set_type=None,
            parent_node=None
    ):
        self.validate_node(json_node)
        new_node = Node(
            name=json_node['name'],
            classifier=self.get_classifier(json_node['classifier']),
            answer_message=self.get_answer_message(json_node['answer']),
            data_set=json_node['data_set'],
            parent=parent_node
        )
        new_node.save()

        if json_node['sub_nodes'] is not None:
            for next_json_node in json_node['sub_nodes']:
                next_node = self._gen_children_tree(
                    next_json_node,
                    parent_node=new_node
                )

        return new_node

    def get_model_object(self, model_name, params_dict):
        query = 'model_name.objects.filter('
        for key, value in params_dict.items():
            query += '{}=\'{}\','.format(key, value)
        query = query[:-1] + ').first()'
        return eval(query)

    def search_classifier(self, name):
        classifier = self.get_model_object(
            Classifier, {'name': name}
        )
        return classifier

    def get_classifier(self, name, create_if_doesnt_exist=True):
        classifier = self.search_classifier(name)
        if classifier is None and create_if_doesnt_exist:
            classifier = Classifier(name=name)
            classifier.save()
        return classifier

    def get_answer_message(self, message_in_json):
        message = self._get_answer(message_in_json)
        search_dict = {}
        if message.text is not None:
            search_dict['text'] = message.text
        if message.file is not None:
            search_dict['file'] = message.file
        if message.function_name is not None:
            search_dict['function_name'] = message.function_name
        answer_message = self.get_model_object(
            AnswerMessage,
            search_dict
        )
        if answer_message is not None:
            return answer_message
        message.save()
        return message

    @staticmethod
    def _get_answer(answer):
        return ModelNodesTreeGenerator._get_answer_with_specified_type(
            answer, AnswerMessage
        )
