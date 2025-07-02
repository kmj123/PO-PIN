from django.shortcuts import render

##### 커뮤니티
# 메인페이지
def main(request):
    return render(request, 'community/main.html')

# 최근게시글
def recent(request):
    return render(request, 'community/community_recent.html')

# 동행모집글 작성
def write_companion(request):
    return render(request, 'community/community_write_companion.html')

# 대리구매글 작성
def write_proxy(request):
    return render(request, 'community/community_write_proxy.html')

# 후기 작성
def write_review(request):
    return render(request, 'community/community_write_review.html')

# 나눔글 작성
def write_sharing(request):
    return render(request, 'community/community_write_sharing.html')

# 현황공유 작성
# def write_status(request):
#     return render(request, 'community/community_write_status.html')

##### 교환/판매후기 게시판
def chgReview(request) :
    return render(request,'chgReview/main.html')

##### 동행 게시판
def companion(request) :
    return render(request,'companion/main.html')

##### 대리구매 게시판
def proxy(request) :
    return render(request,'proxy/main.html')

##### 나눔 게시판
def sharing(request) :
    return render(request,'sharing/main.html')

##### 현황공유 게시판
def status(request) :
    return render(request,'status/main.html')
