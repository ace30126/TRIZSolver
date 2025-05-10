# triz_core.py

# 39가지 기술 특성 (Engineering Parameters)
# 실제로는 39개가 모두 채워져야 합니다. 여기서는 일부만 예시로 넣습니다.
ENGINEERING_PARAMETERS = [
    "1. 이동 물체의 중량 (Weight of moving object)",
    "2. 정지 물체의 중량 (Weight of stationary object)",
    "3. 이동 물체의 길이 (Length of moving object)",
    "4. 정지 물체의 길이 (Length of stationary object)",
    "5. 이동 물체의 면적 (Area of moving object)",
    "6. 정지 물체의 면적 (Area of stationary object)",
    "7. 이동 물체의 부피 (Volume of moving object)",
    "8. 정지 물체의 부피 (Volume of stationary object)",
    "9. 속도 (Speed)",
    "10. 힘 (Force)",
    "11. 응력 또는 압력 (Stress or pressure)",
    "12. 형상 (Shape)",
    "13. 물체의 안정성 (Stability of the object's composition)",
    "14. 강도 (Strength)",
    "15. 이동 물체의 내구성 (Duration of action by a moving object)",
    "16. 정지 물체의 내구성 (Duration of action by a stationary object)",
    "17. 온도 (Temperature)",
    "18. 밝기 (Illumination intensity)",
    "19. 이동 물체가 사용하는 에너지 (Use of energy by moving object)",
    "20. 정지 물체가 사용하는 에너지 (Use of energy by stationary object)",
    "21. 동력 (Power)",
    "22. 에너지 손실 (Loss of energy)",
    "23. 물질 손실 (Loss of substance)",
    "24. 정보 손실 (Loss of information)",
    "25. 시간 손실 (Loss of time)",
    "26. 물질의 양 (Quantity of substance)",
    "27. 신뢰성 (Reliability)",
    "28. 측정 정확도 (Measurement accuracy)",
    "29. 제조 정밀도 (Manufacturing precision)",
    "30. 대상에 작용하는 유해 요인 (Object-affected harmful factors)",
    "31. 대상이 발생시키는 유해 요인 (Object-generated harmful factors)",
    "32. 제조 용이성 (Ease of manufacture)",
    "33. 사용 편의성 (Ease of operation)",
    "34. 수리 용이성 (Ease of repair)",
    "35. 적응성 또는 다용도성 (Adaptability or versatility)",
    "36. 장치의 복잡성 (Device complexity)",
    "37. 제어의 복잡성 (Difficulty of controlling or measuring)",
    "38. 자동화 수준 (Level of automation)",
    "39. 생산성 (Productivity)"
]

