import json
from engine import calculate_mac, compare_scores, get_average_mac_time, normalize_label, EPSILON
from io_handler import get_matrix_input, get_int_input

# 메인 메뉴
def choice_menu():
    while True:
        print("=== Mini NPU Simulator ===")
        print("\n모드 선택:")
        print("\n1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("3. 종료")

        mode = get_int_input("선택: ", 1, 3)

        if mode == 1:
            run_user_input_mode()
        elif mode == 2:
            run_data_analysis_mode()
        elif mode == 3:
            print("프로그램을 종료합니다.")
            break

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

# 모드 2: data.json 분석 모드
def run_data_analysis_mode():
    # 파일 읽기, 예외 처리
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data.json 파일을 찾을 수 없습니다.")
        return
    except json.JSONDecodeError:
        print("data.json 파일의 형식이 잘못되었습니다.")
        return
    
    
    filters = data["filters"]
    patterns = data["patterns"]

    print("-" * 30)
    print("[1] 필터 로드")
    print("-" * 30)
    for size_key in filters.keys():
        print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")

    total_count = len(patterns)
    passed_count = 0
    failed_cases = []
    time_stats = {}

    if total_count == 0:
        print("data.json에 분석할 패턴 데이터가 없습니다.")
        return
    
    correct_count = 0

    print("\n" + "-" * 30)
    print("[2] 패턴 분석")
    print("-" * 30)
    
    # 데이터 순회 및 연산
    for key, value in patterns.items():
        print(f"--- {key} ---")

        # 사이즈 추출
        size_str = key.split('_')[1]
        filter_key = f"size_{size_str}" # "size_5" 형태
        
        filter_cross = filters[filter_key]["cross"]
        filter_x = filters[filter_key]["x"]
        
        pattern_input = value["input"]
        
        # 연산
        score_cross = calculate_mac(pattern_input, filter_cross)
        score_x = calculate_mac(pattern_input, filter_x)

        # 판정
        result = compare_scores(score_cross, score_x)
        
        # 결과 비교
        if result == "A":
            result = "Cross"
        elif result == "B":
            result = "X"
        else:
            result = "UNDECIDED"

        expected = normalize_label(value["expected"])   # 정규화

        if result == expected:
            status = "PASS"
            correct_count += 1
        else:
            status = "FAIL"
            if result == "UNDECIDED":
                reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
            else:
                reason = "불일치"
            failed_cases.append((key, reason))


        # 시간 측정
        avg_time = get_average_mac_time(pattern_input, filter_cross, filter_x)
        
        # 결과 출력
        print(f"{key:<12} | {size_str:<5} | {expected_filter:<8} | {pred:<9} | {status:<6} | {avg_time:.3f}")

    # 최종 정확도 출력    
    accuracy = (correct_count / total_count) * 100
    print("-" * 65)
    print(f"총 처리 건수: {total_count}건")
    print(f"최종 정확도  : {accuracy:.2f}% ({correct_count}/{total_count})")
    print("=" * 65)