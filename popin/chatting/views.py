from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from .models import ChatMessage, ChatRoom
from photocard.models import Photocard

from signupFT.models import User


# Create your views here.

def chatting(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')  # 로그인 안 되어있으면 로그인 페이지로

    try:
        user = User.objects.get(user_id=user_id) # 로그인한 사용자
        rooms = ChatRoom.objects.filter(host_user=user) | ChatRoom.objects.filter(guest_user=user)
        rooms = rooms.distinct().order_by('-last_timestamp')  # 최근 채팅 순 정렬
        room = rooms.first()
        messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
        
        print(rooms)
        context = {
            'rooms':rooms,
            "messages": messages,
        }
        return render(request, 'chatting/chatting.html', context)        
    
    except User.DoesNotExist:
        return redirect('login:main')  # 예외 상황 대비

# def room(request, room_name):
#     messages = ChatMessage.objects.filter(room_name=room_name).order_by('timestamp')
#     print("=====================")
#     print(room_name)
#     print(messages)
#     print("=====================")
#     context = {
#         "room_name": room_name,
#         "messages": messages,
#     }
#     return render(request, "chatting/chatting.html", context)

def test(request):
    return render(request, 'chatting/test.html')

def start_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST만 허용됩니다.'}, status=405)
    
    try:
        body = json.loads(request.body)
        category = body.get('category')
        post_id = body.get('post_id')
        
        print(category, post_id)
        
        user_id = request.session.get('user_id')  # 현재 로그인한 사용자
        if category == "exchange" or category == "sale":
            try:
                guest_user = User.objects.get(user_id=user_id)
                post = Photocard.objects.get(pno=post_id)
                post.buyer = guest_user
                post.save()
                
                room, created = ChatRoom.objects.get_or_create(
                    category="category",
                    post_id=post.pno,
                    host_user=post.seller,
                    guest_user=post.buyer,
                )
                
                return JsonResponse({'success': True, 'created':created, 'room_id': room.id})
                
            except User.DoesNotExist:
                return redirect('home:main')  # 예외 상황 대비
            
            except Exception as e:  
                print(e)
                return JsonResponse({'error': str(e)}, status=500)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)