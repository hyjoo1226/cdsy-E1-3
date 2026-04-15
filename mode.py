import json
from engine import calculate_mac, compare_scores, get_average_mac_time, normalize_label, EPSILON
from io_handler import get_matrix_input, get_int_input, print_matrix

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
    print("#" + "-" * 30)
    print("#[1] 필터 입력")
    print("#" + "-" * 30)

    # 입력
    filter_a = get_matrix_input("필터 A", 3)
    print("\n")
    filter_b = get_matrix_input("필터 B", 3)
    print("\n[입력 확인] 필터 A가 다음과 같이 입력되었습니다:")
    print_matrix(filter_a)
    print("\n[입력 확인] 필터 B가 다음과 같이 입력되었습니다:")
    print_matrix(filter_b)
    print("-" * 20)
    print("#" + "-" * 30)
    print("#[2] 패턴 입력")
    print("#" + "-" * 30)
    print("\n")
    pattern = get_matrix_input("패턴", 3)
    
    # 연산
    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)
    
    # 판정
    result = compare_scores(score_a, score_b)

    # 시간 측정
    avg_time = get_average_mac_time(pattern, filter_a, filter_b)

    # 결과 출력
    print("\n#" + "-"*30)
    print("# [3] MAC 결과")
    print("#" + "-"*30)

    if result == "UNDECIDED":
        print(f"A 점수: {score_a:.16f}")
        print(f"B 점수: {score_b:.16f}")
        print(f"연산 시간(평균/10회): {avg_time:.3f} ms")
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print(f"A 점수: {score_a}")
        print(f"B 점수: {score_b}")
        print(f"연산 시간(평균/10회): {avg_time:.3f} ms")
        print(f"판정: {result}")
    print("\n")

    # 성능 분석 표
    print("\n#" + "-"*30)
    print("# [4] 성능 분석 (평균/10회)")
    print("#" + "-"*30)
    print(f"{'크기':<7} {'평균 시간(ms)':<13} {'연산 횟수'}")
    print("-" * 39)
    print(f"{'3x3':<11} {avg_time:<16.3f} {3*3}")
    print("\n")

# 모드 2: data.json 분석 모드
def run_data_analysis_mode():
    # 파일 읽기, 예외 처리
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"파일을 읽을 수 없습니다: {e}")
        return
    
    
    filters = data.get("filters", {})
    patterns = data.get("patterns", {})

    print("#" + "-" * 30)
    print("#[1] 필터 로드")
    print("#" + "-" * 30)
    for size_key in filters.keys():
        print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")

    total_tests = len(patterns)
    passed_count = 0
    failed_cases = []
    time_stats = {}

    if total_tests == 0:
        print("data.json에 분석할 패턴 데이터가 없습니다.")
        return

    print("\n#" + "-" * 30)
    print("#[2] 패턴 분석")
    print("#" + "-" * 30)
    
    # 데이터 순회 및 연산
    for key, value in patterns.items():
        print(f"--- {key} ---")

        # 사이즈 추출
        size_str = key.split('_')[1]
        filter_key = f"size_{size_str}" # "size_5" 형태
        
        # 필터 키 정규화
        current_filters = filters[filter_key]
        filter_cross = None
        filter_x = None
        for k, v in current_filters.items():
            norm_k = normalize_label(k) 
            if norm_k == "Cross":
                filter_cross = v
            elif norm_k == "X":
                filter_x = v
        
        pattern_input = value["input"]

        # 크기 불일치 검증
        pattern_rows = len(pattern_input)
        pattern_cols = len(pattern_input[0]) if pattern_rows > 0 else False

        cross_r = len(filter_cross)
        cross_c = len(filter_cross[0]) if cross_r > 0 else False

        x_r = len(filter_x)
        x_c = len(filter_x[0]) if x_r > 0 else False

        # 패턴 행별 열 수
        row_mismatch = any(len(row) != pattern_cols for row in pattern_input)

        # 필터 행별 열 수
        cross_row_mismatch = filter_cross and any(len(row) != cross_c for row in filter_cross)
        x_row_mismatch = filter_x and any(len(row) != x_c for row in filter_x)

        # 행렬 가로/세로 전체 크기
        cross_mismatch = (pattern_rows != cross_r or pattern_cols != cross_c)
        x_mismatch = (pattern_rows != x_r or pattern_cols != x_c)

        if row_mismatch or cross_row_mismatch or x_row_mismatch or cross_mismatch or x_mismatch:
            expected = normalize_label(value["expected"])
            if row_mismatch:
                reason = f"패턴 행별 열 수 불일치 ({[len(r) for r in pattern_input]})"
            elif cross_row_mismatch:
                reason = f"Cross 필터 행별 열 수 불일치 ({[len(r) for r in filter_cross]})"
            elif x_row_mismatch:
                reason = f"X 필터 행별 열 수 불일치 ({[len(r) for r in filter_x]})"
            elif cross_mismatch:
                reason = f"크기 불일치 (패턴:{pattern_rows}x{pattern_cols}, Cross필터:{cross_r}x{cross_c})"
            else:
                reason = f"크기 불일치 (패턴:{pattern_rows}x{pattern_cols}, X필터:{x_r}x{x_c})"
            print(f"판정: ERROR | expected: {expected} | FAIL (데이터 오류)")
            failed_cases.append((key, reason))
            continue
        
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
        # expected 값 정규화
        expected = normalize_label(value["expected"])

        if result == expected:
            status = "PASS"
            passed_count += 1
            print(f"Cross 점수: {score_cross}")
            print(f"X 점수: {score_x}")
        else:
            status = "FAIL (동점 규칙)"
            if result == "UNDECIDED":
                reason = "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
                print(f"Cross 점수: {score_cross:.16f}")
                print(f"X 점수: {score_x:.16f}")
            else:
                reason = "불일치"
                print(f"Cross 점수: {score_cross}")
                print(f"X 점수: {score_x}")
            failed_cases.append((key, reason))

        print(f"판정: {result} | expected: {expected} | {status}")

        # 시간 측정
        # 3x3 시간 측정용 더미
        dummy_pattern = [[0.0]*3 for _ in range(3)]
        dummy_filter = [[0.0]*3 for _ in range(3)]
        time_stats["3"] = [get_average_mac_time(dummy_pattern, dummy_filter, dummy_filter)]

        avg_time = get_average_mac_time(pattern_input, filter_cross, filter_x)
        if size_str not in time_stats:
            time_stats[size_str] = []
        time_stats[size_str].append(avg_time)

    # 성능 분석
    print("\n#" + "-" * 30)
    print("#[3] 성능 분석 (평균/10회)")
    print("#" + "-" * 30)
    print(f"{'크기':<7} {'평균 시간(ms)':<13} {'연산 횟수'}")
    print("-" * 39)
        
    for s_int in sorted([int(s) for s in time_stats.keys()]):
        s_str = str(s_int)
        avg_val = sum(time_stats[s_str]) / len(time_stats[s_str])
        print(f"{s_int}x{s_int:<9} {avg_val:<16.3f} {s_int*s_int}")

    # 결과 요약
    print("\n#" + "-" * 30)
    print("#[4] 결과 요약")
    print("#" + "-" * 30)
    print(f"총 테스트: {total_tests}개")
    print(f"통과: {passed_count}개")
    print(f"실패: {len(failed_cases)}개")
    if failed_cases:
        print("실패 케이스:")
        for c_id, res in failed_cases:
            print(f"- {c_id}: {res}")
    print("\n")