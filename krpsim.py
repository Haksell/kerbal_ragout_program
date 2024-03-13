from parsing import parse_file
import sys


def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <filename> <max_delay>")
        print(f"Example: python {sys.argv[0]} resources/steak 10")
    stocks, processes, optimization = parse_file(sys.argv[1])


if __name__ == "__main__":
    main()
