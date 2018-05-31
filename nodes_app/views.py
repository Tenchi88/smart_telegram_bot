# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response

# from  django.template import RequestContext

from . import models


class NodeListView(ListView):
    model = models.Node


class NodeDetailView(DetailView):
    model = models.Node


class ClassifierDetailView(DetailView):
    model = models.Classifier


class ClassifierListView(ListView):
    model = models.Classifier


class AnswerMessageDetailView(DetailView):
    model = models.AnswerMessage


class AnswerMessageListView(ListView):
    model = models.AnswerMessage


def show_nodes(request, **kwargs):
    return render_to_response(
        'nodes_app/node_list.html',
        {'nodes': models.Node.objects.all()}
    )


def gen_nodes(request, **kwargs):
    # config = models.ConfigParser(json_config='json_configs/base_test.json')
    config = models.ConfigParser(json_config='json_configs/caller.json')
    config.gen_full_tree()
    return render_to_response(
        'nodes_app/node_list.html',
        {'nodes': models.Node.objects.all()}
    )


def search_nodes(request, **kwargs):
    # config = models.ConfigParser(json_config='json_configs/base_test.json')
    config = models.ConfigParser(json_config='json_configs/caller.json')
    node = config.search('Подключение через роутер')
    # return render_to_response(
    #     'nodes_app/classifier_detail.html',
    #     {'object': node}
    # )
    return render_to_response(
        'nodes_app/node_detail.html',
        {
            'object': node,
            'classifiers': models.Classifier.objects.all(),
            'answer_messages': models.AnswerMessage.objects.all()
        }
    )


