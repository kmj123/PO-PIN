from django.shortcuts import render

from signupFT.models import User
from photocard.models import Photocard
from idols.models import Member
from photocard.models import TempWish
from pocadeco.models import DecoratedPhotocard

from django.db.models import Count
from datetime import date

from django.core.paginator import Paginator

# 데코포토 전체 리스트
# 데코포토 전체 리스트
def decolist(request):
    # 전체 데코포토 리스트 불러오기
    decoratedpoca = DecoratedPhotocard.objects.select_related('member__group').order_by('-created_at').annotate(wish_count=Count('wished_by_users'))
    searchInput = request.GET.get("search-input")
    
    # 필터용 쿼리 파라미터 받아오기
    searchgroup = request.GET.getlist('searchgroup')
    selected_members = request.GET.getlist('selectedMembers')
    sort = request.GET.get('sort')
    
    # 조건부 필터링 (값이 있을 경우에만 필터링)
    if searchgroup:
        decoratedpoca = decoratedpoca.filter(member__group__name__in=searchgroup)
        
    # 선택된 멤버가 있으면 필터링
    if selected_members:
        decoratedpoca = decoratedpoca.filter(member__name__in=selected_members)
    
    if searchInput:
        decoratedpoca = decoratedpoca.filter(title__icontains=searchInput)
    
    # 최신글 순 정렬 옵션 적용
    if sort == '최신순':
        decoratedpoca = decoratedpoca.order_by('-created_at')
    # 좋아요 순 정렬 옵션 적용
    if sort == '인기순':
        decoratedpoca = decoratedpoca.annotate(wish_count=Count('wished_by_users')).order_by('-wish_count')
    # 조회수 정렬 옵션 적용
    elif sort == '조회순':
        decoratedpoca = decoratedpoca.order_by('-hit')
        
    # 페이지네이터
    paginator = Paginator(decoratedpoca, 4)
    page = int(request.GET.get('page',1))
    page_num = paginator.get_page(page)
        
    deco_list = []
    for poca in page_num.object_list:
        if poca.tag:
            tags = poca.tag.split(',')
            deco_list.append({
                'id': poca.id,
                'title':poca.title,
                'result_image': poca.result_image,
                'user' : poca.user.nickname,
                'created_at': poca.created_at.strftime('%Y-%m-%d'),
                'hit': poca.hit,
                'member': poca.member.name,
                'group': poca.member.group.name,
                'tags': tags,
                'likes': poca.wish_count,
            })
        else:
            deco_list.append({
                'id': poca.id,
                'title':poca.title,
                'result_image': poca.result_image,
                'user' : poca.user.nickname,
                'created_at': poca.created_at.strftime('%Y-%m-%d'),
                'hit': poca.hit,
                'member': poca.member.name,
                'group': poca.member.group.name,
                'likes': poca.wish_count,
            })
        print(deco_list)
    
    context = {'decoList': deco_list, 'page_num':page_num, 'sort':sort, 'searchInput':searchInput}
    return render(request,'pocadeco/decolist.html', context)

# 데코포카 생성 페이지
def main(request):
    return render(request, 'pocadeco/main.html')

def mydecolist(request):
    return render(request, 'pocadeco/mydecolist.html')

# 데코포카 상세보기 페이지
def view(reqeust, id):
    decophotocard = DecoratedPhotocard.objects.get(id=id)
    tags = decophotocard.tag.split(',')
    context = {
        'nickname' : decophotocard.user.nickname,
        'title': decophotocard.title,
        'result_image': decophotocard.result_image,
        'tags' : tags,
        'group' : decophotocard.member.group.name,
        'member' :decophotocard.member.name,
        'hit' : decophotocard.hit,
        'like' : decophotocard.wished_by_users.count(),
    }
    return render(reqeust, 'pocadeco/view.html', context)
