import time

# 허용 오차 설정 (1e-9: 0.000000001)
EPSILON = 1e-9

# 패턴과 필터의 mac(곱셈-누적 연산)
def calculate_mac(pattern, filter_matrix):
    score = 0.0
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            score += pattern[i][j] * filter_matrix[i][j]
    return score

# mac 점수 비교 후 판정 결과 반환
def compare_scores(score_a, score_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"

# mac 연산의 평균 실행 시간 계산    
def get_average_mac_time(pattern, filter_matrix_a, filter_matrix_b, iterations=5):
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        calculate_mac(pattern, filter_matrix_a)
        calculate_mac(pattern, filter_matrix_b)
        
    end_time = time.perf_counter()
    
    # 평균 시간: 전체 걸린 시간 / 반복 횟수 * 1000 (초 단위를 ms로 변환)
    # 필터 A, B 각각 5회씩 총 10회 연산 평균 측정
    avg_time_ms = ((end_time - start_time) / (iterations * 2)) * 1000
    return avg_time_ms

# JSON의 'expected' 값을 표준 라벨로 정규화
def normalize_label(expected_raw):
    label = str(expected_raw).strip().lower()
    
    # 십자가
    if label in ['cross', '+', 'Cross']:
        return "Cross"
    # X
    elif label in ['x', 'X']:
        return "X"  
    return "UNDECIDED"