# 40가지 발명 원리 (Inventive Principles) - 번호를 키로 사용
INVENTIVE_PRINCIPLES = {
    1: {"name": "분할 (Segmentation)", "description": "시스템을 독립적이거나 분리 가능한 부분으로 나눈다. 쉽게 분해/조립 가능하게 한다."},
    2: {"name": "추출 (Taking Out/Extraction)", "description": "시스템에서 '방해되는' 부분이나 성질만 분리하거나, '필요한' 부분이나 성질만 골라낸다."},
    3: {"name": "국부적 품질 (Local Quality)", "description": "시스템이나 환경의 각 부분이 서로 다른 조건에서 작동하도록 한다. 각 부분의 기능을 최적화한다."},
    4: {"name": "비대칭 (Asymmetry)", "description": "대칭적인 형태를 비대칭으로 바꾼다. 비대칭성이 이미 있다면 더욱 강화한다."},
    5: {"name": "통합 (Merging/Consolidation)", "description": "동일하거나 유사한 대상, 또는 연관된 작업을 공간적/시간적으로 통합한다."},
    6: {"name": "다용도 (Universality)", "description": "하나의 대상이 여러 기능을 수행하게 하여 다른 대상의 필요성을 줄인다."},
    7: {"name": "포개기 (Nesting/Matryoshka)", "description": "하나의 대상을 다른 대상 안에 넣고, 다시 그것을 또 다른 대상 안에 넣는다."},
    8: {"name": "무게 보상 (Anti-weight/Counterweight)", "description": "대상의 무게를 줄이기 위해, 부력을 이용하거나 다른 물체와 결합하여 무게를 상쇄한다."},
    9: {"name": "선행 반대 조치 (Preliminary Anti-action/Prior Counteraction)", "description": "유해한 작용이 예상될 경우, 사전에 반대 작용을 가하여 이를 상쇄한다."},
    10: {"name": "선행 조치 (Preliminary Action/Prior Action)", "description": "필요한 변화를 사전에 전부 또는 부분적으로 수행한다. 대상을 가장 편리한 위치에 미리 배치한다."},
    11: {"name": "사전 방비 (Beforehand Cushioning/Prior Grounding)", "description": "비교적 낮은 신뢰도를 가진 대상에 대해, 사전에 비상 수단을 준비한다."},
    12: {"name": "등전위화 (Equipotentiality/Remove tension)", "description": "작업 환경에서 위치 에너지의 변화를 줄이거나 없앤다 (예: 물건을 들어올리거나 내리는 것을 최소화)."},
    13: {"name": "반대로 하기 (The Other Way Around/Inversion)", "description": "문제 해결을 위해 기존의 작용을 반대로 한다. 움직이는 부분을 고정하고, 고정된 부분을 움직이게 한다."},
    14: {"name": "구형화 (Spheroidality/Curvature)", "description": "직선적인 부분을 곡선으로, 평면을 구면으로 바꾼다. 롤러, 볼, 나선 등을 사용한다."},
    15: {"name": "동적 특성 (Dynamics/Dynamicity)", "description": "대상의 특성이나 외부 환경이 각 작동 단계에서 최적이 되도록 유동적으로 변화시킨다."},
    16: {"name": "부족 또는 초과 조치 (Partial or Excessive Action/Slightly Less or Slightly More)", "description": "100% 원하는 결과를 얻기 어렵다면, 약간 덜하거나 약간 더 많이 수행하여 문제를 단순화한다."},
    17: {"name": "차원 변경 (Another Dimension/Move to a new dimension)", "description": "문제를 1차원에서 2차원으로, 2차원에서 3차원으로 옮긴다. 다층 구조를 사용한다."},
    18: {"name": "기계적 진동 (Mechanical Vibration)", "description": "대상을 진동시킨다. 초음파를 사용한다. 공명 주파수를 활용한다."},
    19: {"name": "주기적 작용 (Periodic Action)", "description": "연속적인 작용을 주기적인 작용(펄스)으로 바꾼다. 작용의 주파수를 바꾼다."},
    20: {"name": "유용한 작용의 지속 (Continuity of Useful Action)", "description": "작업의 모든 부분이 중단 없이 지속적으로 유용하게 작동하도록 한다."},
    21: {"name": "고속 통과 (Skipping/Rushing Through)", "description": "유해하거나 위험한 공정을 매우 빠른 속도로 진행하여 부정적 영향을 최소화한다."},
    22: {"name": "전화위복 (Blessing in Disguise/Convert Harm into Benefit)", "description": "유해한 요인이나 환경을 이용하여 유익한 효과를 얻거나, 유해한 작용을 상쇄한다."},
    23: {"name": "피드백 (Feedback)", "description": "결과나 과정에 대한 정보를 도입하여 작용에 영향을 준다."},
    24: {"name": "매개체 (Intermediary/Mediator)", "description": "중간 매개체를 사용하여 작용을 전달하거나 수행한다."},
    25: {"name": "셀프서비스 (Self-service)", "description": "대상이 스스로 기능을 수행하거나 보조 기능을 수행하도록 하고, 스스로 수리하도록 한다."},
    26: {"name": "복제 (Copying)", "description": "복잡하거나 비싸거나 깨지기 쉬운 대상 대신에 간단하고 저렴한 복제품을 사용한다."},
    27: {"name": "값싼 일회용품 (Cheap Short-living Objects)", "description": "비싼 대상 대신에 여러 개의 값싼 일회용품으로 대체하여 특정 속성(예: 수명)을 절충한다."},
    28: {"name": "기계 시스템 대체 (Mechanical System Replacement/Another sense)", "description": "기계적 시스템을 광학, 음향, 열, 냄새 등으로 대체한다."},
    29: {"name": "유체 활용 (Pneumatics and Hydraulics)", "description": "고체 부품 대신 기체나 액체(공기, 물 등)를 사용한다."},
    30: {"name": "유연한 막 또는 얇은 필름 (Flexible Shells and Thin Films)", "description": "기존 구조물 대신 유연한 막이나 얇은 필름을 사용한다. 외부와 격리시킨다."},
    31: {"name": "다공성 물질 (Porous Materials)", "description": "물체를 다공성으로 만들거나 다공성 요소를 추가한다."},
    32: {"name": "색상 변경 (Color Changes)", "description": "물체나 주변 환경의 색상을 변경한다. 투명도를 변경한다."},
    33: {"name": "동질성 (Homogeneity)", "description": "주요 대상과 상호작용하는 대상을 동일한 재료로 만든다."},
    34: {"name": "폐기 및 재생 (Discarding and Recovering/Rejection and Regeneration)", "description": "기능을 다한 부분을 폐기하거나(용해, 증발 등) 작동 중에 직접 복원한다."},
    35: {"name": "물리화학적 특성 변화 (Parameter Changes/Transformation of Properties)", "description": "물체의 물리적 상태(고체, 액체, 기체), 농도, 유연성, 온도 등을 변경한다."},
    36: {"name": "상 변화 (Phase Transitions)", "description": "상 변화(예: 부피 변화, 열 발생/흡수) 시 발생하는 현상을 이용한다."},
    37: {"name": "열 팽창 (Thermal Expansion)", "description": "재료의 열 팽창(또는 수축)을 이용한다."},
    38: {"name": "강산화제 (Strong Oxidants/Enriched atmosphere)", "description": "산소 농도를 높이거나, 산화력이 강한 물질로 대체한다."},
    39: {"name": "불활성 환경 (Inert Atmosphere)", "description": "작업 환경을 일반 환경에서 불활성 환경으로 바꾼다."},
    40: {"name": "복합 재료 (Composite Materials)", "description": "단일 재료에서 복합 재료로 변경한다."}
}

