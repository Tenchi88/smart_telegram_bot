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


class AnswerMessageDetailView(DetailView):
    model = models.AnswerMessage


def show_nodes(request, **kwargs):
    return render_to_response(
        "nodes_app/node_list.html",
        {'nodes':models.Node.objects.all()}
    )
