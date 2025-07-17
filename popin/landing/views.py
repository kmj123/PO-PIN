from django.shortcuts import render, redirect
from photocard.models import Photocard

from django.db.models import Count

def landing(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션
    
    if user_id:
        return redirect('home/main')
    
    photocards = Photocard.objects.select_related('member__group').annotate(
        wish_count=Count('wished_by_users')).order_by('-wish_count')[:4]
    context = {"photocards":photocards}
    return render(request, 'landing.html', context)