# 모순 매트릭스 (Contradiction Matrix)
# 39x39 크기의 2차원 리스트. 각 요소는 발명 원리 번호들의 리스트.
# 예시: CONTRADICTION_MATRIX[개선특성인덱스][악화특성인덱스] = [원리1, 원리2, ...]
# 여기서는 데이터가 매우 방대하므로, 구조만 보여드리고 실제 데이터는 외부 파일(CSV 등)에서 로드하는 것을 권장합니다.
# 아래는 극히 일부의 예시 데이터입니다. (실제로는 39x39를 모두 채워야 함)
# 개선: 1. 이동 물체의 중량 / 악화: 9. 속도 => 추천 원리들
# 개선: 1. 이동 물체의 중량 / 악화: 14. 강도 => 추천 원리들

# 실제로는 이 매트릭스를 모두 채워야 합니다.
# 예시: (0,0) (0,1) ... (0,38)
#       (1,0) (1,1) ... (1,38)
#       ...
#       (38,0) (38,1) ... (38,38)
# 각 셀에는 [원리번호1, 원리번호2, ...] 형태의 리스트가 들어감.
# 빈 리스트는 해당 모순에 대해 고전적 TRIZ 매트릭스에서 제안하는 원리가 없음을 의미할 수 있음.

CONTRADICTION_MATRIX = [
    # 예시: 첫 번째 줄 (개선 특성: 1. 이동 물체의 중량)
    [ [], [10,29,35], [15,29,35], [], [], [], [], [], [10,18,28,34], [], # 악화 1~10
      [], [], [], [1,26,27,40], [], [], [], [], [], [], # 악화 11~20
      [], [], [], [], [], [], [], [], [], [], # 악화 21~30
      [], [], [], [], [], [], [], [], []      # 악화 31~39
    ],
    # 예시: 두 번째 줄 (개선 특성: 2. 정지 물체의 중량)
    [ [10,29,35], [], [], [15,29,35], [], [], [], [], [10,18,28,34], [], # 악화 1~10
      [], [], [], [1,26,27,40], [], [], [], [], [], [], # 악화 11~20
      # ... 이하 생략 (실제 데이터로 채워야 함)
    ],
    # ... 나머지 37개 줄도 모두 채워야 함 (총 39개 줄)
]
# 실제 사용 시에는 이 CONTRADICTION_MATRIX를 완성하거나, CSV 파일 등에서 로드해야 합니다.
# 예시 CSV 파일 로드:
# import csv
# def load_matrix_from_csv(filename="triz_matrix.csv"):
#     matrix = []
#     with open(filename, 'r', encoding='utf-8') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             matrix_row = []
#             for cell in row:
#                 if cell.strip(): # 셀이 비어있지 않으면
#                     # 원리 번호들이 쉼표나 공백으로 구분되어 있다고 가정
#                     principle_ids = [int(p.strip()) for p in cell.split(',')]
#                     matrix_row.append(principle_ids)
#                 else:
#                     matrix_row.append([]) # 빈 셀은 빈 리스트
#             matrix.append(matrix_row)
#     return matrix
# CONTRADICTION_MATRIX = load_matrix_from_csv() # 실제 파일이 있을 경우 이렇게 로드


def get_engineering_parameters():
    """39가지 기술 특성 리스트를 반환합니다."""
    return ENGINEERING_PARAMETERS

def get_inventive_principles():
    """40가지 발명 원리 딕셔너리를 반환합니다."""
    return INVENTIVE_PRINCIPLES

