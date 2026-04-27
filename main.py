"""Module Providing Version Information"""

import sys
from version import VERSION


def get_version():
    """Function returning the version of the application"""
    return VERSION


def print_version():
    """Function printing the version of the application"""
    print(get_version())


if __name__ == "__main__":
    if "--version" in sys.argv:
        print_version()
