from django.shortcuts import render

def write_review(request):
    return render(request, 'community_write_review.html')

def write_sharing(request):
    return render(request, 'community_write_sharing.html')