# -*- coding: utf-8 -*-

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Node(MPTTModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=256)
    classifier = models.ForeignKey('Classifier', related_name='nodes')
    data_set = models.CharField(max_length=256, null=True, blank=True)
    answer_message = models.ForeignKey('AnswerMessage', related_name='nodes')

    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Classifier(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class AnswerMessage(models.Model):
    text = models.CharField(max_length=256, null=True, blank=True)
    file = models.CharField(max_length=256, null=True, blank=True)
    options = models.CharField(max_length=256, null=True, blank=True)
    function = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        if self.text is not None:
            return ' \'{}\''.format(self.text)
        if self.function is not None:
            return ' Function: \'{}\''.format(self.function)
        if self.file is not None:
            return ' File: \'{}\''.format(self.file)
        if self.options is not None:
            return ' Options: \'{}\''.format(self.options)
        return ''
