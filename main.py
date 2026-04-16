import sys
from boards_parser import parse_boards_data


def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "boards_parser":
            parse_boards_data()


if __name__ == "__main__":
    main()