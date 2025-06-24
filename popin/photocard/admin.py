from django.contrib import admin
from photocard.models import TempIdol
from photocard.models import TempUser
from photocard.models import Photocard

# Register your models here.

admin.site.register(TempIdol)
admin.site.register(TempUser)
admin.site.register(Photocard)