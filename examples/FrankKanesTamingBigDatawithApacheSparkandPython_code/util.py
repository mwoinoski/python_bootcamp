"""
Utility functions for PySpark examples
"""

from argparse import ArgumentParser, Namespace
from getpass import getpass


def file_url(filename: str) -> str:
    """ Generate a file:// URL for the given filename in the current dir """
    import pathlib
    parent_dir = str(pathlib.Path().absolute())
    return f"file://{parent_dir}/{filename}"


def get_db_credentials() -> Namespace:
    """ Get a DB username and password from the command line or keyboard """
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-u', '--user', type=str, default='SA')
    parser.add_argument('-p', '--password', type=str)
    args: Namespace = parser.parse_args()
    if not args.password:
            args.password = getpass(f"\nEnter password for DB user {args.user}: ")
    return args