def get_principle_details(principle_id):
    """주어진 ID의 발명 원리 상세 정보를 반환합니다."""
    return INVENTIVE_PRINCIPLES.get(principle_id)

def get_principles_from_contradiction(improving_param_index, worsening_param_index):
    """
    모순 매트릭스에서 개선 특성과 악화 특성에 해당하는 발명 원리 번호 리스트를 반환합니다.
    매트릭스 인덱스는 0부터 시작합니다.
    """
    if not (0 <= improving_param_index < len(CONTRADICTION_MATRIX) and \
            0 <= worsening_param_index < len(CONTRADICTION_MATRIX[0])): # 매트릭스 범위 확인
        return [] # 인덱스 벗어나면 빈 리스트

    # CONTRADICTION_MATRIX가 완성되어 있다고 가정
    # 실제로는 위에서 정의한 CONTRADICTION_MATRIX가 일부만 채워져 있으므로,
    # 이 함수를 제대로 테스트하려면 매트릭스 데이터가 완전해야 합니다.
    # 또는, 테스트를 위해 몇몇 특정 셀에만 데이터를 넣어두고 해당 인덱스로 테스트할 수 있습니다.
    
    # 임시로, 매트릭스가 비어있을 경우를 대비 (실제로는 데이터가 있어야 함)
    if not CONTRADICTION_MATRIX or \
       improving_param_index >= len(CONTRADICTION_MATRIX) or \
       worsening_param_index >= len(CONTRADICTION_MATRIX[improving_param_index]):
        print(f"경고: 모순 매트릭스 데이터가 부족하거나 인덱스 접근 오류 ({improving_param_index}, {worsening_param_index})")
        return []
        
    principle_ids = CONTRADICTION_MATRIX[improving_param_index][worsening_param_index]
    return principle_ids

if __name__ == '__main__':
    # 테스트용 코드
    print("--- 기술 특성 ---")
    params = get_engineering_parameters()
    for i, p in enumerate(params):
        if i < 5: # 처음 5개만 출력
            print(f"{i}: {p}")

    print("\n--- 발명 원리 (예시) ---")
    principles = get_inventive_principles()
    for i in range(1, 6): # 처음 5개 원리만 출력
        details = get_principle_details(i)
        print(f"원리 {i}: {details['name']} - {details['description'][:30]}...")

    print("\n--- 모순 해결 원리 조회 (예시) ---")
    # 예시: 개선(이동 물체의 중량, 인덱스 0) vs 악화(속도, 인덱스 8)
    # CONTRADICTION_MATRIX[0][8]에 [10,18,28,34] 가 있다면 해당 원리들이 출력되어야 함
    # 단, 위 CONTRADICTION_MATRIX 예시 데이터가 이 값을 포함하도록 수정해야 테스트 가능
    # 현재 예시 CONTRADICTION_MATRIX[0][8] = [10,18,28,34] 로 설정되어 있음.
    
    improving_idx = 0 # 예: 1. 이동 물체의 중량
    worsening_idx = 8 # 예: 9. 속도
    
    # 만약 CONTRADICTION_MATRIX가 비어있거나 일부만 채워져 있다면, 아래 코드가 정상 작동하지 않을 수 있습니다.
    # 테스트를 위해 CONTRADICTION_MATRIX[0][8]에 값을 넣어두겠습니다.
    if len(CONTRADICTION_MATRIX) > improving_idx and len(CONTRADICTION_MATRIX[improving_idx]) > worsening_idx:
         CONTRADICTION_MATRIX[improving_idx][worsening_idx] = [10, 18, 28, 34] # 테스트용 데이터 삽입
    else: # 매트릭스 크기가 작아서 해당 셀이 없는 경우 (예시 매트릭스가 축소되었으므로)
        print(f"주의: 예시 CONTRADICTION_MATRIX가 작아서 ({improving_idx},{worsening_idx}) 테스트 데이터를 설정할 수 없습니다.")


    print(f"개선: {ENGINEERING_PARAMETERS[improving_idx]}")
    print(f"악화: {ENGINEERING_PARAMETERS[worsening_idx]}")
    suggested_ids = get_principles_from_contradiction(improving_idx, worsening_idx)
    
    if suggested_ids:
        print("추천 발명 원리:")
        for pid in suggested_ids:
            p_details = get_principle_details(pid)
            if p_details:
                print(f"  - {pid}. {p_details['name']}")
            else:
                print(f"  - 원리 {pid} (정보 없음)")
    else:
        print("추천 발명 원리를 찾을 수 없거나, 매트릭스 데이터가 없습니다.")