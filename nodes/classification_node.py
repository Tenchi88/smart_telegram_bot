# coding: utf-8

from classifiers.classifier_base import ClassifierBase
from classifiers.classifier_equal import ClassifierEqual
from classifiers.classifier_simple_td_idf import ClassifierSimpleTFIDF
from nodes.answer_message import AnswerMessage
import nodes.external_node_functions


class ClassificationNode(object):
    def __init__(
            self, name, data_set=None, answer=None, classifier=None
    ):
        if type(name) is not str:
            raise TypeError('ClassificationNode name has to be str', name)
        self.name = name
        self.sub_nodes = []
        self.classifier = ClassifierBase()
        self.parent_node = None
        self.data_set = data_set
        if answer is not None and type(answer) is not AnswerMessage:
            raise ValueError('Answer has to be AnswerMessage or '
                             'None: [{}] {}'.format(answer, type(answer)))
        self.answer = answer
        if classifier is not None:
            self.set_classifier(classifier)

    def __repr__(self):
        res = '<{}> Name: \'{}\' Classifier: \'{}\' Answer: \'{}\''.format(
            type(self).__name__, self.name, type(self.classifier).__name__,
            self.answer
        )
        # answers = self.classifier.get_answers()
        # if answers is not None:
        #     res += ' Options: \'{}\''.format(answers)
        return res

    def set_classifier(self, classifier):
        if ClassifierBase not in type(classifier).__bases__ and \
                        type(classifier) is not ClassifierBase:
            raise TypeError(
                'Classifier has to be based on ClassifierBase', classifier
            )
        self.classifier = classifier

    def answer_message(self, message):
        if self.answer is None:
            raise ValueError('Answer has to be not None in {}'.format(self))
        self.answer.options = self.classifier.get_answers()
        if self.answer.function is not None:
            answer = eval(
                'external_node_functions.' + self.answer.function
            )(message=message, answer_params=self.answer)
            if type(answer) is AnswerMessage:
                return answer
            return AnswerMessage(text=answer)
        else:
            return self.answer

    def parse_message(self, message):
        if self.classifier is None:
            raise AttributeError(
                'Error: classifier is not set.\n{}'.format(self)
            )
        node = self.classifier.predict(message=message)
        return node, node.answer_message(message)

    def add_sub_node(self, sub_node):
        if type(sub_node) is not ClassificationNode:
            raise TypeError('Sub node must be ClassificationNode')
        if self.classifier is None:
            raise ValueError('Classifier is None')
        self.sub_nodes.append(sub_node)
        self.classifier.add_option(sub_node)
        sub_node.parent_node = self

    def show_children_tree(
            self, prefix=' ▶', first_cycle=True, full_info=False
    ):
        if first_cycle:
            print('\n{} children tree:'.format(self.name))
        if full_info:
            print(prefix, self)
        else:
            print(prefix, self.name)
        for sub in self.sub_nodes:
            ClassificationNode.show_children_tree(
                sub, prefix='\t' + prefix,
                full_info=full_info, first_cycle=False)
        if first_cycle:
            print('')

    def show_parents_tree(self, full_info=False):
        print('\n{} parents tree:'.format(self.name))
        if full_info:
            sup_tree = [self.__repr__()]
        else:
            sup_tree = [self.name]
        node = self
        while node.parent_node is not None:
            node = node.parent_node
            if full_info:
                sup_tree.append(node.__repr__())
            else:
                sup_tree.append(node.name)
        prefix = ' ▶ '
        for i in range(len(sup_tree)).__reversed__():
            print(prefix + sup_tree[i])
            prefix = '\t' + prefix
        print('')

    def show_full_tree(self, full_info=False):
        node = self
        while node.parent_node is not None:
            node = node.parent_node
        node.show_children_tree(full_info=full_info)
