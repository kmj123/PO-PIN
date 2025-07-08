from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import SharingPost, SharingTag, SharingImage
from django.core.paginator import Paginator
from django.db.models import Avg
from datetime import datetime, timedelta
from django.core.files.storage import default_storage
from django.db import transaction
from django.http import HttpResponse
from community.models import ExchangeReview, ReviewImage, ReviewTag
from signupFT.models import User  # 너의 커스텀 유저 모델 import
from django.contrib import messages


User = get_user_model()
#########  urls.py 순서대로 정리함 

 ##교환/판매후기 메인
def chgReviewmain(request):
    #이번 주 시작일 기준잡기  
    today= datetime.today()
    start_of_week = today - timedelta(days=today.weekday())# 월요일기준 
    #이번 주 거래량 (후기수)
    weekly_reviews = ExchangeReview.objects.filter(created_at__gte=start_of_week)
    weekly_count = weekly_reviews.count() 
    # 평균 평점
    average_score = ExchangeReview.objects.aggregate(avg_score=Avg("overall_score"))["avg_score"]
    average_score = round(average_score or 0, 1)  # None 대비 처리
    
    all_reviews = ExchangeReview.objects.all().order_by('-created_at')  # 최신순
    
    # 페이지네이터
    paginator = Paginator(all_reviews, 7)  # 한 페이지당 7개
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"weekly_count": weekly_count, "average_score": average_score,"page_obj": page_obj}
    return render(request, "chgReview/main.html", context)




##교환/판매 상세보기 
def chgReviewview(request) :
    return render(request,"chgReview/chgR_view.html")

## 최근게시글
def recent(request):
    return render(request, 'community/community_recent.html')

#############################################################################
# 동행모집글 작성
def write_companion(request):
    
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', '').strip()
        category =request.POST.get('category', '').strip()
        location= request.POST.get('location','').strip()
        share_date=request.POST.get('share_date','').strip()
        requirement=request.POST.get('requirement','').strip()
        content = request.POST.get('content', '').strip()
        tag_string = request.POST.get('tags', '').strip()
        images = request.FILES.getlist('images')
        # 2. 필수값 체크
        required_fields = {
            "제목": title,
            "내용": content,
            "장소": location,
            "필수사항": requirement,
        }
        for label, value in required_fields.items():
            if not value:
                return render(request, 'community_write_sharing.html', {
                    "error": f"{label}은(는) 필수 항목입니다.",
                    "form_data": request.POST
                })


        # 3. 나눔글 저장
        try:
            post = SharingPost.objects.create(
                title=title,
                artist=artist,
                category =category,
                location=location,
                share_date =share_date ,
                content=content,
                author=user,
               
            )
            print(" 리뷰 생성 완료:", post.id)
        except Exception as e:
            print(" 리뷰 저장 실패:", e)
            return render(request, 'community_write_sharing.html', {
                "error": f"리뷰 저장 중 오류 발생: {str(e)}",
                "form_data": request.POST
            })

        # 4. 태그 저장
        if tag_string:
            tag_names = tag_string.replace(",", " ").split()
            for tag_name in tag_names:
                tag_obj, _ = SharingTag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)
            print(" 태그 추가:", tag_names)

        # 5. 이미지 수 제한 확인
        if len(images) > 5:
            return render(request, 'community_write_sharing.html', {
                "error": "이미지는 최대 5개까지만 업로드할 수 있습니다.",
                "form_data": request.POST
            })

        # 6. 이미지 저장
        for img in images: 
            try:
                 SharingImage.objects.create(post=post, image=img)
                 print(" 이미지 저장됨:", img.name)
            except Exception as e: 
                print(" 이미지 저장 실패 :" ,  e)

        return redirect('sharing:main')  # 또는 너의 리뷰 리스트 페이지

    return render(request, 'community/community_write_companion.html')

## 대리구매글 작성

