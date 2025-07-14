from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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
        first_room = rooms.first()
        messages = ChatMessage.objects.filter(room=first_room).order_by('timestamp')
        
        room_list = []
        for room in rooms:
            read_count = ChatMessage.objects.filter(room=room, is_read=False).order_by('timestamp').count
            if user.nickname == room.host_user.nickname:
                nickname = room.guest_user.nickname
            else:
                nickname = room.host_user.nickname
            
            room_list.append({
                'id':room.id,
                'nickname': nickname,
                'last_timestamp':room.last_timestamp,
                'last_message' : room.last_message,
                'read_count' : read_count,
            })

        context = {
            'rooms':room_list,
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
        
        print(category, post_id, flush=True)
        
        user_id = request.session.get('user_id')  # 현재 로그인한 사용자
        if category == "exchange" or category == "sale":
            try:
                guest_user = User.objects.get(user_id=user_id)
                post = Photocard.objects.get(pno=post_id)
                post.buyer = guest_user
                post.buy_state ="중"
                post.save()
                
                room, created = ChatRoom.objects.get_or_create(
                    category=category,
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
    
def fetch_messages(request, room_id):
    if not request.session.get("user_id"):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    data = []
    for msg in messages:
        msg.is_read = True
        msg.save()
        data.append({
            'user_id': msg.send_user.user_id,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime("%p %I:%M")
                        .replace("AM", "오전")
                        .replace("PM", "오후")
        })
        
    print(data);
    return JsonResponse({'messages': data})