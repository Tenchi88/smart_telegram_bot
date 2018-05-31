# -*- coding: utf-8 -*-

from classifiers.classifier_base import ClassifierBase, ClassifierBaseDataSet


class ClassifierLinear(ClassifierBase):
    def __init__(self):
        super(ClassifierLinear, self).__init__()
        self.options = {}

    def __repr__(self):
        return '<{}> Options: {}'.format(
            type(self).__name__, self.options)

    def predict(self, message):
        return [x for x in self.options.values()][0]

    def add_option(self, option):
        self.options[option.name] = option

    class DataSet(ClassifierBaseDataSet):
        def __init__(self, text):
            self.text = text
            self.schema = {
                'type': 'string'
            }

        def __repr__(self):
            return self.repr_base() + 'Text: {}'.format(self.text)
