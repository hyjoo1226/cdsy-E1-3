from engine import calculate_mac, compare_scores, get_average_mac_time, EPSILON
from io_handler import get_matrix_input

# 모드 1: 사용자 입력 모드
def run_user_input_mode():
    print("-" * 30)
    print("[1] 필터 입력")
    print("-" * 30)

    # 입력
    filter_a = get_matrix_input("필터 A", 3)
    filter_b = get_matrix_input("필터 B", 3)
    print("-" * 30)
    print("[2] 패턴 입력")
    print("-" * 30)
    pattern = get_matrix_input("패턴", 3)
    
    # 연산
    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)
    
    # 판정
    result = compare_scores(score_a, score_b)

    # 시간 측정
    avg_time = get_average_mac_time(pattern, filter_a, filter_b)

    # 결과 출력
    print("\n" + "-"*30)
    print("# [3] MAC 결과")
    print("-"*30)
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time:.3f} ms")

    if result == "UNDECIDED":
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print(f"판정: {result}")

def main():
    print("=== Mini NPU Simulator ===")
    print("\n모드 선택:")
    print("\n1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    print("3. 종료")

    mode = input("선택: ")

    if mode == "1":
        run_user_input_mode()
    elif mode == "2":
        # data.json 분석
        pass
    elif mode == "3":
        print("프로그램을 종료합니다.")

if __name__ == "__main__":
    main()