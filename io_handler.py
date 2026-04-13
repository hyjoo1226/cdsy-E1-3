# 사용자로부터 패턴과 필터 매트릭스를 입력받는 함수
def get_matrix_input(name, size=3):
    print(f"{name} ({size}줄 입력, 공백 구분)")
    
    matrix = []
    
    while len(matrix) < size:
        try:
            raw_input_data = input(f"{len(matrix) + 1}행: ").strip()

            if not raw_input_data:
                continue

            parsed_data = [float(x) for x in raw_input_data.split()]
            
            if len(parsed_data) != size:
                print(f"각 줄에 {size}개의 숫자를 공백으로 구분해 입력해주세요.")
                continue
            
            matrix.append(parsed_data)
            
        except ValueError:
            print("숫자만 입력 가능합니다. 다시 입력해주세요.")
            
    return matrix