# -*- coding: utf-8 -*-

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from . import models


class NodeListView(ListView):
    model = models.Node


class NodeDetailView(DetailView):
    model = models.Node
