from django.shortcuts import render, redirect,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UserForm, EditProfileForm
from django.forms.models import inlineformset_factory
from django.contrib import messages
from .forms import StatusForm
from .models import Status, SiteUser
from django.views.decorators.http import require_http_methods
from django.http import Http404,JsonResponse,HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.core.exceptions import PermissionDenied

import json

#User related views
class UserFormView(View):
    form_class = UserForm
    template_name ='registration/registration_form.html'

    #Registration display form
    def get(self,request):
        form= self.form_class(None)
        return render(request,self.template_name,{'form': form})

    #On registration form submit, add users to database
    def post(self,request):

        form = self.form_class(data=request.POST)
        
        if form.is_valid():
            user=form.save()
            user.refresh_from_db()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.siteuser.telephone = form.cleaned_data.get('telephone')
            user.siteuser.gender = form.cleaned_data.get('gender')
            user.siteuser.birthdate = form.cleaned_data.get('birthdate')
            user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request,user)
                return redirect('profile')
            else:
                return HttpResponse("<h1>User is not active!</h1>")
        else:
            return HttpResponse("<h1>Not registered!</h1>")

#To Change your profile
@login_required
def edit_profile(request,pk):
    user = User.objects.get(pk=pk)
    user_form = EditProfileForm(instance=user)

    ProfileInlineFormset = inlineformset_factory(User, SiteUser, fields=('gender', 'telephone', 'birthdate'))
    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated and request.user.id == user.id:
        if request.method == "POST":
            user_form = EditProfileForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    messages.success(request, 'Your profile has been updated')
                    # return redirect('../../edit_profile/%d/'%pk)

        return render(request, "profile/edit_profile.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
#------End of user views-------------------


# To post user status
def create_post(request):
    if request.method == 'POST':
        post_text = request.POST.get('the_post')
        response_data = {}

        post = Status.objects.create(text=post_text,user=request.user)
        post.save()
        return redirect('profile')
    
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


#To get user status
def get_status(request):
    if request.method == 'GET':
        statusList = Status.objects.all().filter(user=request.user).values('text', 'timestamp') 
        response_data = {}
        status_list = list(statusList)
        return JsonResponse(status_list, safe=False)

    else:
        return JsonResponse('', safe=False)


# Create your views here.


def profile(request):
    template = "profile.html" 
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