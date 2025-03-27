import random

class TreapNode:
    def __init__(self, key, priority=None):
        self.key = key
        self.priority = priority if priority is not None else random.randint(1, 1000)
        self.left = None
        self.right = None

class Treap:
    def __init__(self):
        self.root = None

    def insert(self, x):
        self.root = self._insert(self.root, x)

    def delete(self, x):
        self.root = self._delete(self.root, x)

    def search(self, x):
        return self._search(self.root, x)

    def get_min(self):
        return self._min(self.root)

    def print_tree(self):
        self._print_rec(self.root, 0)

    def _rotate_left(self, root):
        R = root.right
        root.right = R.left
        R.left = root
        return R

    def _rotate_right(self, root):
        L = root.left
        root.left = L.right
        L.right = root
        return L

    def _insert(self, node, x):
        if not node:
            return TreapNode(x)
        if x < node.key:
            node.left = self._insert(node.left, x)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        else:
            node.right = self._insert(node.right, x)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)
        return node

    def _delete(self, node, x):
        if not node:
            return None
        if x < node.key:
            node.left = self._delete(node.left, x)
        elif x > node.key:
            node.right = self._delete(node.right, x)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            else:
                if node.left.priority > node.right.priority:
                    node = self._rotate_right(node)
                    node.right = self._delete(node.right, x)
                else:
                    node = self._rotate_left(node)
                    node.left = self._delete(node.left, x)
        return node

    def _search(self, node, x):
        if not node:
            return False
        if x == node.key:
            return True
        elif x < node.key:
            return self._search(node.left, x)
        else:
            return self._search(node.right, x)

    def _min(self, node):
        if not node:
            return None
        while node.left:
            node = node.left
        return node.key

    def _print_rec(self, u, i):
        if not u:
            return
        self._print_rec(u.left, i + 3)
        print(" " * i + f"{u.key} {u.priority}")
        self._print_rec(u.right, i + 3)

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 treap.py <input_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as file:
        lines = file.readlines()

    treap = Treap()
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        op = int(parts[0])
        if op == 1:
            treap.insert(int(parts[1]))
        elif op == 2:
            treap.delete(int(parts[1]))
        elif op == 3:
            print(1 if treap.search(int(parts[1])) else 0)
        elif op == 4:
            print(treap.get_min())
        elif op == 5:
            treap.print_tree()
