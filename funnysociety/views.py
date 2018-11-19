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
from .models import Status, SiteUser,Friend
from django.views.decorators.http import require_http_methods
from django.http import Http404,JsonResponse,HttpResponse,HttpResponseRedirect
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Q
import json
from itertools import chain

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
        #response_data = {}

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
        #response_data = {}
        status_list = list(statusList)
        return JsonResponse(status_list, safe=False)

    else:
        return JsonResponse('', safe=False)


#To add friend
def add_friend(request):
    if request.method == 'POST':
        requestUsername = request.POST.get('username')

        try:
            newFriend = User.objects.get(username=requestUsername)
        except User.DoesNotExist:
            newFriend = None

        #Check user availability
        if newFriend is None:
            return HttpResponse(
            json.dumps({"status": "user_not_found"}),
            content_type="application/json"
        )

        #Check user is a friend already
        try:
            oldFriendMain = Friend.objects.get(party1=newFriend,party2=request.user.id)
        except Friend.DoesNotExist:
            oldFriendMain = None

        try:
            oldFriendSecond = Friend.objects.get(party2=newFriend,party1=request.user.id)
        except Friend.DoesNotExist:
            oldFriendSecond = None


        if oldFriendMain is None and oldFriendSecond is None:
            request = Friend.objects.create(party1=request.user,party2=newFriend,isPendingRequest=True,isReceivedRequest=False)
            return HttpResponse(
                json.dumps({"status": "request_sent"}),
                content_type="application/json"
            )
        return HttpResponse(
            json.dumps({"status": "already_sent"}),
            content_type="application/json"
        )


#To get friends
def get_friends(request):
    if request.method == 'GET':
         
        friend_List = Friend.objects.filter(Q(party1=request.user) | Q(party2=request.user))
        #.values('party1','party2','party1__username', 'party2__username','party1__first_name','party2__first_name','timestamp','isPendingRequest','isReceivedRequest')
        
 
        data = []
        for r in friend_List:

            cur_user = User.objects.get(id=request.user.id) #gets current user's username
            print(cur_user.id)

            responseData = {
                'friend': list(User.objects.filter(id=r.party1.id).values('id','first_name','last_name')) if cur_user.id != r.party1.id else list(User.objects.filter(id=r.party2.id).values('id','first_name','last_name')),
                'timestamp': r.timestamp,
                'isPendingRequest':r.isPendingRequest,
                'isReceivedRequest': r.isReceivedRequest if cur_user.id == r.party1.id else not r.isReceivedRequest
            }

            data.append(responseData)
        return JsonResponse(data,safe=False)





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