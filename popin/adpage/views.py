from django.shortcuts import render

# Create your views here.
def main(request) :
    return render(request,"admin/main.html")

def user(request) :
    return render(request,"admin/manageUser.html")

def post(request) :
    return render(request,"admin/managePost.html")

def postV(request) :
    return render(request,"admin/managePost_view.html")

def notice(request) :
    return render(request,"admin/notice.html")

def noticeV(request) :
    return render(request,"admin/notice_view.html")

def noticeW(request) :
    return render(request,"admin/notice_write.html")