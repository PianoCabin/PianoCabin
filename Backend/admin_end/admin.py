from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PianoRoom)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(LongTermOrder)
admin.site.register(News)
admin.site.register(Feedback)