# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB
import stop_words
# from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
import string
import re
from urllib import request

from spacy.lang.ru import Russian

from os.path import isfile
from json import load
from jsonschema import Draft3Validator
from classifiers.classifier_base import ClassifierBase, ClassifierBaseDataSet
from nodes.answer_message import AnswerMessage


class ClassifierSpacy(ClassifierBase):
    def __init__(self):
        self.is_trained = False
        self.data_sets = []
        self.texts = {}
        self.options = {}
        self.threshold = 0.3

        self.russian_stop_words = stop_words.get_stop_words('russian')
        self.parser = Russian()
        self.stop_list = set(stopwords.words('russian') + list(
            self.russian_stop_words))
        # List of symbols we don't care about
        self.escape_symbols = ' '.join(string.punctuation).split(' ') +\
                              ['-----', '---', '...', '“', '”', '\'ve']
        # the vectorizer and classifer to use
        # note that I changed the tokenizer in CountVectorizer
        # to use a custom function using spaCy's tokenizer
        self.vectorizer = CountVectorizer(
            tokenizer=self.tokenizeText,
            ngram_range=(1, 1)
        )
        self.clf = MultinomialNB()
        # self.clf = LinearSVC()
        # self.clf = SVC(probability=True)

        # the pipeline to clean, tokenize, vectorize, and classify
        self.pipe = Pipeline(
            [
                ('cleanText', ClassifierSpacy.CleanTextTransformer()),
                ('vectorizer', self.vectorizer),
                ('clf', self.clf)
            ]
        )

    def __repr__(self):
        return '<{}> Data sets: {}'.format(
            type(self).__name__, self.options)

    def predict(self, message, auto_train=True):
        if auto_train and not self.is_trained:
            self.train()
            # print('support_', self.clf.support_)
            print('coef_', self.clf.coef_)
            # print('dual_coef_', self.clf.dual_coef_)
            print('intercept_', self.clf.intercept_)
        print(message)
        preds = self.pipe.predict([message])
        print(preds)
        print(message)
        probs = self.pipe.predict_proba([message])
        # probs = self.pipe.decision_function([message])
        # probs = self.pipe.score([message], ['Услуги'])
        print('predict_proba', self.pipe.predict_proba([message]))
        # print('decision_function', self.pipe.decision_function([message]))
        # intercept_x_decision = []
        # for i in range(len(probs[0])):
        #     intercept_x_decision.append(self.clf.intercept_[i]*probs[0][i])
        # print('intercept_x_decision', intercept_x_decision)
        # threshold = sorted_proba[1]*(1.0+self.threshold)
        # print('{} thr {}'.format(proba, threshold))
        if min(probs[0]) <= self.threshold:
            return self.options[preds[0]]
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

    def train(self):
        train = []
        labels_train = []
        print('train')
        for data_set in self.data_sets:
            print('data_set', data_set)
            for text in self.texts[data_set]:
                train.append(text)
                labels_train.append(data_set)

        for i in range(len(train)):
            print(train[i], labels_train[i])

        # train
        self.pipe.fit(train, labels_train)

        self.texts = {}
        self.is_trained = True
        self.threshold = 0.9*1.0/len(self.data_sets)

    # A custom function to clean the text before sending it into the vectorizer

    @staticmethod
    def cleanText(text):
        # get rid of newlines
        text = text.strip().replace('\n', ' ').replace('\r', ' ')

        # replace twitter @mentions
        mentionFinder = re.compile(r'@[a-z0-9_]{1,15}', re.IGNORECASE)
        text = mentionFinder.sub('@MENTION', text)

        # replace HTML symbols
        text = text.replace('&amp;', 'and').replace('&gt;', '>').replace(
            '&lt;',
            '<')

        # lowercase
        text = text.lower()

        return text

    # A custom function to tokenize the text using spaCy
    # and convert to lemmas
    def tokenizeText(self, sample):
        # get the tokens using spaCy
        tokens = self.parser(sample)

        # lemmatize
        lemmas = []
        for tok in tokens:
            lemmas.append(
                tok.lemma_.lower().strip() if tok.lemma_ != '-PRON-' else tok.lower_)
        tokens = lemmas

        # stoplist the tokens
        tokens = [tok for tok in tokens if tok not in self.stop_list]

        # stoplist symbols
        tokens = [tok for tok in tokens if tok not in self.escape_symbols]

        # remove large strings of whitespace
        while '' in tokens:
            tokens.remove('')
        while ' ' in tokens:
            tokens.remove(' ')
        while '\n' in tokens:
            tokens.remove('\n')
        while '\n\n' in tokens:
            tokens.remove('\n\n')

        # print('Tokens:', tokens)
        return tokens

    def printNMostInformative(self, vectorizer, clf, N):
        """Prints features with the highest coefficient values, per class"""
        feature_names = vectorizer.get_feature_names()
        coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
        topClass1 = coefs_with_fns[:N]
        topClass2 = coefs_with_fns[:-(N + 1):-1]
        print('Class 1 best: ')
        for feat in topClass1:
            print(feat)
        print('Class 2 best: ')
        for feat in topClass2:
            print(feat)

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

    # Every step in a pipeline needs to be a "transformer".
    # Define a custom transformer to clean text using spaCy
    class CleanTextTransformer(TransformerMixin):
        """
        Convert text to cleaned text
        """

        def transform(self, X, **transform_params):
            return [ClassifierSpacy.cleanText(text) for text in X]

        def fit(self, X, y=None, **fit_params):
            return self

        def get_params(self, deep=True):
            return {}
