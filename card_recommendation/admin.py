# card_recommendation/admin.py

from django.contrib import admin
from .models import Card

class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_url', 'link', 'benefits', 'details')  # categories를 제거하거나 올바른 필드명으로 수정

admin.site.register(Card, CardAdmin)
