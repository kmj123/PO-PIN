from django.shortcuts import render, redirect
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from collections import defaultdict

from signupFT.models import User
from photocard.models import Photocard

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
        
        user_list = User.objects.all().values('user_id','nickname','email','state') # 전체 유저 리스트
        
        print("======================")
        print(total_users, active_users, block_users)
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
    return render(request,"admin/notice.html")

def noticeV(request) :
    return render(request,"admin/notice_view.html")

def noticeW(request) :
    return render(request,"admin/notice_write.html")

def noticeR(request) :
    return render(request,"admin/notice_rewrite.html")

def test(request):
    return render(request, "admin/test.html")