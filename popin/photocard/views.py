from django.shortcuts import render, redirect

from photocard.models import Photocard
from idols.models import Member
from photocard.models import TempUser
from photocard.models import TempWish

from django.db.models import Count
from datetime import date

# 포토카드 거래글 전체 읽어오기 (추후 위치 기반으로 수정 필요)
def list(request):
    # 쿼리 파라미터 받아오기
    idol_names = request.GET.getlist('idol')
    place = request.GET.get('place')
    category = request.GET.get('category')
    sort = request.GET.get('sort')
    
    # 전체 포토카드 리스트 불러오기
    photocards = Photocard.objects.select_related('member__group').annotate(
        wish_count=Count('wished_by_users')
    )
    
    # 조건부 필터링 (값이 있을 경우에만 필터링)
    if idol_names:
        photocards = photocards.filter(member__name__in=idol_names)
    if place:
        photocards = photocards.filter(place=place)
    if category:
        photocards = photocards.filter(category=category)
        
    # 좋아요 순 정렬 옵션 적용
    if sort == 'likes':
        photocards = photocards.annotate(wish_count=Count('wished_by_users')).order_by('-wish_count')
        
    
    
    context = {'list': photocards}
    return render(request, 'list.html', context)

# 선택 포토카드 거래글 상세정보
def view(request, pno):
    # pno 포토카드 불러오기
    qs = Photocard.objects.get(pno=pno)
    
    # 포토카드 상세정보 반환
    context = {"info":qs}
    return render(request, 'view.html', context)
  
def exchange(request):
    return render(request, 'exchange.html')

def detail(request):
    return render(request, 'pocadetail.html')

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
        # 작성 버튼 클릭 시 필요한 필드 정보
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
        
        sell_state = '중' # 등록 시 default
        
        if request.POST.get('available_at') == "" :
            available_at = str(date.today())
        else:
            available_at = request.POST.get('available_at')
        
        latitude=request.POST.get('latitude')
        longitude=request.POST.get('longitude')
        
        print('-------------------------')
        print(title, image, seller, category, album, member, poca_state, tag, trade_type, place, sell_state, available_at, latitude, longitude)
        print('-------------------------')
        
        # Photocard 객체 생성
        Photocard.objects.create(
            title=title, image=image, seller=seller, category=category, album=album, member=member_obj, poca_state=poca_state, tag=tag, trade_type=trade_type, place=place, sell_state=sell_state, available_at=available_at, latitude=latitude, longitude=longitude
        )
        
        # redirect로 이동
        return redirect('/photocard/list')

# 포토카드 거래글 수정
def update(request, pno):
    # 포토카드 상세정보 불러오기 (context 작성 참고)
    photo_qs = Photocard.objects.get(pno=pno)
    if request.method == "GET":
        
        member_qs = Member.objects.all()
        context = {
            'category_choices': Photocard.CATEGORY_CHOICES,
            'poca_state_choices': Photocard.P_STATE_CHOICES,
            'trade_type_choices': Photocard.TRADE_CHOICES,
            'place_choices': Photocard.PLACE_CHOICES,
            'trade_state_choices' : Photocard.TRADE_STATE_CHOICES,
            'member': member_qs,
            'photocard': photo_qs
        }
        return render(request, 'update.html', context)
    
    # 포토카드 상세정보 수정
    elif request.method == "POST":
        photo_qs.title = request.POST.get('title')
        photo_qs.image = request.FILES.get('image')
        
        photo_qs.category=request.POST.get('category')
        photo_qs.album=request.POST.get('album')
        
        member_id=request.POST.get('member')
        member_obj = Member.objects.get(pk=int(member_id))
        photo_qs.member = member_obj
        
        photo_qs.poca_state=request.POST.get('poca_state')
        photo_qs.tag=request.POST.get('tag', None)
        
        photo_qs.trade_type=request.POST.get('trade_type')
        photo_qs.place=request.POST.get('place')
        
        photo_qs.sell_state = request.POST.get('sell_state')
        
        if request.POST.get('available_at') == "" :
            available_at = str(date.today())
        else:
            available_at = request.POST.get('available_at')
        
        photo_qs.available_at = available_at
        
        photo_qs.latitude=request.POST.get('latitude')
        photo_qs.longitude=request.POST.get('longitude')
        
        photo_qs.save()
        
        return redirect('/photocard/list')

# 포토카드 거래글 삭제
def delete(request, pno):
    Photocard.objects.get(pno=pno).delete()
    return redirect('/photocard/list/')

# 포토카드 위시 등록 & 삭제
def wish(request, pno):
    user = TempUser.objects.first() # 로그인 구현 후 수정
    photocard = Photocard.objects.get(pno=pno)
    
    try: 
        # 테이블에 해당 유저가 해당 포토카드를 위시 했는지 조회
        qs = TempWish.objects.get(user=user, photocard=photocard)
        # 이미 존재할 경우 삭제
        qs.delete()
    except:
        # 존재하지 않을 경우 추가
        TempWish.objects.create(user=user, photocard=photocard)
    
    return redirect('/photocard/list')
