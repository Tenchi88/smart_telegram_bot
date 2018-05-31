# -*- coding: utf-8 -*-

from nodes.classification_node import ClassificationNode


class NodesTree:
    def __init__(self, root_node):
        if type(root_node) is not ClassificationNode:
            raise ValueError('Root node has to be ClassificationNode')
        self.root_node = root_node
        self.current_node = self.root_node

    def go_to(self, message, node_name):
        if node_name is not None:
            print('parse_message Go to [{}]'.format(node_name))
            go_to = NodesTree.search_node(node_name, self.root_node)
            print(go_to)
            self.current_node = go_to
            _, answer = self.current_node.parse_message(message)

            if self.current_node is None:
                self.current_node = self.root_node
            if len(self.current_node.sub_nodes) < 1:
                self.current_node = self.root_node

            return answer

    def parse_message(self, message):
        self.current_node, answer = self.current_node.parse_message(message)

        if self.current_node is None:
            self.current_node = self.root_node
        if len(self.current_node.sub_nodes) < 1:
            self.current_node = self.root_node

        # if self.current_node.name == "Настройки интернет подключения":
        #     # print('DEBUG settings')
        #     if 'роутер' in message:
        #         # print('DEBUG settings router')
        #         self.current_node, answer = self.current_node.parse_message(
        #             'использую роутер')
        # if self.current_node.name == "Подключение через роутер":
        #     routers = ['asus', 'd-link', 'apple', 'zyxel']
        #     for router in routers:
        #         if router in message.lower():
        #             self.current_node, answer = self.current_node.parse_message(
        #                 router)
        print('nodes_tree parse_message', answer)

        # if self.current_node is None:
        #     self.current_node = self.root_node
        # if len(self.current_node.sub_nodes) < 1:
        #     self.current_node = self.root_node
        return answer

    def show_tree(self, full_info=True):
        self.root_node.show_full_tree(full_info=full_info)

    def go_to_root(self, message):
        self.current_node = self.root_node
        return self.current_node.answer_message(message)

    @staticmethod
    def search_node(name, node):
        for sub_node in node.sub_nodes:
            if sub_node.name == name:
                return sub_node
        for sub_node in node.sub_nodes:
            res = NodesTree.search_node(name, sub_node)
            if res is not None:
                return res
        return None

    @staticmethod
    def train_tree(node):
        for sub_node in node.sub_nodes:
            NodesTree.train_tree(sub_node)
        node.train_classifier()

    @property
    def current_node_name(self):
        return self.current_node.name
