from django.shortcuts import render
import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer

chatterbot = ChatBot(**settings.CHATTERBOT)
# inser below lines in views.py file under above line.
trainer = ChatterBotCorpusTrainer(chatterbot)
trainer.train('chatterbot.corpus.hindi')

