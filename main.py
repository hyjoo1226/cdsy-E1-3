from engine import calculate_mac
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
    
    # 2. 연산 (engine 담당)
    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)
    
    # 3. 판정 및 출력
    result = compare_scores(score_a, score_b)
    print_result(score_a, score_b, result)

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
    
    # MAC 계산
    score = calculate_mac(pattern, filter_matrix)
    
    print(f"MAC Score: {score}")

if __name__ == "__main__":
    main()