from django.shortcuts import render, redirect
from django.http import JsonResponse

from collections import defaultdict

from signupFT.models import User
from photocard.models import Photocard
from photocard.models import TempWish


def pchange(request):
    return render(request,'mypage/pchange.html')

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
    
def test(request):
    return render(request, 'mypage/test.html')

def keyword(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)
        
        try:
            user = User.objects.get(user_id=user_id)
            groups = list(user.bias_group.values('id', 'name'))
            members = list(user.bias_member.values('id', 'name', 'group__name'))

            return JsonResponse({
                'groups': groups,
                'members': members,
            })
        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

def my_poca(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)
        
        try:
            user = User.objects.get(user_id=user_id)
            my_poca_qs = user.selling_photocards.select_related('member__group').all()
            print(my_poca_qs)

            album_dict = defaultdict(list)
            for card in my_poca_qs:
                print(card)
                album_dict[card.album].append({
                    'title': card.title,
                    'member': str(card.member),  # 예: "BTS - 정국"
                    'category': card.category,
                    'image_url': card.image.url if card.image else '',
                    'poca_state': card.poca_state,
                    'trade_type': card.trade_type,
                    'place': card.place,
                })
                print(album_dict)

            return JsonResponse({'my_poca': album_dict})
        
        except User.DoesNotExist:
            return JsonResponse({'error': '사용자를 찾을 수 없습니다.'}, status=404)

    return JsonResponse({'error': 'POST 요청만 허용됩니다.'}, status=400)

def wishlist(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    qs = TempWish.objects.filter(user=user)
    print(qs)
    
    context = {'wishlist':qs}
    return render(request, 'mypage/wishlist.html', context)

def trade(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(user_id=user_id)
    
    sell_poca = Photocard.objects.filter(seller=user).exclude(sell_state='전')
    
    buy_poca = Photocard.objects.filter(buyer=user).exclude(buy_state='전')
    
    print(sell_poca)
    print(buy_poca)
    
    context = {
        "sell_poca":sell_poca,
        "buy_poca":buy_poca,
    }
    return render(request, 'mypage/trade.html', context)