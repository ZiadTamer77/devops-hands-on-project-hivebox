import sys
from version import VERSION


def print_version():
    print(VERSION)


if __name__ == "__main__":
    if "--version" in sys.argv:
        print_version()
