
from django.shortcuts import render,redirect
from signupFT.models import User

def main(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        user = User.objects.get(user_id=user_id)
        context = {
            'username': user.name,  # 또는 user.nickname, user.user_id 등 원하는 필드
        }
        return render(request, 'main.html', context)
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비