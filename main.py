from engine import calculate_mac

def main():
    # 패턴과 필터 정의
    pattern = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
    
    filter_matrix = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]
    
    # MAC 계산
    score = calculate_mac(pattern, filter_matrix)
    
    print(f"MAC Score: {score}")

if __name__ == "__main__":
    main()