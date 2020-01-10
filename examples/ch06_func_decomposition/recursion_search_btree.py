"""
Binary tree creation and searching.
"""

from dataclasses import dataclass


class Node:
    """ Binary tree node """
    def __init__(self, data, left, right) -> None:
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data)


@dataclass
class Patient:
    id: int
    name: str


def inorder(node):
    if node is not None:
        inorder(node.left)
        print(node)
        inorder(node.right)


def add_to_tree(root, patient):
    if root:
        if patient.id < root.data.id:
            if not root.left:
                root.left = Node(patient, None, None)
            else:
                add_to_tree(root.left, patient)
        else:
            if not root.right:
                root.right = Node(patient, None, None)
            else:
                add_to_tree(root.right, patient)


def search_tree(root, pid):
    if not root:
        return None
    else:
        if pid == root.data.id:
            return root.data
        elif pid < root.data.id:
            return search_tree(root.left, pid)
        else:
            return search_tree(root.right, pid)


names = ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte',
         'Liam', 'Noah', 'William', 'James', 'Logan', 'Benjamin', 'Mason',
         'Amelia', 'Evelyn', 'Abigail', 'Harper', 'Emily', 'Avery',
         'Elijah', 'Oliver', 'Jacob', 'Lucas', 'Alexander', 'Ethen']

patients = [Patient(i + 1, n) for i, n in enumerate(names)]

if __name__ == '__main__':

    tree = Node(patients[0], None, None)
    for p in patients[1:]:
        add_to_tree(tree, p)

    inorder(tree)

    for pat_id in [1, 17, 26, 99]:
        found = search_tree(tree, pat_id)
        print(f'patient with ID {pat_id}: {found}')
