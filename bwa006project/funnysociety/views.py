# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, Http404
from django.shortcuts import render,get_object_or_404
# from funnysociety.models import Product

# Create your views here.
def home(request):
    template = "home_page.html"
    context = {}
    return render(request, template, context)

def profile(request):
    template = "profile_page.html"
    context = {}
    return render(request, template, context)

def discussion(request):
    template = "discussion_page.html"
    context = {}
    return render(request, template, context)

def event(request):
    template = "event_page.html"
    context = {}
    return render(request, template, context)