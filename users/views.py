from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import login,logout



def register(request):
    if request.method=="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            return redirect('/')
    else:

        form = CustomUserCreationForm()
    context = {'form':form}
    return render(request, 'users/registration.html', context)

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form = AuthenticationForm

def logout_user(request):
   logout(request)
   return redirect("login")