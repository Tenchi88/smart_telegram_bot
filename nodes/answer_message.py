# -*- coding: utf-8 -*-

class AnswerMessage(object):
    def __init__(
            self,
            text=None,
            file=None,
            options=None,
            function_name=None
    ):
        AnswerMessage._param_type_check('Text', text, str)
        AnswerMessage._param_type_check('File', file, str)
        AnswerMessage._param_type_check('Options', options, list)
        AnswerMessage._param_type_check('Function', function_name, str)
        self.text = text
        self.file = file
        self.options = options
        self.function = function_name

    @staticmethod
    def _param_type_check(param_name, val, _type):
        if val is not None and type(val) is not _type:
            raise ValueError(
                '{} has to be {}, not {}'.format(param_name, _type, type(val))
            )

    def __repr__(self):
        res = '<{}>'.format(type(self).__name__)
        if self.text is not None:
            res += ' Text: \'{}\''.format(self.text)
        if self.file is not None:
            res += ' File: \'{}\''.format(self.file)
        if self.options is not None:
            res += ' Options: \'{}\''.format(self.options)
        if self.function is not None:
            res += ' Function: \'{}\''.format(self.function)
        return res

