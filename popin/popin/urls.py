from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('mypage/', include('mypage.urls')),
    path('photocard/', include('photocard.urls')),
    path('signup/', include('signupFT.urls')),
    path('idols/', include('idols.urls')),
]

# 파일업로드시 url구성 , urlpatterns 에 추가로 설정이 들어감.
urlpatterns += static(settings.MEDIA_URL, 
                      document_root=settings.MEDIA_ROOT)
