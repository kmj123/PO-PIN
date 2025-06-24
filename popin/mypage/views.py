from django.shortcuts import render

def pchange(request):
    return render(request,'mypage/pchange.html')

def mypage(request):
    return render(request,'mypage/mypage.html')
