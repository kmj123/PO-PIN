from django.shortcuts import render, redirect
from django.http import JsonResponse

from collections import defaultdict

from signupFT.models import User
from photocard.models import Photocard
from photocard.models import TempWish

def profile(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        user = User.objects.get(user_id=user_id) # 로그인한 사용자
        completed = Photocard.objects.filter(seller=user.user_id, sell_state = "후", buy_state = "후").count()
        print(user)
        context = {
            'user':user,
            'completed':completed,
            }
        
        return render(request,'mypage/profile.html', context)
    
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비
    
# 기능 테스트 html 페이지 > 기능 구현 완료 시 삭제
def test(request):
    return render(request, 'mypage/test.html')

# 키워드
def keyword(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)
        try:
            # 유저가 설정한 최애 그룹, 멤버 키워드 확인
            user = User.objects.get(user_id=user_id)
            groups = list(user.bias_group.values('id', 'name'))
            members = list(user.bias_member.values('id', 'name', 'group__name'))

            print(groups, members)

            return JsonResponse({
                'groups': groups,
                'members': members,
            })
        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

# 최근 본 글 
def latest_post(request):
    if request.method == 'POST':
        latestList = request.session.get('latest_poca', [])[:10]
        photocards = []

        for pno in latestList:
            try:
                poca = Photocard.objects.get(pno=pno)
                photocards.append({
                    'title': poca.title,
                    'album': poca.album,
                    'image_url': poca.image.url if poca.image else '',
                    'pno': poca.pno,
                    'member': poca.member.name if poca.member else '',
                    'created_at':poca.created_at,
                    'available_at':poca.available_at,
                })
            except Photocard.DoesNotExist:
                continue

        return JsonResponse({
            'count': len(photocards),
            'photocards': photocards
        })

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

# 사용자 보유 포토카드 (마이포카)
def my_poca(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)
        
        try:
            user = User.objects.get(user_id=user_id)
            my_poca_qs = Photocard.objects.select_related('member__group').filter(seller=user)
            
            # 그룹 -> 앨범 -> 포토카드 묶기
            group_album_dict = defaultdict(lambda: defaultdict(list))
            
            for poca in my_poca_qs:
                group_name = poca.member.group.name if poca.member and poca.member.group else "기타"
                album_name = poca.album or "미지정 앨범"
                group_album_dict[group_name][album_name].append(poca)

            # JSON 직렬화 가능한 형태로 변환
            group_album_dict_json = {}

            for group_name, albums in group_album_dict.items():
                group_album_dict_json[group_name] = {}
                for album_name, photocards in albums.items():
                    group_album_dict_json[group_name][album_name] = [
                        {
                            'title': photocard.title,
                            'album': photocard.album,
                            'image_url': photocard.image.url if photocard.image else '',
                            'member': photocard.member.name if photocard.member else '',
                            'category': photocard.category,
                            'pno': photocard.pno,
                        }
                        for photocard in photocards
                    ]

            return JsonResponse({'group_album_dict': group_album_dict_json})

        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

# 위시리스트 
def wishlist(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    qs = TempWish.objects.filter(user=user).select_related('photocard')

    wishlist_data = []
    for item in qs:
        wishlist_data.append({
            'pno': item.photocard.pno,
            'title': item.photocard.title,
            'album': item.photocard.album,
            'image_url': item.photocard.image.url,
            'trade_state': item.photocard.sell_state,
        })

    return JsonResponse({'wishlist': wishlist_data})

# 교환거래(내역)
def trade(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)

        try:
            user = User.objects.get(user_id=user_id)
            
            sell_poca = Photocard.objects.filter(seller=user).exclude(sell_state='전')
            buy_poca = Photocard.objects.filter(buyer=user).exclude(buy_state='전')

            sell_data = [
                {
                    'title': photocard.title,
                    'trade_type': photocard.trade_type,
                    'trade_state': photocard.sell_state,
                    'album': photocard.album,
                    'image_url': photocard.image.url if photocard.image else '',
                    'pno': photocard.pno,
                    'member': photocard.member.name if photocard.member else '',
                }
                for photocard in sell_poca
            ]

            buy_data = [
                {
                    'title': photocard.title,
                    'trade_type': photocard.trade_type,
                    'trade_state': photocard.buy_state,
                    'album': photocard.album,
                    'image_url': photocard.image.url if photocard.image else '',
                    'pno': photocard.pno,
                    'member': photocard.member.name if photocard.member else '',
                }
                for photocard in buy_poca
            ]

            return JsonResponse({
                'sell_poca': sell_data,
                'buy_poca': buy_data,
            })

        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

# # 후기글
# def review(request):
#     return JsonResponse()

# # 커뮤니티 작성글
# def review(request):
#     return JsonResponse()

# 차단 유저 관리
def block_list(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)

        try:
            user = User.objects.get(user_id=user_id)
            block_users = user.initiated_relations.filter(relation_type='BLOCK')
            
            for u in block_users :
                block_data = [
                    {
                        'user_id': u.to_user.user_id,
                        'name': u.to_user.name,
                    }
                ]

            return JsonResponse({'blocked_users': block_data})

        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

# 프로필 수정 (수정중)
def update(request):
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    
    context = {
        'user':user
    }
    return render(request, 'mypage/update.html', context)
