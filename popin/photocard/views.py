from django.shortcuts import render
from photocard.models import Photocard
from django.db.models import Count

# Create your views here.

def list(request):
    qs = Photocard.objects.annotate(
        wish_count=Count('wished_by_users')
    ).values('pno', 'category', 'album', 'trade_type', 'place', 'wish_count', 'image','idol__group', 'idol__member')

    context = {'list': qs}
    return render(request, 'list.html', context)