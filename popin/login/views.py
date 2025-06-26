from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from signupFT.models import User
from django.core.mail import send_mail
from django.http import JsonResponse 
from django.conf import settings
import random
# 이메일 인증번호 전송 
def send_verification_code(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        try:
            user = User.objects.get(email=email, name=name)
            code = str(random.randint(100000, 999999))
            request.session['verify_code'] = code
            request.session['verify_user'] = user.user_id

            send_mail(
                subject='[PO-PIN] 이메일 인증번호',
                message=f'인증번호는 다음과 같습니다: {code}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '회원 정보가 일치하지 않습니다.'})
# 로그인
def loginp(request):
    if request.method == 'POST':
        user_id = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(user_id=user_id)
            if check_password(password, user.password):
                request.session['user_id'] = user.user_id
                return redirect('home:main')  # 홈 또는 메인 페이지
            else:
                messages.error(request, "비밀번호가 일치하지 않습니다.")
        except User.DoesNotExist:
            messages.error(request, "존재하지 않는 아이디입니다.")

    return render(request, 'login.html')


# 아이디 찾기
def loginID(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        try:
            user = User.objects.get(name=name, email=email)
            return render(request, "login-findID.html", {'found_id': user.user_id})
        except User.DoesNotExist:
            messages.error(request, '일치하는 회원이 없습니다.')
    return render(request, "login-findID.html")


# 비밀번호 찾기 (세션에 user_id 저장)

def loginPW(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        email = request.POST.get('email')
        try:
            user = User.objects.get(user_id=user_id, email=email)
            # 세션에 유저 저장
            request.session['reset_user_id'] = user.user_id

            reset_link = request.build_absolute_uri('/login/loginCPW/')
            send_mail(
                subject='[PO-PIN] 비밀번호 재설정 링크',
                message=f'다음 링크를 클릭하여 비밀번호를 재설정하세요:\n{reset_link}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, '비밀번호 재설정 링크를 이메일로 전송했습니다.')
        except User.DoesNotExist:
            messages.error(request, '일치하는 회원이 없습니다.')
    return render(request, "login-findPW.html")


# 비밀번호 재설정
def loginCPW(request):
    if request.method == 'POST':
        pw1 = request.POST.get('pw1')
        pw2 = request.POST.get('pw2')

        if pw1 != pw2:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, "login-changePW.html")

        user_id = request.session.get('reset_user_id')
        if not user_id:
            messages.error(request, '비밀번호 재설정 대상이 없습니다. 다시 시도해주세요.')
            return redirect('login:loginp')

        try:
            user = User.objects.get(user_id=user_id)
            user.password = make_password(pw1)
            user.save()
            del request.session['reset_user_id']  # ✅ 재설정 후 세션 삭제
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다.')
            return redirect('login:loginp')
        except User.DoesNotExist:
            messages.error(request, '해당 사용자를 찾을 수 없습니다.')

    return render(request, "login-changePW.html")