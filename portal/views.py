from django.shortcuts import render,redirect
def home(request):
    return render(request,'portal/index.html')
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
def signup(request):
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('home')
    else:
        form=UserCreationForm()
    return render(request,'portal/signup.html',{'form': form})
# Create your views here.
