from django.urls import path
from . import views
from .views import get_cards_by_category


urlpatterns = [
    path('main/', views.recommendation_view, name='recommendation_view'),  # 폼 입력 페이지
    path('credit-card/', views.credit_card_template, name='credit_card_template'),   # 신용카드 추천 결과 페이지
    path('debit-card/', views.debit_card_template, name='debit_card_template'),      # 체크카드 추천 결과 페이지
    path('api/cards/', get_cards_by_category, name='get_cards_by_category'),
]
