from django.shortcuts import render

# Create your views here.
def login(request) :
    return render(request,'login.html')

def id(request) :
    return render(request,'login-findID.html')

def pw(request) :
    return render(request,'login-findPW.html')

def chgpw(request) :
    return render(request,'login-changePW.html')
