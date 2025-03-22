import argparse
from typing import Optional, List

class Node:
    def __init__(self, val: Optional[int], parent: Optional["Node"], depth: int):
        self.val = val
        self.parent = parent
        self.depth = depth
        self.jump: Optional["Node"] = None

class Tree:
    def __init__(self, root: Node):
        self.root = root

    def add_leaf(self, u: Node):
        v = u.parent
        if v and v.jump and v.jump.jump and (v.jump != self.root) and (
                v.depth - v.jump.depth == v.jump.depth - v.jump.jump.depth):
            u.jump = v.jump.jump
        else:
            u.jump = v

    def level_ancestor(self, k: int, u: Node) -> Node:
        target_depth = u.depth - k
        while u.depth != target_depth:
            if u.jump and u.jump.depth >= target_depth:
                u = u.jump
            else:
                u = u.parent
        return u

    def lowest_common_ancestor(self, u: Node, v: Node) -> Node:
        if u.depth > v.depth:
            u, v = v, u
        v = self.level_ancestor(v.depth - u.depth, v)
        if u == v:
            return u
        while u.parent != v.parent:
            if u.jump != v.jump:
                u, v = u.jump, v.jump
            else:
                u, v = u.parent, v.parent
        return u.parent

class Deque:
    def __init__(self, tree: Tree):
        self.tree = tree
        self.front: Optional[Node] = None
        self.back: Optional[Node] = None

    def is_empty(self) -> bool:
        return self.front is None

    def push_front(self, x: int):
        if self.is_empty():
            u = Node(x, self.tree.root, 1)
        else:
            u = Node(x, self.front, self.front.depth + 1)
        self.tree.add_leaf(u)
        self.front = u
        if self.back is None:
            self.back = u

    def push_back(self, x: int):
        self.swap()
        self.push_front(x)
        self.swap()

    def pop_front(self):
        if self.is_empty():
            return
        if self.front == self.back:
            self.front = self.back = None
        else:
            if self.tree.lowest_common_ancestor(self.front, self.back) == self.front:
                self.front = self.tree.level_ancestor(self.back.depth - self.front.depth - 1, self.back)
            else:
                self.front = self.front.parent

    def pop_back(self):
        self.swap()
        self.pop_front()
        self.swap()

    def front_value(self) -> Optional[int]:
        return self.front.val if self.front else None

    def back_value(self) -> Optional[int]:
        return self.back.val if self.back else None

    def kth(self, k: int) -> Optional[int]:
        if self.is_empty():
            return None
        mid = self.tree.lowest_common_ancestor(self.front, self.back)
        l1 = self.front.depth - mid.depth
        l2 = self.back.depth - mid.depth
        if k - 1 <= l1:
            return self.tree.level_ancestor(k - 1, self.front).val
        else:
            return self.tree.level_ancestor(l1 + l2 + 1 - k, self.back).val

    def print_deque(self) -> str:
        if self.is_empty():
            return ""
        values = []
        lca = self.tree.lowest_common_ancestor(self.front, self.back)
        node = self.front
        while node != lca:
            values.append(str(node.val))
            node = node.parent
        values.append(str(lca.val))
        node = self.back
        suffix = []
        while node != lca:
            suffix.append(str(node.val))
            node = node.parent
        values.extend(reversed(suffix))
        return " ".join(values)

    def swap(self):
        self.front, self.back = self.back, self.front

class DequeManager:
    def __init__(self):
        root = Node(None, None, 0)
        root.jump = root
        self.tree = Tree(root)
        self.deques: List[Deque] = [Deque(self.tree)]

    def process_command(self, command: str) -> Optional[str]:
        parts = list(map(int, command.split()))
        op, t = parts[0], parts[1]

        if op == 1:
            x = parts[2]
            new_deque = Deque(self.tree)
            new_deque.front, new_deque.back = self.deques[t].front, self.deques[t].back
            new_deque.push_front(x)
            self.deques.append(new_deque)

        elif op == 2:
            x = parts[2]
            new_deque = Deque(self.tree)
            new_deque.front, new_deque.back = self.deques[t].front, self.deques[t].back
            new_deque.push_back(x)
            self.deques.append(new_deque)

        elif op == 3:
            new_deque = Deque(self.tree)
            new_deque.front, new_deque.back = self.deques[t].front, self.deques[t].back
            new_deque.pop_front()
            self.deques.append(new_deque)

        elif op == 4:
            new_deque = Deque(self.tree)
            new_deque.front, new_deque.back = self.deques[t].front, self.deques[t].back
            new_deque.pop_back()
            self.deques.append(new_deque)

        elif op == 5:
            return str(self.deques[t].front_value())

        elif op == 6:
            return str(self.deques[t].back_value())

        elif op == 7:
            k = parts[2]
            return str(self.deques[t].kth(k))

        elif op == 8:
            return self.deques[t].print_deque()

        return None

    def process_file(self, input_file: str):
        with open(input_file, 'r') as file:
            commands = file.read().strip().split('\n')

        results = [self.process_command(command) for command in commands]
        results = [res for res in results if res is not None]

        for line in results:
            print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process deque operations from a file.")
    parser.add_argument("input_file", help="Path to the input file containing operations.")

    args = parser.parse_args()

    manager = DequeManager()
    manager.process_file(args.input_file)
