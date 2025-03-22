class Node:
    def __init__(self, val, parent, depth):
        self.val = val        # Value stored in the deque
        self.parent = parent  # Parent node in the tree
        self.depth = depth    # Depth in the tree
        self.jump = None      # Jump pointer for Level Ancestor

        v = parent
        if parent != None and v.depth - v.jump.depth == v.jump.depth - v.jump.jump.depth:
            self.jump = v.jump.jump
        else:
            self.jump = v 


    def __repr__(self):
        if self.val != None:
            return str(self.val)
        else:
            return "None"

class PersistentDeque:
    def __init__(self, first, last):
        self.first = first
        self.last = last

def deque():
    return PersistentDeque(None, None)

def front(d):
    return d.first.val

def back(d):
    return d.last.val

def swap(d):
    return PersistentDeque(d.last, d.first)

def push_front(d, x):
    if d.first == None:
        u = Node(x, None, 1)
        return PersistentDeque(u, u)

    else:
        return PersistentDeque(Node(x, d.first, d.first.depth + 1), d.last)
    
def push_back(d, x):
    return swap(push_front(swap(d), x))


def level_ancestor(k, u):
    y = u.depth - k
    while u.depth != y:
        if u.jump.depth >= y:
            u = u.jump
        else:
            u = u.parent
    
    return u


d_0 = deque()
d_1 = push_front(d_0, 1)
print(d_1.first, d_1.last)
d_2 = push_front(d_1, 2)
print(d_2.first, d_2.last)
d_3 = push_front(d_2, 3)
#
#print(d_3.first, d_3.last)
