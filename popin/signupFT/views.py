from django.shortcuts import render

# Create your views here.

def agree(request):
    return render(request, '1.agree.html')