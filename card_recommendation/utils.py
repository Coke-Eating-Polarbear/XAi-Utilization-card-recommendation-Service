import os
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from django.conf import settings
# 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = r'C:\Users\audwn\wooriFisa\seminar2\myseminar\models\random_forest_model4.joblib'
scaler_path = r'C:\Users\audwn\wooriFisa\seminar2\myseminar\models\scaler1.joblib'

print("Current working directory:", os.getcwd())
print("Expected model path:", os.path.join(os.getcwd(), 'models', 'random_forest_model4.joblib'))

# 범위별 나이 매핑
age_range_mapping = {
    (20, 24): 20, (25, 29): 25, (30, 34): 30, (35, 39): 35, 
    (40, 44): 40, (45, 49): 45, (50, 54): 50, (55, 59): 55, 
    (60, 64): 60, (65, 69): 65, (70, 74): 70, (75, 79): 75, 
    (80, 84): 80, (85, 89): 85
}

def map_age(age):
    """입력된 나이를 범위의 대표값으로 매핑"""
    for age_range, representative_age in age_range_mapping.items():
        if age_range[0] <= age <= age_range[1]:
            return representative_age
    return None  # 범위에 맞지 않는 경우 None 반환

# Life_stage를 라벨 인코더
def create_label_encoder():
    encoder = LabelEncoder()
    encoder.fit(["UNI", "NEW_JOB", "NEW_WED", "CHILD_BABY", "CHILD_TEEN", "CHILD_UNI", "GOLLIFE", "SECLIFE", "RETIR"])
    return encoder

# 입력받은 데이터를 모델에 넣어 해당 데이터를 가진 사람들은 주로 신용카드를 쓰는지 체크카드를 쓰는지 확인
def predict_card_type(data):
    model_path = settings.MODEL_PATH
    scaler_path = settings.SCALER_PATH
    print("Model path exists:", os.path.exists(settings.MODEL_PATH))
    print("Scaler path exists:", os.path.exists(settings.SCALER_PATH))
    # 모델과 스케일러 로드
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    encoder = create_label_encoder()
    
    
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

    life_stage_code = life_stage_mapping.get(data['LIFE_STAGE'])
    if not life_stage_code:
        raise ValueError(f"Invalid LIFE_STAGE value: {data['LIFE_STAGE']}")

    input_data = pd.DataFrame({
        'AGE': [data['AGE']],
        'DIGT_CHNL_REG_YN': [data['DIGT_CHNL_REG_YN']],
        'LIFE_STAGE': [life_stage_code]
    })

    # Check the classes known to the encoder
    print(f"Encoder classes: {encoder.classes_}")
    
    if life_stage_code not in encoder.classes_:
        raise ValueError(f"Life stage code {life_stage_code} not found in encoder classes")

    input_data['LIFE_STAGE'] = encoder.transform(input_data['LIFE_STAGE'])
    input_scaled = scaler.transform(input_data)
    predicted_card_type = model.predict(input_scaled)[0]
    
    return "신용카드" if predicted_card_type == 0 else "체크카드"
