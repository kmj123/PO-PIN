from django.shortcuts import render
from .models import ExchangeReview

def main(request):
    reviews = ExchangeReview.objects.all().order_by('-created_at')  # 최신순
    return render(request, 'chgReview/main.html', {'reviews': reviews})

def view(request) :
    return render(request,"chgReview/chgR_view.html")