"""
Recursive tree traversals.
"""


class Node:
    """ Binary tree node """
    def __init__(self, data, left, right) -> None:
        self.data = data
        self.left = left
        self.right = right


def preorder(node, visitor):
    if node is not None:
        visitor(node.data)
        preorder(node.left, visitor)
        preorder(node.right, visitor)


def inorder(node, visitor):
    if node is not None:
        inorder(node.left, visitor)
        visitor(node.data)
        inorder(node.right, visitor)


def postorder(node, visitor):
    if node is not None:
        postorder(node.left, visitor)
        postorder(node.right, visitor)
        visitor(node.data)


def levelorder(node, visitor, more=None):
    if node is not None:
        if more is None:
            more = []
        more += [node.left, node.right]
        visitor(node.data)
    if more:
        levelorder(more[0], visitor, more[1:])


tree = Node(1,
            Node(2,
                 Node(4, None, None),
                 Node(5, None, None)),
            Node(3,
                 Node(6, None, None),
                 Node(7, None, None))
            )

if __name__ == '__main__':
    print('preorder: ')
    preorder(tree, lambda x: print(f'{x} ', end=''))

    print('\ninorder: ')
    inorder(tree, lambda x: print(f'{x} ', end=''))

    print('\npostorder: ')
    postorder(tree, lambda x: print(f'{x} ', end=''))

    print('\nlevelorder: ')
    levelorder(tree, lambda x: print(f'{x} ', end=''))

    print('\n')