# coding: utf-8

from classifiers.classifier_base import ClassifierBase, ClassifierBaseDataSet


class ClassifierEqual(ClassifierBase):
    def __init__(self):
        self.options = {}
        self.answers = None
        self.answers_actual = False

    def predict(self, message):
        for option in self.options.values():
            if message == option.data_set.text:
                return option
        return None

    def add_option(self, option):
        self.check_data_set_type(option.data_set)
        self.options[option.name] = option
        self.answers_actual = False

    def get_answers(self):
        if not self.answers_actual:
            self.answers = [[a.data_set.text] for a in self.options.values()]
            self.answers_actual = True
        return self.answers

    def __repr__(self):
        return '<{}> Options: {}'.format(
            type(self).__name__, self.get_answers())

    class DataSet(ClassifierBaseDataSet):
        def __init__(self, text):
            self.text = text
            self.schema = {
                'type': 'string'
            }

        def __repr__(self):
            return self.repr_base() + 'Text: {}'.format(self.text)

