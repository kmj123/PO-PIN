from django.shortcuts import render,redirect

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

def noticeR(request) :
    return render(request,"admin/notice_rewrite.html")

def noticeD(request,pk) :
    ## 모델 추가시 적용 
    # notice = get_object_or_404(Notice, pk=pk) 

    if request.method == 'POST':
        notice.delete()
        return redirect('adpage:notice')  # 목록 페이지로 이동

    return redirect('adpage:noticeV', pk=pk)  # 잘못된 접근일 경우 다시 상세 페이지로

