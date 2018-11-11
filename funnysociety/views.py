from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from django.http import HttpResponse
from .forms import UserForm
from .forms import StatusForm
from .models import Status
from django.views.decorators.http import require_http_methods
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