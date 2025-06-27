from django.shortcuts import render

def pchange(request):
    return render(request,'mypage/pchange.html')

def profile(request):
    return render(request,'mypage/profile.html')
