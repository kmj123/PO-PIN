from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import json
from django.utils import timezone

from .models import ChatMessage, ChatRoom
from photocard.models import Photocard
from signupFT.models import User
from community.models import ProxyPost, CompanionPost  # 상단에 import

def chatting(request):
    user_id = request.session.get('user_id')  # 로그인 시 저장한 user_id 세션

    if not user_id:
        return redirect('login:loginp')

    try:
        user = User.objects.get(user_id=user_id)
        post_id = request.GET.get('post_id')
        post_type = request.GET.get('post_type')  # 동행인지 대리인지 구분하려고 추가

        selected_room = None
        messages = []
        post_info = None

        if post_id:
            try:
                if post_type == "companion":
                    post = CompanionPost.objects.get(id=post_id)
                else:
                    post = ProxyPost.objects.get(id=post_id)

                post_author = post.author

                existing_room = ChatRoom.objects.filter(
                    host_user=user, guest_user=post_author
                ).first() or ChatRoom.objects.filter(
                    host_user=post_author, guest_user=user
                ).first()

                if existing_room:
                    selected_room = existing_room
                else:
                    selected_room = ChatRoom.objects.create(
                        host_user=user,
                        guest_user=post_author,
                    )

                messages = ChatMessage.objects.filter(room=selected_room).order_by('timestamp')

                post_info = {
                    'id': post.id,
                    'title': post.title,
                    'artist': post.artist,
                    'location': getattr(post, 'location', ''),  # 나눔은 location 없을 수도
                    'reward': getattr(post, 'reward', ''),  # 동행은 reward 없음
                    'status': post.status,
                }

            except (ProxyPost.DoesNotExist, CompanionPost.DoesNotExist):
                selected_room = None
                messages = []

        rooms = ChatRoom.objects.filter(host_user=user) | ChatRoom.objects.filter(guest_user=user)
        rooms = rooms.distinct().order_by('-last_timestamp')

        if not selected_room:
            first_room = rooms.first()
            if first_room:
                messages = ChatMessage.objects.filter(room=first_room).order_by('timestamp')

        room_list = []
        for room in rooms:
            read_count = ChatMessage.objects.filter(
                room=room,
                is_read=False
            ).exclude(send_user=user).count()

            nickname = room.guest_user.nickname if user.nickname == room.host_user.nickname else room.host_user.nickname

            room_list.append({
                'id': room.id,
                'nickname': nickname,
                'last_timestamp': room.last_timestamp,
                'last_message': room.last_message,
                'read_count': read_count,
            })

        context = {
            'rooms': room_list,
            'messages': messages,
            'selected_room_id': selected_room.id if selected_room else (rooms.first().id if rooms.first() else None),
            'post_info': post_info,
        }

        return render(request, 'chatting/chatting.html', context)

    except User.DoesNotExist:
        return redirect('login:main')

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
                    defaults={
                        'last_timestamp':now(),
                        'last_message' : "채팅을 시작해 보세요",
                    }
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
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    try:
        room = ChatRoom.objects.get(id=room_id)
    except ChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

    messages = ChatMessage.objects.filter(room=room).order_by('timestamp')
    data = []
    for msg in messages:
        if user_id != msg.send_user.user_id:
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