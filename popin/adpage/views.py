from django.shortcuts import render, redirect
from django.db.models.functions import ExtractMonth,ExtractYear
from django.db.models import Count, Q
from collections import defaultdict
from django.http import JsonResponse
import json
from signupFT.models import User
from photocard.models import Photocard
from adpage.models import Notice, NoticeImage
from django.utils import timezone
from community.models import (ExchangeReview, SharingPost, ProxyPost, CompanionPost, StatusPost)
from django.shortcuts import get_object_or_404

# Create your views here.
def main(request) :
        user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

        if not user_id:
            return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

        try:
            print(user_id)
            admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
            
            # 전체 게시글 (** 커뮤니티 수정 필요)
            total_photocards = Photocard.objects.all().count()
            # 전체 사용자
            total_users = User.objects.all().count() 
            # 대기중인 신고 (게시글)
            pending_reports = (
                ExchangeReview.objects.filter(report_level='pending').count() +
                SharingPost.objects.filter(report_level='pending').count() +
                ProxyPost.objects.filter(report_level='pending').count() +
                CompanionPost.objects.filter(report_level='pending').count() +
                StatusPost.objects.filter(report_level='pending').count())
            # 차단 사용자
            block_users = User.objects.filter(state=3).count()
            
            # 월별 거래 통계
            monthly_trade_stats = Photocard.objects.annotate(
                year=ExtractYear('available_at'),
                month=ExtractMonth('available_at')
            ).values(
                'year', 'month', 'trade_type'
            ).annotate(
                count=Count('pno')
            ).order_by(
                'year', 'month', 'trade_type'
            ).exclude(
                sell_state='전'
            )
                
            # 집계 구조 준비
            month_set = set()
            count_data = defaultdict(lambda: {'판매': 0, '교환': 0})
            
            for entry in monthly_trade_stats:
                year = entry['year']
                month = entry['month']
                trade_type = entry['trade_type']
                count = entry['count']

                label = f"{year}-{str(month).zfill(2)}"  # 예: "2025-07"
                month_set.add(label)
                count_data[label][trade_type] = count

            # 정렬된 결과로 리스트 준비
            sorted_months = sorted(list(month_set))
            all_counts = [count_data[m]['판매'] + count_data[m]['교환'] for m in sorted_months]
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
                'pending_reports': pending_reports, 
                'months':json.dumps(sorted_months), # 월별 거래 통계 (month)
                'all' : all_counts, # 월별 거래 통계 (총판)
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
        
        user_list = User.objects.annotate(
            report_count=Count(
                'received_relations',
                filter=Q(received_relations__relation_type='REPORT')
            )
        ).values('user_id','nickname','email','state','report_count').exclude(state=0)
        
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

