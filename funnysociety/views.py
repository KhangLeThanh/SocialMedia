from django.shortcuts import render

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