from django.shortcuts import render

from signupFT.models import User
from photocard.models import Photocard
from idols.models import Member
from photocard.models import TempWish
from pocadeco.models import DecoratedPhotocard

from django.db.models import Count
from datetime import date

# 데코포토 전체 리스트
def decoMain(request):
    # 전체 데코포토 리스트 불러오기
    decoratedpoca = DecoratedPhotocard.objects.select_related('member__group').order_by('-created_at').annotate(
    wish_count=Count('wished_by_users')
)
    
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
    # 최신글 순 정렬 옵션 적용
    if sort == 'created_at':
        decoratedpoca = decoratedpoca.annotate('created_at')
    # 좋아요 순 정렬 옵션 적용
    if sort == 'likes':
        decoratedpoca = decoratedpoca.annotate(wish_count=Count('wished_by_users')).order_by('-wish_count')
    # 조회수 정렬 옵션 적용
    elif sort == 'hit':
        decoratedpoca = decoratedpoca.order_by('-hit')
        
    deco_list = []
    for poca in decoratedpoca:
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
        print(deco_list)

    
    context = {'decoList': deco_list}
    return render(request,'pocadeco/decoMain.html', context)

def main(request):
    return render(request, 'pocadeco/main.html')
def mydecolist(request):
    return render(request, 'pocadeco/mydecolist.html')

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