def write_proxy(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title', '').strip()
        artist = request.POST.get('artist', '').strip()
        #대리구매 날짜 =
        location= request.POST.get('location','').strip()
        #최대모집인원 = 
        #수고비 = 
        content = request.POST.get('content', '').strip()
        tag_string = request.POST.get('tags', '').strip()
        images = request.FILES.getlist('images')
        
        # 2. 필수값 체크
        required_fields = {
            "제목": title,
            "내용": content,
            "장소": location,
           
        }
        for label, value in required_fields.items():
            if not value:
                return render(request, 'community_write_sharing.html', {
                    "error": f"{label}은(는) 필수 항목입니다.",
                    "form_data": request.POST
                })


        # 3. 나눔글 저장
        try:
            post = SharingPost.objects.create(
                title=title,
                artist=artist,
                #날짜 
                location=location,
                # 최대모집인원 
                #수고비 
                content=content,
                author=user,
               
            )
            print(" 리뷰 생성 완료:", post.id)
        except Exception as e:
            print(" 리뷰 저장 실패:", e)
            return render(request, 'community_write_sharing.html', {
                "error": f"리뷰 저장 중 오류 발생: {str(e)}",
                "form_data": request.POST
            })

        # 4. 태그 저장
        if tag_string:
            tag_names = tag_string.replace(",", " ").split()
            for tag_name in tag_names:
                tag_obj, _ = SharingTag.objects.get_or_create(name=tag_name)
                post.tags.add(tag_obj)
            print(" 태그 추가:", tag_names)

        # 5. 이미지 수 제한 확인
        if len(images) > 5:
            return render(request, 'community_write_sharing.html', {
                "error": "이미지는 최대 5개까지만 업로드할 수 있습니다.",
                "form_data": request.POST
            })

        # 6. 이미지 저장
        for img in images: 
            try:
                 SharingImage.objects.create(post=post, image=img)
                 print(" 이미지 저장됨:", img.name)
            except Exception as e: 
                print(" 이미지 저장 실패 :" ,  e)

        return redirect('sharing:main')  # 또는 너의 리뷰 리스트 페이지

    return render(request, 'community/community_write_companion.html')
    
    
    return render(request, 'community/community_write_proxy.html')


## 교환후기 글작성 
def write_review(request):
    if request.method == 'POST':
        try:
            # 세션에서 user_id 가져오기
            user_id = request.session.get('user_id')
            if not user_id:
                messages.error(request, "[오류] 로그인 정보가 없습니다.")
                return redirect('community:write_review')

            try:
                writer = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                messages.error(request, "[오류] 유저 정보를 찾을 수 없습니다.")
                return redirect('community:write_review')

            title = request.POST.get('title')
            content = request.POST.get('content')
            artist = request.POST.get('artist', '기타')
            method = request.POST.get('method')
            transaction_type = request.POST.get('transaction_type', '교환')
            score = int(request.POST.get('overall_score', 3))
            tag_str = request.POST.get('tags', '')
            partner_id = request.POST.get('partner')

            try:
                partner = User.objects.get(user_id=partner_id)
            except User.DoesNotExist:
                partner = writer  # fallback

            with transaction.atomic():
                review = ExchangeReview.objects.create(
                    writer=writer,
                    partner=partner,
                    title=title,
                    content=content,
                    artist=artist,
                    method=method,
                    transaction_type=transaction_type,
                    overall_score=score
                )

                if tag_str:
                    tag_list = [tag.lstrip('#') for tag in tag_str.strip().split()]
                    for tag in tag_list:
                        tag_obj, _ = ReviewTag.objects.get_or_create(name=tag)
                        review.tags.add(tag_obj)

                for img in request.FILES.getlist('images'):
                    ReviewImage.objects.create(review=review, image=img)

            messages.success(request, "리뷰가 저장되었습니다.")
            return redirect('community:main')

        except Exception as e:
            print("[리뷰 저장 실패]", e)
            messages.error(request, f"[오류] {str(e)}")
            return redirect('community:write_review')

    return render(request, 'community/community_write_review.html')
#########################################

#나눔 

from signupFT.models import User  # 정확한 사용자 모델 import

def write_sharing(request):
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')  # 문자열 'aaa' 같은 값
            if not user_id:
                messages.error(request, "[오류] 로그인 정보가 없습니다.")
                return redirect('community:write_sharing')

            # 💥 핵심 수정: get(pk=...) 사용하고, 모델의 PK는 'user_id'이므로 문제 없음
            try:
                author = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                messages.error(request, "[오류] 작성자 정보를 찾을 수 없습니다.")
                return redirect('community:write_sharing')

            # 폼 데이터 수집
            title = request.POST.get('title')
            content = request.POST.get('content')
            artist = request.POST.get('artist', '기타')
            category = request.POST.get('category')
            type = request.POST.get('type')
            share_date = request.POST.get('share_date')
            location = request.POST.get('location')
            requirement = request.POST.get('requirement')
            tag_str = request.POST.get('tags', '')

            with transaction.atomic():
                post = SharingPost.objects.create(
                    author=author,
                    title=title,
                    content=content,
                    artist=artist,
                    category=category,
                    type=type,
                    share_date=share_date,
                    location=location,
                    requirement=requirement
                )

                # 태그 저장
                if tag_str:
                    tag_list = [tag.strip().lstrip('#') for tag in tag_str.split()]
                    for tag in tag_list:
                        tag_obj, _ = SharingTag.objects.get_or_create(name=tag)
                        post.tags.add(tag_obj)

                # 이미지 저장
                for img in request.FILES.getlist('images'):
                    SharingImage.objects.create(post=post, image=img)

            messages.success(request, "나눔 글이 저장되었습니다.")
            return redirect('community:main')

        except Exception as e:
            print("[나눔 저장 실패]", e)
            messages.error(request, f"[오류] {str(e)}")
            return redirect('community:write_sharing')

    return render(request, 'community/community_write_sharing.html')
#################################################################
 #현황공유 작성
def write_status(request):
     return render(request, 'community/community_write_status.html')


# 메인페이지
def main(request):
    return render(request, 'community/main.html')



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

