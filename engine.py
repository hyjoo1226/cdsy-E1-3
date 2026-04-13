# 패턴과 필터의 mac(곱셈-누적 연산)
def calculate_mac(pattern, filter_matrix):
    score = 0.0
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            score += pattern[i][j] * filter_matrix[i][j]
    return score