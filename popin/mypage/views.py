from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
import json
from collections import defaultdict
from idols.models import Group, Member
from signupFT.models import User, UserRelation
from photocard.models import Photocard
from photocard.models import TempWish
from community.models import CompanionPost, SharingPost, ProxyPost
from django.shortcuts import get_object_or_404
from community.models import ExchangeReview
from django.views.decorators.http import require_POST

def profile(request, target_id=None):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    try:
        # 만약 target_id가 있으면 그걸로, 없으면 로그인 유저 기준으로
        user = User.objects.get(user_id=target_id or user_id)
        completed = Photocard.objects.filter(seller=user, sell_state = "후", buy_state = "후").count()
        first_group = user.bias_group.all().first()

        if first_group:
            group_logo = first_group.group_logo if first_group.group_logo else None
        else:
            group_logo = None
        
        context = {
            # 수정 시 닉네임, 자기소개, 프로필 이미지, 최애 멤버는 프로필에서 불러온 정보로 모달에 넘겨 주세요!
            # 수정할 시에는 update_profile ajax 통신!
            # 첫 프로필 진입으로 키워드 부분이 보여질 경우 해당 members, groups 반환 바랍니다
            'target_id': target_id or None,
            'nickname':user.nickname, # 닉네임
            'introduction':user.introduction, # 자기소개
            'group_logo': group_logo, # 그룹 로고 이미지
            'selling_photocards':user.selling_photocards.count(), # 보유 포카 수
            'completed':completed, # 교환 완료 수
            'manners_score':user.manners_score, # 평점
            'profile_image':user.profile_image, # 프로필 이미지
            'members': user.bias_member.all(), # 최애 멤버 (member.group.name으로 최애 그룹 이름 접근 가능)
            'groups': user.bias_group.all(), # 최애 그룹
            'bias_pairs': zip(user.bias_group.all(), user.bias_member.all())  # ✅ 그룹-멤버 쌍
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
        user_id = request.session.get('user_id') # 로그인 유저
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)
        try:
            target_user_id = request.POST.get('target_user_id')
            query_user_id = target_user_id if target_user_id else user_id
            user = User.objects.get(user_id=query_user_id)
            
            # 유저가 설정한 최애 그룹, 멤버 키워드 확인
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
                    'tag' : poca.tag,
                    'trade_type': poca.trade_type,
                    'trade_state' : poca.get_sell_state_display(),
                    'place': poca.place,
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
            target_user_id = request.POST.get('target_user_id')
            query_user_id = target_user_id if target_user_id else user_id
            user = User.objects.get(user_id=query_user_id)
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
        photocard = item.photocard
        wishlist_data.append({
            'pno': photocard.pno,
            'title': photocard.title,
            'album': photocard.album,
            'image_url': photocard.image.url,
            'trade_type' : photocard.trade_type,
            'trade_state': photocard.get_sell_state_display(),
            'place': photocard.place,
            'available_at' : photocard.available_at,
            'price' : photocard.price,
        })

    return JsonResponse({'wishlist': wishlist_data})

# 교환거래(내역)
def trade(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)

        try:
            target_user_id = request.POST.get('target_user_id')
            query_user_id = target_user_id if target_user_id else user_id
            user = User.objects.get(user_id=query_user_id)
            
            sell_poca = Photocard.objects.filter(seller=user, trade_type="판매").exclude(sell_state='전')
            buy_poca = Photocard.objects.filter(buyer=user, trade_type="판매").exclude(buy_state='전')
            exchange_poca = Photocard.objects.exclude(buy_state='전').filter(Q(seller=user) | Q(buyer=user), trade_type="교환")

            sell_data = [
                {
                    'title': photocard.title,
                    'trade_type': photocard.trade_type,
                    'trade_state': photocard.get_sell_state_display(),
                    'album': photocard.album,
                    'image_url': photocard.image.url if photocard.image else '',
                    'pno': photocard.pno,
                    'member': photocard.member.name if photocard.member else '',
                    'price' : photocard.price,
                    'place': photocard.place,
                    'available_at':photocard.available_at,
                }
                for photocard in sell_poca
            ]

            buy_data = [
                {
                    'title': photocard.title,
                    'trade_type': photocard.trade_type,
                    'trade_state': photocard.get_sell_state_display(),
                    'album': photocard.album,
                    'image_url': photocard.image.url if photocard.image else '',
                    'pno': photocard.pno,
                    'member': photocard.member.name if photocard.member else '',
                    'price' : photocard.price,
                    'place': photocard.place,
                    'available_at':photocard.available_at,
                }
                for photocard in buy_poca
            ]
            
            exchange_data = [
                {
                    'title': photocard.title,
                    'trade_type': photocard.trade_type,
                    'trade_state': photocard.get_sell_state_display(),
                    'album': photocard.album,
                    'image_url': photocard.image.url if photocard.image else '',
                    'pno': photocard.pno,
                    'member': photocard.member.name if photocard.member else '',
                    'price' : photocard.price,
                    'place': photocard.place,
                    'available_at':photocard.available_at,
                }
                for photocard in exchange_poca
            ]

            return JsonResponse({
                'sell_poca': sell_data,
                'buy_poca': buy_data,
                'exchange_poca':exchange_data,
            })

        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)


