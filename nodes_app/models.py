# -*- coding: utf-8 -*-

from django.db import models


class Node(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=256)
    classifier = models.ForeignKey('Classifier', related_name='nodes')
    data_set = models.CharField(max_length=256, null=True, blank=True)
    answer_message = models.ForeignKey('AnswerMessage', related_name='nodes')
    parent_node = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='sub_nodes',
        related_query_name="sub_node",
    )

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
        return self.text
