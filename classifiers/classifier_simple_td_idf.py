# -*- coding: utf-8 -*-

from os.path import isfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from jsonschema import Draft3Validator
from json import load
from classifiers.classifier_base import ClassifierBase, ClassifierBaseDataSet
from nodes.answer_message import AnswerMessage
from urllib import request


class ClassifierSimpleTFIDF(ClassifierBase):
    def __init__(self):
        self.is_trained = False
        self.data_sets = []
        self.texts = {}
        self.count_vect = None
        self.clf = None
        self.tfidf_transformer = None
        self.options = {}
        self.threshold = 0.3

    def __repr__(self):
        return '<{}> Is trained: {} Data sets: {}'.format(
            type(self).__name__, self.is_trained, self.options)

    def predict(self, message, auto_train=True):
        if auto_train and not self.is_trained:
            self.train()
        x_train_counts_tst = self.count_vect.transform([message])
        x_train_tfidf_tst = self.tfidf_transformer.transform(x_train_counts_tst)
        set_number = self.clf.predict(x_train_tfidf_tst)
        proba = self.clf.predict_proba(x_train_tfidf_tst)[0]
        sorted_proba = proba.copy()
        sorted_proba.sort()
        threshold = sorted_proba[1]*(1.0+self.threshold)
        print('{} thr {}'.format(proba, threshold))
        if proba[set_number[0]] >= threshold:
            return self.options[self.data_sets[set_number[0]]]
        answer = AnswerMessage(
            text='Ищу в Google https://google.ru/search?q={}'.format(
                request.quote(message.encode('cp1251'))
            )
        )
        return answer

    def add_option(self, option):
        self.check_data_set_type(option.data_set)
        if self.is_trained:
            raise PermissionError(
                'You can not add options to already trained model. Use clear_'
                'options() before it'
            )
        set_name = option.name
        self.options[option.name] = option
        self.data_sets.append(set_name)
        with open(option.data_set.train_set, 'r', encoding='utf-8') as train_file:
            self.texts[set_name] = load(train_file)['data']
        self.is_trained = False

    def clear_options(self):
        self.is_trained = False
        self.texts = {}
        self.count_vect = None
        self.clf = None
        self.tfidf_transformer = None

    def train(self):
        data_text = []
        target_text = []

        for ind, t in enumerate(self.data_sets):
            for sent in self.texts[t]:
                data_text.append(sent)
                target_text.append(ind)

        self.count_vect = CountVectorizer()
        x_train_counts = self.count_vect.fit_transform(data_text)

        self.tfidf_transformer = TfidfTransformer()
        x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_counts)

        self.clf = MultinomialNB().fit(x_train_tfidf, target_text)

        self.texts = {}
        self.is_trained = True

    class DataSet(ClassifierBaseDataSet):
        def __init__(self, train_set):
            if type(train_set) is not str:
                raise TypeError(
                    'Train set has to be path to .json file, '
                    'not {}'.format(train_set)
                )
            if not train_set.endswith('.json') or not isfile(train_set):
                raise ValueError(
                    'Train set has to be path to .json file, '
                    'not {}'.format(train_set)
                )
            self.schema = {
                'type': 'array',
                'items': {
                    'type': 'string'
                }
            }
            schema = {
                'type': 'object',
                'required': ['data'],
                'properties': {
                    'data': {'type': 'array'}
                }
            }
            with open(train_set, 'r', encoding='utf-8') as train_file:
                train_data = load(train_file)
            if not Draft3Validator(schema).is_valid(train_data):
                exception_data = ['Validation error in: {}'.format(train_data)]
                for error in sorted(
                        Draft3Validator(self.schema).iter_errors(train_data),
                        key=str):
                    exception_data.append(error.message)
                raise ValueError(exception_data)
            self.train_set = train_set

        def __repr__(self):
            return self.repr_base() + \
                   'Train set len: {} First 5 values: {}'.format(
                       len(self.train_set),
                       self.train_set[:min(5, len(self.train_set))]
                   )
