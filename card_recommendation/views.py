from django.shortcuts import render, redirect
from .utils import predict_card_type
from django.http import HttpResponse
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import os
from django.http import JsonResponse
from .models import Card
# 생활 단계 매핑
life_stage_mapping = {
    "UNI": "UNI",
    "NEW_JOB": "NEW_JOB",
    "NEW_WED": "NEW_WED",
    "CHILD_BABY": "CHILD_BABY",
    "CHILD_TEEN": "CHILD_TEEN",
    "CHILD_UNI": "CHILD_UNI",
    "GOLLIFE": "GOLLIFE",
    "SECLIFE": "SECLIFE",
    "RETIR": "RETIR"
}


def create_label_encoder():
    """생활 단계에 대한 라벨 인코더 생성"""
    encoder = LabelEncoder()
    encoder.fit(list(life_stage_mapping.keys()))  # key를 기준으로 인코딩
    return encoder


def credit_card_template(request):
    return render(request, 'credit_card_template.html')

def debit_card_template(request):
    return render(request, 'debit_card_template.html')

def recommendation_view(request):
    if request.method == "POST":
        age = int(request.POST.get('age'))
        app_usage = request.POST.get('appUsage')
        life_stage = request.POST.get('life_stage')

        # Debugging: Check received data
        print(f"Received data: age={age}, app_usage={app_usage}, life_stage={life_stage}")

        life_stage_code = life_stage_mapping.get(life_stage)
        if not life_stage_code:
            return HttpResponse(f"Error: Invalid LIFE_STAGE value: {life_stage}", status=400)

        data = {
            'AGE': age,
            'DIGT_CHNL_REG_YN': 1 if app_usage == 'yes' else 0,
            'LIFE_STAGE': life_stage_code
        }

        try:
            card_type = predict_card_type(data)
        except ValueError as e:
            return HttpResponse(f"Error: {e}", status=400)

        if card_type == "신용카드":
            return redirect('credit_card_template')
        else:
            return redirect('debit_card_template')

    return render(request, 'main.html')

#----------------------------credit card-------------------------------
# views.py

def get_cards_by_category(request):
    category = request.GET.get('category', '')
    if not category:
        return JsonResponse({'error': 'Category is required'}, status=400)

    cards = Card.objects.filter(benefits__contains=category)  # 필터링 로직 확인 필요
    card_list = list(cards.values('name', 'link', 'image_url', 'benefits'))

    return JsonResponse({'cards': card_list})
