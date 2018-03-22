# -*- coding: utf-8 -*-

from jsonschema import validate


class ClassifierBaseDataSet(object):
    def repr_base(self):
        return '<{}.{}>'.format(
            self.__module__, type(self).__name__, type(self).__name__)


class ClassifierBase(object):
    def __init__(self):
        self.is_trained = False

    def predict(self, message):
        pass

    def add_option(self, option):
        pass

    def train(self):
        self.is_trained = True

    def json_data_set_validate(self, json_data_set):
        validate(json_data_set, self.DataSet.schema)

    def check_data_set_type(self, data_set):
        if type(data_set) is not self.DataSet:
            raise TypeError(
                'Wrong data set type. It must be {}, not {}'.format(
                    self.DataSet, type(data_set)
                )
            )

    def get_answers(self):
        return None

    class DataSet(ClassifierBaseDataSet):
        def __init__(self):
            pass
