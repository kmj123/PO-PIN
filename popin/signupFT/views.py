from django.shortcuts import render,redirect
from idols.models import Group, Member  

def agree(request):
    return render(request, '1.agree.html')

def signup(request):
    if request.method == 'POST':
        # ... 회원가입 처리 로직 ...
        return redirect('accounts:login')  
    return render(request, '2.signup.html')

def location_select(request):
    return render(request, '3.location_select.html')

def member_select(request):
    return render(request, '4.member_select.html')

def completed(request):
    return render(request, '5.completed.html')