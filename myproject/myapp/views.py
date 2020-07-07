from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.

def mainpage(request):
    return render(request, 'mainpage.html')

def register(request):
    regiform = RegisterForm(request.POST)
    context = {'regiform': regiform,}

    if request.method == 'POST':
        if regiform.is_valid():
            regiform.save()  
            return redirect('mainpage')

    return render(request, 'register.html', context)

def foruser(request):
    return render(request, 'foruser.html')

def forpoli(request):
    return render(request, 'forpoli.html')