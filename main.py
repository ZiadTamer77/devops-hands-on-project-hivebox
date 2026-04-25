import sys
from version import VERSION


def get_version():
    return VERSION


def print_version():
    print(get_version())


if __name__ == "__main__":
    if "--version" in sys.argv:
        print_version()
