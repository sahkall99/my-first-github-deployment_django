from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# Additional imports for handling user login, logout, and login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

# another example of login required function

@login_required     # only logged in users can see this special view
def special(request):
    return HttpResponse("You are logged in. NIce!")

# the logout view

@login_required     # this ensures that login is required for this logout view.
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:  # used for receiving images, and other documents
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})


# the function view for handling user login
def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

# this line handle the user authentication
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)        # user has logged in
                return HttpResponseRedirect(reverse('index'))   # redirects to the index page
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")   # invalid login details
        else:
            print("Someone tried to login and failed!")
            print("Username: {} and password {}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'basic_app/login.html', {})  # returns the login page to the user


