class Node:
    def __init__(self, val, parent, depth):
        self.val = val
        self.parent = parent
        self.depth = depth
        self.jump = None

class Tree:
    def __init__(self, root):
        self.root = root

    def add_leaf(self, u):
        v = u.parent
        if (v.jump != self.root) and (v.jump and v.jump.jump and 
           (v.depth - v.jump.depth == v.jump.depth - v.jump.jump.depth)):
            u.jump = v.jump.jump
        else:
            u.jump = v

    def Deque(self):
        return (None, None)

    def push_front(self, d, x):
        d_first, d_last = d
        if d_first is None:
            u = Node(x, self.root, 1)
            self.add_leaf(u)
            return (u, u)
        else:
            u = Node(x, d_first, d_first.depth + 1)
            self.add_leaf(u)
            return (u, d_last)

    def swap(self, d):
        d_first, d_last = d
        return (d_last, d_first)

    def push_back(self, d, x):
        return self.swap(self.push_front(self.swap(d), x))

    def level_ancestor(self, k, u):
        y = u.depth - k
        while u.depth != y:
            if u.jump.depth >= y:
                u = u.jump
            else:
                u = u.parent
        return u

    def lowest_commom_ancestor(self, u, v):
        if u.depth > v.depth:
            u, v = v, u
        v = self.level_ancestor(v.depth - u.depth, v)
        if u == v:
            return u
        while u.parent != v.parent:
            if u.jump != v.jump:
                u = u.jump
                v = v.jump
            else:
                u = u.parent
                v = v.parent
        return u.parent

    def pop_front(self, d):
        d_first, d_last = d
        if d_first == d_last:
            return self.Deque()
        elif self.lowest_commom_ancestor(d_first, d_last) == d_first:
            return (self.level_ancestor(d_last.depth - d_first.depth - 1, d_last), d_last)
        else:
            return (d_first.parent, d_last)

    def pop_back(self, d):
        return self.swap(self.pop_front(self.swap(d)))

    def kth(self, d, k):
        d_first, d_last = d
        mid = self.lowest_commom_ancestor(d_first, d_last)
        l1 = d_first.depth - mid.depth
        l2 = d_last.depth - mid.depth
        if k - 1 <= l1:
            return self.level_ancestor(k - 1, d_first)
        else:
            return self.level_ancestor(l1 + l2 + 1 - k, d_last)

    def print_deque(self, d):
        d_first, d_last = d
        values = []
        if d_first is not None:
            lca = self.lowest_commom_ancestor(d_first, d_last)
            u = d_first
            while u != lca:
                values.append(u.val)
                u = u.parent
            values.append(lca.val)
            u = d_last
            suffix = []
            while u != lca:
                suffix.append(u.val)
                u = u.parent
            values += reversed(suffix)
        return values

# Process input and apply operations
def process_commands(commands):
    root = Node(None, None, 0)
    root.jump = root
    tree = Tree(root)
    deques = [tree.Deque()]
    output = []

    for command in commands:
        parts = list(map(int, command.split()))
        op = parts[0]
        t = parts[1]

        if op == 1:
            x = parts[2]
            deques.append(tree.push_front(deques[t], x))
        elif op == 2:
            x = parts[2]
            deques.append(tree.push_back(deques[t], x))
        elif op == 3:
            deques.append(tree.pop_front(deques[t]))
        elif op == 4:
            deques.append(tree.pop_back(deques[t]))
        elif op == 5:
            d_first, _ = deques[t]
            output.append(str(d_first.val))
        elif op == 6:
            _, d_last = deques[t]
            output.append(str(d_last.val))
        elif op == 7:
            k = parts[2]
            node = tree.kth(deques[t], k)
            output.append(str(node.val))
        elif op == 8:
            values = tree.print_deque(deques[t])
            output.append(" ".join(map(str, values)))
    
    return output

# Function to process input from file and save output to another file
def file_based_deque_processor(input_file_path):
    with open(input_file_path, 'r') as file:
        commands = file.read().strip().split('\n')

    results = process_commands(commands)

    for line in results:
        print(line)

# Example usage:
file_based_deque_processor('input.txt')
