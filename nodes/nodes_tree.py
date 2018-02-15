# -*- coding: utf-8 -*-

from nodes.classification_node import ClassificationNode


class NodesTree:
    def __init__(self, root_node):
        if type(root_node) is not ClassificationNode:
            raise ValueError('Root node has to be ClassificationNode')
        self.root_node = root_node
        self.current_node = self.root_node

    def parse_message(self, message):
        self.current_node, answer = self.current_node.parse_message(message)
        if self.current_node is None:
            self.current_node = self.root_node
        if len(self.current_node.sub_nodes) < 1:
            self.current_node = self.root_node
        return answer

    def show_tree(self, full_info=True):
        self.root_node.show_full_tree(full_info=full_info)

    def go_to_root(self, message):
        self.current_node = self.root_node
        return self.current_node.answer_message(message)

    @staticmethod
    def train_tree(node):
        for sub_node in node.sub_nodes:
            NodesTree.train_tree(sub_node)
        node.train_classifier()

    @property
    def current_node_name(self):
        return self.current_node.name
