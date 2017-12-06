# -*- coding: utf-8 -*-

from django.contrib import admin

from . import models


admin.site.register(models.Node)
admin.site.register(models.Classifier)
admin.site.register(models.AnswerMessage)