def delete_user(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)
    
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        body = json.loads(request.body)
        ids = body.get('ids')  # 리스트 형태로 받아야 함
        
        if not ids or not isinstance(ids, list):
            return JsonResponse({'error': '유효한 사용자 ID 리스트가 필요합니다.'}, status=400)
        
        results = []
        for uid in ids:
            try:
                user = User.objects.get(user_id=uid)
                user.delete()
                message = uid + " 삭제 완료"
                results.append({'user_id': uid, 'message': message})
                
            except User.DoesNotExist:
                results.append({'user_id': uid, 'error': '사용자 없음'})

        return JsonResponse({
            'success': True,
            'processed': len(results),
            'results': results
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def block_user(request):
    if request.method != "POST":
        return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=405)
    
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)

    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        body = json.loads(request.body)
        ids = body.get('ids')  # 리스트 형태로 받아야 함
        
        if not ids or not isinstance(ids, list):
            return JsonResponse({'error': '유효한 사용자 ID 리스트가 필요합니다.'}, status=400)
        
        results = []
        for uid in ids:
            try:
                user = User.objects.get(user_id=uid)
                if user.state == 3:
                    user.state = 1
                    message = "차단 → 일반"
                elif user.state == 1:
                    user.state = 3
                    message = "일반 → 차단"
                else:
                    message = f"변경 안됨 (현재 상태: {user.state})"
                user.save()
                results.append({'user_id': uid, 'new_state': user.state, 'message': message})
            except User.DoesNotExist:
                results.append({'user_id': uid, 'error': '사용자 없음'})

        return JsonResponse({
            'success': True,
            'processed': len(results),
            'results': results
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

###########

def post(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login:loginp')

    try:
        admin = User.objects.get(user_id=user_id, state=0)
    except User.DoesNotExist:
        return redirect('home:main')

    today = timezone.now().date()

    def convert_status(level):
        return {
            'normal': '정상',
            'pending': '대기',
            'hidden': '삭제',
        }.get(level, '정상')

    # 🔥 신고수가 1 이상인 글만 가져오는 함수
    def get_reported_posts(queryset, board_name):
        posts = []
        for post in queryset.filter(report_count__gte=1):  # ✅ 여기서 report_level → report_count로 변경
            writer = getattr(post, 'writer', None)
            if writer is None:
                writer = getattr(post, 'author', None)

            posts.append({
                'id': post.pk,
                'board': board_name,
                'title': post.title,
                'writer': writer.nickname if writer else '알 수 없음',
                'created_at': post.created_at.strftime('%Y-%m-%d'),
                'report_count': post.report_count,
                'status': convert_status(post.report_level),
            })
        return posts

    posts = (
        get_reported_posts(ExchangeReview.objects.all(), '교환후기') +
        get_reported_posts(SharingPost.objects.all(), '나눔') +
        get_reported_posts(ProxyPost.objects.all(), '대리구매') +
        get_reported_posts(CompanionPost.objects.all(), '동행') +
        get_reported_posts(StatusPost.objects.all(), '현황공유')
    )

    all_count = (
        ExchangeReview.objects.count() +
        SharingPost.objects.count() +
        ProxyPost.objects.count() +
        CompanionPost.objects.count() +
        StatusPost.objects.count()
    )

    # ✅ 신고된 글 수 역시 report_count 기준으로 변경
    reported_count = (
        ExchangeReview.objects.filter(report_count__gte=1).count() +
        SharingPost.objects.filter(report_count__gte=1).count() +
        ProxyPost.objects.filter(report_count__gte=1).count() +
        CompanionPost.objects.filter(report_count__gte=1).count() +
        StatusPost.objects.filter(report_count__gte=1).count()
    )

    today_count = (
        ExchangeReview.objects.filter(created_at__date=today).count() +
        SharingPost.objects.filter(created_at__date=today).count() +
        ProxyPost.objects.filter(created_at__date=today).count() +
        CompanionPost.objects.filter(created_at__date=today).count() +
        StatusPost.objects.filter(created_at__date=today).count()
    )

    context = {
        'posts': posts,
        'total_posts': all_count,
        'reported_posts': reported_count,
        'today_posts': today_count,
    }
    return render(request, 'admin/managePost.html', context)
    



def postV(request, board, pk):
    board_map = {
        '교환후기': ExchangeReview,
        '나눔': SharingPost,
        '대리구매': ProxyPost,
        '동행': CompanionPost,
        '현황공유': StatusPost,
    }

    model = board_map.get(board)
    if not model:
        return render(request, 'admin/error.html', {'message': '잘못된 게시판입니다.'})

    post_obj = get_object_or_404(model, pk=pk)

    writer = getattr(post_obj, 'writer', None) or getattr(post_obj, 'author', None)
    partner = getattr(post_obj, 'partner', None)
    content = getattr(post_obj, 'content', '')
    score = getattr(post_obj, 'overall_score', None)
    image = post_obj.images.first().image.url if hasattr(post_obj, 'images') and post_obj.images.exists() else None

    context = {
        'post': {
            'board': board,
            'title': post_obj.title,
            'writer': writer.nickname if writer else '',
            'partner': partner.nickname if partner else '-',
            'created_at': post_obj.created_at.strftime('%Y-%m-%d'),
            'content': content,
            'score': score,
            'image': image,
        }
    }

    return render(request, "admin/managePost_view.html", context)

def notice(request) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        qs = Notice.objects.all().order_by('-is_pinned', '-created_at').values('id', 'title', 'created_at', 'views')
        
        print(qs)
        context = {
            "notice_list": qs, 
        }
        
        return render(request,"admin/notice.html", context)

    except:
        return redirect('adpage:main')

def noticeV(request, notice_id) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        notice = Notice.objects.get(id=notice_id)
        notice.views += 1
        notice.save()
        
        images = NoticeImage.objects.filter(notice=notice)
        
        context = {
            'notice':notice,
            'images':images
        }
        return render(request,"admin/notice_view.html", context)
    
    except User.DoesNotExist:
        return redirect('home:main')
    except Notice.DoesNotExist:
        return redirect('adpage:notice')

def noticeW(request) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용
        
        if request.method == "GET":
            return render(request,"admin/notice_write.html")
        elif request.method == "POST":
            notice_type = request.POST.get('notice_type')
            title = request.POST.get('title')
            is_pinned = True if request.POST.get('is_pinned') == 'on' else False
            content = request.POST.get('content')
            images = request.FILES.getlist('images')
            
            print("=====================")
            print("작성 정보: ")
            print(notice_type, title, is_pinned, content, images)
            print("=====================")
            
            notice = Notice.objects.create(notice_type=notice_type, title=title, is_pinned=is_pinned, content=content)
            
            for image in images:
                NoticeImage.objects.create(notice=notice, image=image)
            
            return render(request, "admin/notice_write.html")
    
    except User.DoesNotExist:
        return redirect('login:loginp')  # 로그인 안 되어있거나 권한 없으면 로그인 페이지로
    except Exception as e:
        # 에러 로그 찍어보세요 (디버깅용)
        print(f"Error: {e}")
        return redirect('home:main')



def noticeR(request, notice_id) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        if request.method == "GET":
            notice = Notice.objects.get(id=notice_id)
            images = NoticeImage.objects.filter(notice=notice)
            
            context = {
                "notice":notice,
                "images":images,
            }
            return render(request,"admin/notice_rewrite.html", context)
        
        elif request.method == "POST":
            notice_type = request.POST.get('notice_type')
            title = request.POST.get('title')
            is_pinned = True if request.POST.get('is_pinned') == 'on' else False
            content = request.POST.get('content')
            images = request.FILES.getlist('images')
            
            notice = Notice.objects.get(id = notice_id)
            
            notice.notice_type = notice_type
            notice.title = title
            notice.is_pinned = is_pinned
            notice.content = content
            
            if images:
                for img in NoticeImage.objects.filter(notice=notice):
                    img.image.delete(save=False)  # 실제 파일 삭제
                    img.delete()                  # 레코드 삭제
                    
                for image in images:
                    NoticeImage.objects.create(notice=notice, image=image)
            
            notice.save()
            
            return redirect('adpage:notice')
    
    
    except User.DoesNotExist:
        return redirect('login:loginp')  # 로그인 안 되어있거나 권한 없으면 로그인 페이지로    
    # except Exception as e:
    #     # 에러 로그 찍어보세요 (디버깅용)
    #     print(f"Error: {e}")
    #     return redirect('home:main')
    
def noticeD(request, notice_id) :
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        admin = User.objects.get(user_id=user_id, state=0) # 로그인한 사용자
        Notice.objects.get(id=notice_id).delete()
        return redirect('adpage:notice')
    except:
        return redirect('home:main')  # 예외 상황 대비