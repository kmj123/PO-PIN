from django.shortcuts import render, redirect
from django.db.models.functions import ExtractMonth
from django.db.models import Count, Q
from collections import defaultdict

from signupFT.models import User
from photocard.models import Photocard
from adpage.models import Notice

# Create your views here.
def main(request) :
        user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

        if not user_id:
            return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

        try:
            print(user_id)
            admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
            
            # 전체 게시글
            total_photocards = Photocard.objects.all().count() 
            # 전체 사용자
            total_users = User.objects.all().count() 
            # 대기중인 신고 (게시글)
            
            # 차단 사용자
            block_users = User.objects.filter(state=3).count()
            
            # 월별 거래 통계
            monthly_trade_stats = Photocard.objects.annotate(
                    month=ExtractMonth('available_at')
                ).values(
                    'month', 'trade_type'
                ).annotate(
                    count=Count('pno')
                ).order_by(
                    'month', 'trade_type'
                ).exclude(
                    sell_state='전'
                )
                
            # 집계 구조 준비
            month_set = set()
            count_data = defaultdict(lambda: {'판매': 0, '교환': 0})

            for entry in monthly_trade_stats:
                month = entry['month']
                trade_type = entry['trade_type']
                count = entry['count']
                
                month_set.add(month)
                count_data[month][trade_type] = count

            # 정렬된 결과로 리스트 준비
            sorted_months = sorted(list(month_set))
            sale_counts = [count_data[m]['판매'] for m in sorted_months]
            exchange_counts = [count_data[m]['교환'] for m in sorted_months]
            
            print("==============================")
            print(monthly_trade_stats)
            print(sorted_months, sale_counts, exchange_counts)
            print("==============================")
            
            context = {
                'total_photocards':total_photocards, # 전체 게시글 (포토카드)
                'total_users':total_users,  # 전체 사용자
                'block_users':block_users, # 차단 사용자
                'months':sorted_months, # 월별 거래 통계 (month)
                'sell':sale_counts, # 월별 거래 통계 (판매)
                'exchange':exchange_counts, # 월별 거래 통계 (교환)
            }
            
            return render(request,"admin/main.html", context)
        
        except:
            return redirect('home:main')  # 예외 상황 대비
    

def user(request) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        total_users = User.objects.all().count() # 전체 사용자
        active_users = User.objects.filter(state=1).count() # 활성 사용자 (정상 사용자)
        block_users = User.objects.filter(state=3).count() # 정지된 사용자 (차단 사용자)
        
        print("======================")
        print(total_users, active_users, block_users)
        print("======================")
        
        state = request.GET.get('state')
        keyword = request.GET.get('keyword')
        
        user_list = User.objects.all().values('user_id','nickname','email','state') # 전체 유저 리스트
        
        # 조건부 필터링 (값이 있을 경우에만 필터링)
        if state:
            user_list = user_list.filter(state=state)
        if keyword:
            user_list = user_list.filter(Q(user_id=keyword) | Q(email=keyword))
        
        print("======================")
        print(user_list)
        print("======================")
        
        context = {
            "total_users":total_users, # 전체 사용자
            "active_users":active_users, # 활성 사용자 (정상 사용자)
            "block_users" : block_users, # 정지된 사용자 (차단 사용자)
            "users":user_list, # 전체 유저 리스트
        }
        return render(request,"admin/manageUser.html", context)
        
    except:
        return redirect('home:main')  # 예외 상황 대비

def delete_user(request, delete_user_id):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        delete_user = User.objects.get(user_id=delete_user_id)
        delete_user.delete()
        return redirect('adpage:main')  # 예외 상황 대비
    except:
        return redirect('home:main')  # 예외 상황 대비
    
def block_user(request, block_user_id):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        block_user = User.objects.get(user_id=block_user_id) # 해당 유저 객체
        
        if block_user.state == 3: # 차단 사용자일 경우
            block_user.state = 1 # 일반 사용자로 전환
            
        elif block_user.state == 1: # 일반 사용자의 경우
            block_user.state = 3 # 차단 사용자로 전환
            
        block_user.save() # 저장
        return redirect('adpage:main')  # 예외 상황 대비
    except:
        return redirect('home:main')  # 예외 상황 대비

def post(request) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        return render(request,"admin/managePost.html")
    except:
        return redirect('home:main')  # 예외 상황 대비
    

def postV(request) :
    return render(request,"admin/managePost_view.html")

def notice(request) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        qs = Notice.objects.all()
    return render(request,"admin/notice.html")

def noticeV(request, notice_id) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        qs = Notice.objects.get(id=notice_id)
        
        context = {
            'notice':qs,
        }
        return render(request,"admin/notice_view.html", context)
    
    except:
        return redirect('home:main')  # 예외 상황 대비

def noticeW(request) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        
        if request.method == "GET":
            return render(request,"admin/notice_view.html")
        elif request.method == "POST":
            notice_type = request.POST.get('notice_type')
            title = request.POST.get('title')
            is_pinned = request.POST.get('is_pinned')
            content = request.POST.get('content')
            file = request.FILE.get('file')
            
            qs = Notice.objects.create(notice_type=notice_type, title=title, is_pinned=is_pinned, content=content, file=file)
            print("============")
            print(qs)
            print("============")
        
            return render(request,"admin/notice_write.html")
    except:
        return redirect('home:main')  # 예외 상황 대비


def noticeR(request, notice_id) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        if request.method == "GET":
            return render(request,"admin/notice_rewrite.html")
        
        elif request.method == "POST":
            notice_type = request.POST.get('notice_type')
            title = request.POST.get('title')
            is_pinned = request.POST.get('is_pinned')
            content = request.POST.get('content')
            file = request.FILE.get('file')
            
            qs = Notice.objects.get(id = notice_id)
            
            qs.notice_type = notice_type
            qs.title = title
            qs.is_pinned = is_pinned
            qs.content = content
            qs.file = file
            qs.save()
            
            return redirect('adpage:notice')

    except:
        return redirect('home:main')  # 예외 상황 대비
    
def noticeD(request, notice_id) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        qs = Notice.objects.get(id=notice_id)
        qs.delete()
        return redirect('adpage:notice')
    except:
        return redirect('home:main')  # 예외 상황 대비

def test(request):
    return render(request, "admin/test.html")