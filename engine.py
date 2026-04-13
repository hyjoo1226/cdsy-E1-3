# 패턴과 필터의 mac(곱셈-누적 연산)
def calculate_mac(pattern, filter_matrix):
    score = 0.0
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            score += pattern[i][j] * filter_matrix[i][j]
    return score

# mac 점수 비교 후 판정 결과 반환
def compare_scores(score_a, score_b):
    # 허용 오차 설정 (1e-9: 0.000000001)
    EPSILON = 1e-9

    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"