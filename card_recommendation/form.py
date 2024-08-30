from django import forms

class RecommendationForm(forms.Form):
    age = forms.IntegerField(label='나이', min_value=20, max_value=89)
    digital_channel = forms.ChoiceField(
        label='은행 어플 사용 여부',
        choices=[('사용', '사용'), ('미사용', '미사용')]
    )
    life_stage = forms.ChoiceField(
        label='라이프 스테이지',
        choices=[
            ('대학생', '대학생'),
            ('사회초년생', '사회초년생'),
            ('신혼', '신혼'),
            ('자녀 영유아', '자녀 영유아'),
            ('자녀 의무교육', '자녀 의무교육'),
            ('자녀 대학생', '자녀 대학생'),
            ('중년 (자녀 없음)', '중년 (자녀 없음)'),
            ('중년 (자녀 있음)', '중년 (자녀 있음)'),
            ('은퇴', '은퇴')
        ]
    )
