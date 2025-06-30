from django.shortcuts import render

# Create your views here.
def main(request) :
    return render(request,'chgReview/main.html')

def view(request) :
    return render(request,"chgReview/chgR_view.html")