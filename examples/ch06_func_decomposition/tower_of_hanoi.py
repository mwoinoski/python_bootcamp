"""
Solve the Tower of Hanoi puzzle (recursively, of course)
"""


def move_disks(how_many, from_stack, to_stack):
    if how_many:
        other_stack = 6 - from_stack - to_stack
        move_disks(how_many - 1, from_stack, other_stack)
        print(f'move disk from stack {from_stack} to {to_stack}')
        move_disks(how_many - 1, other_stack, to_stack)


move_disks(how_many=6, from_stack=1, to_stack=2)
