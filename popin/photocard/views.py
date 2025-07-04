from django.shortcuts import render, redirect

from signupFT.models import User
from photocard.models import Photocard
from idols.models import Member
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
    user_id = request.session.get('user_id')
    
    if user_id: # 유저 정보가 있는 경우
        latest_list = request.session.get('latest_poca', []) # 세선 안에 latest_poca 있으면 리스트 불러오기 or []
        
        if pno in latest_list: # 리스트 안에 해당 게시글 pno가 있을 때
            if latest_list[0] != pno: # pno가 리스트 안에 존재하지만 가장 최근이 아닐 때
                latest_list.remove(pno) # 리스트 내 pno 제거
                latest_list.insert(0,pno) # 가장 최근으로 insert
        else:
            latest_list.insert(0,pno) # 가장 최근으로 insert
            
        request.session['latest_poca'] = latest_list
            
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
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
        
    try:
        user = User.objects.get(user_id=user_id)
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
            
            seller = user
            
            category=request.POST.get('category')
            album=request.POST.get('album')
            
            member=request.POST.get('member')
            # group_name, member_name = member.split(' - ')
            # member_obj = Member.objects.get(name=member_name, group__name=group_name)
            
            poca_state=request.POST.get('poca_state')
            # 태그 문자리스트로 get
            tag=request.POST.getlist('tag', None)
            
            trade_type=request.POST.get('trade_type')
            place=request.POST.get('place')
            
            sell_state = '중' # 등록 시 default
            
            if request.POST.get('available_at') == "" :
                available_at = str(date.today())
            else:
                available_at = request.POST.get('available_at')
            
            # 위치 문자열 -> 숫자열로 전환
            lat = request.POST.get('latitude')
            lng = request.POST.get('longitude')

            latitude = float(lat) if lat else None
            longitude = float(lng) if lng else None
            
            # Photocard 객체 생성
            Photocard.objects.create(
                title=title, image=image, seller=seller, category=category, album=album, member=member, poca_state=poca_state, tag=tag, trade_type=trade_type, place=place, sell_state=sell_state, available_at=available_at, latitude=latitude, longitude=longitude
            )
            print(title, image,seller,category, album, member, poca_state,tag,trade_type,place,sell_state,available_at)
            # redirect로 이동
            return redirect('/photocard/list')
            
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비

# 포토카드 거래글 수정
def update(request, pno):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    user = User.objects.get(user_id=user_id) # 사용자
    photo_qs = Photocard.objects.get(pno=pno) # 수정 포토카드 게시글
    
    # 사용자 아이디와 수정 포토카드 게시글의 판매자가 같을 시 True
    if user.user_id == photo_qs.seller.user_id :
        try:
            if request.method == "GET":
                member_qs = Member.objects.all() # DB 내 아이돌 전체
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
                photo_qs.title = request.POST.get('title') # 제목
                photo_qs.image = request.FILES.get('image') # 이미지
                
                photo_qs.category=request.POST.get('category') # 카테고리 (공방, 앨범)
                photo_qs.album=request.POST.get('album') # 활동 시기 앨범 (1집, 2집)
                
                member_id=request.POST.get('member') # 아이돌
                member_obj = Member.objects.get(pk=int(member_id))
                photo_qs.member = member_obj
                
                photo_qs.poca_state=request.POST.get('poca_state') # 포카 하자 상태
                photo_qs.tag=request.POST.get('tag', None) # 태그
                
                photo_qs.trade_type=request.POST.get('trade_type') # 거래 방식
                photo_qs.place=request.POST.get('place') # 장소 (올공, 더현대)
                
                photo_qs.sell_state = request.POST.get('sell_state') # 판매자 거래 상태
                
                # 거래 가능일
                if request.POST.get('available_at') == "" :
                    available_at = str(date.today())
                else:
                    available_at = request.POST.get('available_at')
                
                photo_qs.available_at = available_at 
                
                #거래 위치 위도 경도
                photo_qs.latitude=request.POST.get('latitude')
                photo_qs.longitude=request.POST.get('longitude')
                
                # 새로 설정한 값 수정
                photo_qs.save()
                
                # 수정 완료 후 리다이렉트
                return redirect('/photocard/list')
        except User.DoesNotExist:
            return redirect('login:main')  # 예외 상황 대비
    else: 
        # 사용자 아이디와 판매자 아이디가 일치하지 않을 경우 리다이렉트
        return redirect('/photocard/list')
                
        

# 포토카드 거래글 삭제
def delete(request, pno):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로
    
    user = User.objects.get(user_id=user_id) # 사용자
    photo_qs = Photocard.objects.get(pno=pno) # 수정 포토카드 게시글
    
    # 사용자 아이디와 수정 포토카드 게시글의 판매자가 같을 시 True
    if user.user_id == photo_qs.seller.user_id :
        Photocard.objects.get(pno=pno).delete()
        
    return redirect('/photocard/list/')

# 포토카드 위시 등록 & 삭제
def wish(request, pno):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        user = User.objects.get(user_id=user_id)
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
    
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비