# #커뮤니티 작성글(동행, 나눔, 대리구매) 
def review(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return JsonResponse({"error": "로그인 필요"}, status=403)

    try:
        user = User.objects.get(user_id=user_id)

        # 사용자 작성 게시글 조회
        
        companion_posts = CompanionPost.objects.filter(author=user).values(
            "id","title", "created_at", "views", "comments_count"
        )

        # 나눔
        sharing_posts = SharingPost.objects.filter(author=user).values(
            "id","title", "created_at", "views"
        )

        # 대리구매
        proxy_posts = ProxyPost.objects.filter(author=user).values(
           "id","title", "created_at", "views"
        )

        return JsonResponse({
            "companion": list(companion_posts),
            "sharing": list(sharing_posts),
            "proxy": list(proxy_posts),
        })

    except User.DoesNotExist:
        return JsonResponse({"error": "사용자 없음"}, status=404)
###########################################
#내가쓴 교환판매후기

def my_written_reviews(request):
    user_id = request.session.get("user_id")
    user = get_object_or_404(User, user_id=user_id)
    
    reviews = ExchangeReview.objects.filter(writer=user).values(
        'id', 'title', 'created_at', 'overall_score', 'content', 'partner__nickname'
    )
    return JsonResponse({'written_reviews': list(reviews)})


# 내가받은 교환판매후기 
def my_received_reviews(request):
    # GET으로 요청 받기
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)

        try:
            target_user_id = request.POST.get('target_user_id')
            query_user_id = target_user_id if target_user_id else user_id
            user = User.objects.get(user_id=query_user_id)
        
            reviews = ExchangeReview.objects.filter(partner=user).select_related("writer").values(
                'id', 'title', 'content', 'overall_score', 'created_at', 'writer__nickname'
            )

            # 날짜 문자열 처리
            received_data = [
                {
                    'title': review['title'],
                    'content': review['content'],
                    'overall_score': review['overall_score'],
                    'created_at':  review['created_at'].strftime('%Y-%m-%d'),
                    'writer': review['writer__nickname'],
                }
                for review in reviews
            ]

        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

        reviews = ExchangeReview.objects.filter(partner=user).select_related("writer").values(
            'id', 'title', 'content', 'overall_score', 'created_at', 'writer__nickname'
        )

        received_data = [
            {
                'id': review['id'],  # ✅ id도 같이 보내줘야 JS에서 undefined 안 뜸
                'title': review['title'],
                'content': review['content'],
                'overall_score': review['overall_score'],
                'created_at': review['created_at'].strftime('%Y-%m-%d'),
                'writer': review['writer__nickname'],
            }
            for review in reviews
        ]

        return JsonResponse({'received_reviews': received_data})

    # GET이 아닌 요청은 405
    return JsonResponse({'error': 'GET 요청만 지원합니다.'}, status=405)
     
###########################################
# 차단 유저 관리
def block_list(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)

        try:
            user = User.objects.get(user_id=user_id)
            block_users = user.initiated_relations.filter(relation_type='BLOCK')
            
            block_data = []
            for u in block_users :
                block_data.append({
                        'user_id': u.to_user.user_id,
                        'name': u.to_user.name,
                        'reason': u.reason,
                    })

            return JsonResponse({'blocked_users': block_data})

        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

# 프로필 수정 (수정중)
def update_profile(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'message': '로그인 필요'}, status=401)
        
        try:
            user = User.objects.get(user_id=user_id)

            # 텍스트 데이터는 request.POST에서
            user.nickname = request.POST.get('nickname', user.nickname)
            user.introduction = request.POST.get('introduction', user.introduction)
        
            # 파일은 request.FILES에서
            profile_img = request.FILES.get('profile_image')
            if profile_img:
                user.profile_image = profile_img
                
            # 최애 그룹/멤버 2개까지
            favorite_group = request.POST.get('favorite_group')
            favorite_member = request.POST.get('favorite_member')
            second_group = request.POST.get('second_group')
            second_member = request.POST.get('second_member')

            groups = []
            members = []

            if favorite_group and favorite_member:
                g1 = Group.objects.get(name=favorite_group)
                m1 = Member.objects.get(name=favorite_member, group=g1)
                groups.append(g1)
                members.append(m1)

            if second_group and second_member:
                g2 = Group.objects.get(name=second_group)
                m2 = Member.objects.get(name=second_member, group=g2)
                groups.append(g2)
                members.append(m2)
            else:
                bias_pairs = zip(user.bias_group.all(), user.bias_member.all())
                return render(request, '/mypage/profile/', {
                    'bias_pairs': bias_pairs,
                    'nickname': user.nickname,
                    'introduction': user.introduction,
                    'profile_image': user.profile_image.url if user.profile_image else '',
                })
            user.bias_group.set(groups)
            user.bias_member.set(members)
            

            user.save()
            return JsonResponse({'message': '프로필 수정 성공'}, status=200)

        except Exception as e:
            return JsonResponse({'message': f'오류 발생: {str(e)}'}, status=500)

    return JsonResponse({'message': '허용되지 않은 메서드입니다.'}, status=405)

def update_blocklist(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'message': '로그인 필요'}, status=401)
        
        try:
            from_user = User.objects.get(user_id=user_id) # 현재 로그인한 유저 
            
            body = json.loads(request.body)
            id = body.get('id')
            to_user = User.objects.get(user_id = id) # 차단한 유저 
            
            relation = UserRelation.objects.get(to_user=to_user, from_user=from_user, relation_type="BLOCK")
            if not relation:
                return JsonResponse({'error': '관계를 찾을 수 없습니다.'}, status=404)
            else:
                relation.delete()
                block_data = [
                        {
                            'user_id': to_user.name,
                            'message': to_user.name + " 을 차단 해제하였습니다.",
                        }
                    ]
            return JsonResponse({'blocked_users': block_data})

        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)