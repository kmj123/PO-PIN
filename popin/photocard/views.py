from django.shortcuts import render, redirect

from photocard.models import Photocard
from idols.models import Member
from photocard.models import TempUser

from django.db.models import Count
from datetime import date

# 포토카드 거래글 전체 읽어오기 (추후 위치 기반으로 수정 필요)
def list(request):
    qs = Photocard.objects.select_related('member__group').annotate(
        wish_count=Count('wished_by_users')
    )
    context = {'list': qs}
    return render(request, 'list.html', context)

# 선택 포토카드 거래글 상세정보
def view(request, pno):
    qs = Photocard.objects.get(pno=pno)
    context = {"info":qs}
    return render(request, 'view.html', context)

# 포토카드 거래글 작성
# 포토카드 거래글 작성
def write(request):
    if request.method == "GET" :
	# choices : select options 반환 >> PHOTOCARD model.py 참고!!
	# ex) Photocard.CATEGORY_CHOICES
	# > ('앨범', '앨범'),('특전', '특전'),('MD', 'MD'),('공방', '공방'),('기타', '기타'),
	# member : idol의 member 반환
        context = {
        'category_choices': Photocard.CATEGORY_CHOICES,
        'poca_state_choices': Photocard.P_STATE_CHOICES,
        'trade_type_choices': Photocard.TRADE_CHOICES,
        'place_choices': Photocard.PLACE_CHOICES,
        'member': Member.objects.all(),
        }
        return render(request, 'write.html', context)
        
    elif request.method == 'POST':
	# 제목, 이미지, 판매자, 카테고리, 앨범, 멤버, 하자상태, 태그, 거래 방식, 
	# 장소, 구매자 거래 상태(게시글 등록 시 거래중 설정), 거래날짜, 위도, 경도

        title = request.POST.get('title')
        image = request.FILES.get('image')
        
        seller=TempUser.objects.first() ## 로그인 구현 시 자동 지정 수정 필요 
        
        category=request.POST.get('category')
        album=request.POST.get('album')
        
        member=request.POST.get('member')
        group_name, member_name = member.split(' - ')
        member_obj = Member.objects.get(name=member_name, group__name=group_name)
        
        poca_state=request.POST.get('poca_state')
        tag=request.POST.get('tag', None)
        
        trade_type=request.POST.get('trade_type')
        place=request.POST.get('place')
        
        sell_state = '중'
        
        if request.POST.get('available_at') == "" :
            available_at = str(date.today())
        else:
            available_at = request.POST.get('available_at')
        
        latitude=request.POST.get('latitude')
        longitude=request.POST.get('longitude')
        
        print('-------------------------')
        print(title, image, seller, category, album, member, poca_state, tag, trade_type, place, sell_state, available_at, latitude, longitude)
        print('-------------------------')
        
        Photocard.objects.create(
            title=title, image=image, seller=seller, category=category, album=album, member=member_obj, poca_state=poca_state, tag=tag, trade_type=trade_type, place=place, sell_state=sell_state, available_at=available_at, latitude=latitude, longitude=longitude
        )
        return redirect('/photocard/list')