from django.shortcuts import render,redirect
from django.contrib import auth
from.forms import UserLoginForm
from.forms import UserRegistrationForm
from Usercontacts.models import Contact

# Create your views here.
def get_index(request):
    if request.user.is_authenticated():
        contacts = Contact.objects.filter(owner=request.user)
    else:
        contacts = []
        
    return render(request, "index.html", {'contacts':contacts})
    
def logout(request):
    auth.logout(request)
    return redirect(get_index)
    
def login(request):
    if request.method=="POST":
       form=UserLoginForm(request.POST) 
       if form.is_valid():
          user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])

          if user is not None:
                auth.login(request, user)
          else:
              form.add_error (None, "You username or password was not recognised")
                
          return redirect(get_index)
        
    else:
        form = UserLoginForm()
    
    return render(request, "login.html", {'form': form})
    
def register(request):
    if request.method=="POST":
         form = UserRegistrationForm(request.POST)
         
         if form.is_valid():
             user = form.save()
             user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])
             if user is not None:
                auth.login(request, user)
                return redirect(get_index)
    else:
        form = UserRegistrationForm()
    
    
    return render(request,"register.html", {'form': form})
    