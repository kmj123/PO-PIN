
from django.shortcuts import render,redirect
from signupFT.models import User
from photocard.models import Photocard
from django.db.models import Count
from django.core.paginator import Paginator


def main(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        user = User.objects.get(user_id=user_id) # 로그인한 사용자
        
        # 전체 게시글
        total_photocard = Photocard.objects.all().count() 
        # 활성 사용자
        total_user = User.objects.all().count() 
        # 교환 완료
        completed_photocard = Photocard.objects.filter(sell_state='후', buy_state='후').count() 
        
        # 최근 인기 포토카드 (거래중인 것)
        photocards = Photocard.objects.filter(sell_state='중', buy_state=None).select_related('member__group').annotate(
        wish_count=Count('wished_by_users')).order_by('-wish_count')[:4]
        
        context = {
            'username': user.name or user.nickname or user.user_id,  # 로그인한 사용자
            'photocards': photocards, # 최근 인기 포토카드
            'total_photocard':total_photocard, # 전체 게시글
            'total_user':total_user,  # 활성 사용자
            'completed_photocard':completed_photocard, #교환 완료
        }
        
        return render(request, 'main.html', context)
    
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비
    
    


# 임시 게시글 데이터 (카테고리별로 구분된 예시)
posts = [
    {'title': 'IVE 원영 포토카드 교환해요!', 'category': '교환', 'writer_id': 'kpop_lover', 'createDate': '5분 전', 'hit': 23},
    {'title': 'IVE 원영 포토카드 판매해요!', 'category': '판매', 'writer_id': 'kpop_lover', 'createDate': '30분 전', 'hit': 38},
    {'title': 'BLACKPINK 리사 포토카드 판매합니다', 'category': '판매', 'writer_id': 'generous_fan', 'createDate': '12분 전', 'hit': 45},
    {'title': 'BTS 정국 포토카드 판매', 'category': '판매', 'writer_id': 'army_collector', 'createDate': '23분 전', 'hit': 67},
    {'title': '교환 구해요', 'category': '교환', 'writer_id': 'happy_trader', 'createDate': '1시간 전', 'hit': 112},
    {'title': 'IVE 안유진 포카 판매', 'category': '판매', 'writer_id': 'creative_diver', 'createDate': '35분 전', 'hit': 89},
    {'title': 'NCT 포토카드 교환해요!', 'category': '교환', 'writer_id': 'kpop_lover', 'createDate': '50분 전', 'hit': 50},
    {'title': '뷔 포카 판매', 'category': '판매', 'writer_id': 'kpop_lover', 'createDate': '1달 전', 'hit': 40},
    {'title': '트와이스 나연 포카 판매', 'category': '판매', 'writer_id': 'generous_fan', 'createDate': '2일 전', 'hit': 145},
    {'title': '포카 정리합니다', 'category': '판매', 'writer_id': 'army_collector', 'createDate': '55분 전', 'hit': 67},
    {'title': '포카 교환', 'category': '교환', 'writer_id': 'happy_trader', 'createDate': '4시간 전', 'hit': 112},
    {'title': '정연 포카 팔아요', 'category': '판매', 'writer_id': 'creative_diver', 'createDate': '1시간 전', 'hit': 89},
]

def recent(request):
    # GET 요청에서 카테고리와 검색어를 받음
    category = request.GET.get('category', '전체')  # 기본값은 '전체'
    searchinput = request.GET.get('searchinput', '')

    # 카테고리 필터링
    if category != '전체':
        filtered_posts = [post for post in posts if post['category'] == category]
    else:
        filtered_posts = posts  # '전체'일때 모든 게시글을 표시

    # 검색어 필터링
    if searchinput:
        filtered_posts = [post for post in filtered_posts if searchinput.lower() in post['title'].lower()]
    
    # 페이지네이터
    paginator = Paginator(filtered_posts, 5)
    page = int(request.GET.get('page', 1))
    page_num = paginator.get_page(page)

    return render(request, 'recent.html', {'category':category, 'searchinput':searchinput, 'page_num':page_num})