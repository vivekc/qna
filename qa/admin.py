from django.contrib import admin

# Register your models here.
from .models import Question, Answer, QaUser, Tenant

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QaUser)
admin.site.register(Tenant)
