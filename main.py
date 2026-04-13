from mode import choice_menu

def main():
    try:
        choice_menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n오류가 발생했습니다")

if __name__ == "__main__":
    main()