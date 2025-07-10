from django.shortcuts import render

# Create your views here.

def information(request):
    return render(request, 'information.html')

def notice(request):
    return render(request, 'notice.html')

def notice_view(request):
    return render(request, 'notice_view.html')

def QnA(request):
    return render(request, 'Q&A.html')