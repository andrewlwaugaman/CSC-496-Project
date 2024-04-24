from shared_main import shared_main

from stv import scheme


def main() -> None:
    shared_main("stv", scheme)


if __name__ == "__main__":
    main()

# python3 main.py --corpus elections.json --overwrite