# -*- coding: utf-8 -*-

from nodes.classification_node import ClassificationNode
from nodes.nodes_tree import NodesTree
from nodes.answer_message import AnswerMessage

from nodes.tree_generator_base import TreeGeneratorBase

from classifiers import *


class NodesTreeGenerator(TreeGeneratorBase):
    def gen_full_tree(self, data_set_type=None):
        return NodesTree(self._gen_children_tree(
            json_node=self.json_data,
            data_set_type=data_set_type
            )
        )

    @staticmethod
    def _get_data_set(json_node, data_set_type):
        if data_set_type is None:
            return None
        return data_set_type(json_node['data_set'])

    @staticmethod
    def _get_answer(answer):
        return NodesTreeGenerator._get_answer_with_specified_type(
            answer, AnswerMessage
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
