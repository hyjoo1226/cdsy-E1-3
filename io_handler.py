# 사용자로부터 패턴과 필터 매트릭스를 입력받는 함수
def get_matrix_input(name, size=3):
    print(f"{name} ({size}줄 입력, 공백 구분)")
    
    matrix = []
    
    while len(matrix) < size:
        try:
            raw_input_data = input(f"{len(matrix) + 1}행: ").strip()

            if not raw_input_data:
                print(f"각 줄에 {size}개의 숫자를 공백으로 구분해 입력해주세요.")
                continue

            parsed_data = [float(x) for x in raw_input_data.split()]
            
            if len(parsed_data) != size:
                print(f"각 줄에 {size}개의 숫자를 공백으로 구분해 입력해주세요.")
                continue
            
            matrix.append(parsed_data)
            
        except ValueError:
            print("숫자만 입력 가능합니다. 다시 입력해주세요.")
            
    return matrix

# 공통 입력 예외 처리(숫자)
def get_int_input(prompt, min_val, max_val):
    while True:
        try:
            # 앞뒤 공백 제거
            user_input = input(prompt).strip()

            # 빈 입력 처리
            if not user_input:
                print("값을 입력해주세요.")
                continue

            # 숫자 변환 실패 처리
            temp_number = int(user_input)

            # 허용 범위 밖 숫자 처리
            if not (min_val <= temp_number <= max_val):
                print(f"{min_val}~{max_val} 사이의 숫자를 입력해주세요.")
                continue

            validate_input = temp_number

            return validate_input

        except ValueError:
            print("숫자를 입력해주세요.")