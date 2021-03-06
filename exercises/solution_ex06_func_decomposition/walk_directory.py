"""
Recursive directory walk
"""


import sys
import pathlib


# TODO: define a global function named walk_directory, which takes 2 arguments:
#       1. a Path with the directory to walk
#       2. an int with the number of spaces to indent
def walk_directory(path, indent: int):
    # TODO: print the number of spaces indicated by `indent`, followed by `path
    # HINT: use the following Python trick to get the right number of spaces:
    #       " " * indent
    print(f'{" " * indent}{path}')

    # TODO: call the path's is_dir method. If it returns True, go to the next
    #       step. Otherwise, do nothing
    if path.is_dir():

        # TODO: set up a `for` loop over all the files returned returned by
        #       path.iterdir()
        for file in path.iterdir():

            # TODO: call walk_directory recursively, passing the current file and
            #       indent + 4
            walk_directory(file, indent + 4)


if __name__ == '__main__':
    path = pathlib.Path(sys.argv[1])

    # TODO: note the initial call to walk_directory
    walk_directory(path, 0)
