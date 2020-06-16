class Node:
    def __init__(self, val, left=None, right=None, parent=None):
        self.value = val
        self.sum_below = val
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return f"{self.value}"


class SplayTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
            return
        current = self.root
        while True:
            if current.value == val:
                break
            if val < current.value:
                if current.left is None:
                    current.left = Node(val)
                    current.sum_below += val
                    current.left.parent = current
                    self._splay(current.left)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(val)
                    current.right.parent = current
                    current.sum_below += val
                    self._splay(current.right)
                    break
                current = current.right

    def find(self, val):
        current = self.root
        if current is None:
            return False

        while True:
            if val == current.value:
                self._splay(current)
                return True
            elif val < current.value:
                if current.left is None:
                    self._splay(current)
                    return False
                current = current.left
            elif val > current.value:
                if current.right is None:
                    self._splay(current)
                    return False
                current = current.right

    def remove(self, val):
        if self.find(val):  # Now val is the root
            self.root = self._merge(self.root.left, self.root.right)

    def sum_range(self, min_val, max_val):
        pass

    def _splay(self, node):
        while node.parent is not None:
            parent = node.parent
            gparent = parent.parent
            if gparent is None:
                SplayTree._swap(node, parent)
            else:
                if (gparent.left == parent) == (parent.left == node):
                    SplayTree._swap(parent, gparent)
                    SplayTree._swap(node, parent)
                else:
                    SplayTree._swap(node, parent)
                    SplayTree._swap(node, gparent)
        self.root = node

    def _set_root(self, node):
        self.root = node
        node.parent = None

    def test_some_shit(self):
        print(f"Here is root node before shit: {self.root}")
        c = self.root
        c.value = 666
        print(f"Here is changed copy of root: {c}, here is original root: {self.root}")

    @staticmethod
    def _merge(left, right):
        """
        :param left: Node
        :param right: Node
        :return: root node of merged tree
        """
        if left is None:
            return right
        if right is None:
            return left
        tree = SplayTree()
        SplayTree._set_root(tree, left)
        current = tree.root
        while current.right is not None:
            current = current.right
        tree._splay(current)
        tree.root.right = right
        tree.root.right.parent = tree.root
        return tree.root

    @staticmethod
    def _make_parent(parent):
        if parent.left is not None:
            parent.left.parent = parent
        if parent.right is not None:
            parent.right.parent = parent

    @staticmethod
    def _swap(child, parent):
        gparent = parent.parent
        if gparent is not None:
            if gparent.left == parent:
                gparent.left = child
            else:
                gparent.right = child
        if parent.left == child:
            parent.left = child.right
            child.right = parent
        else:
            parent.right = child.left
            child.left = parent
        # Making nodes their kids' parents
        SplayTree._make_parent(child)
        SplayTree._make_parent(parent)
        child.parent = gparent


def random_insert_find_test(n_elements=10000, rand_seed=1):
    import random

    t = SplayTree()
    random.seed(rand_seed)
    elements = set([random.randint(0, 10**9) for _ in range(n_elements)])
    for i, el in enumerate(elements):
        t.insert(el)
        try:
            assert t.root.value == el
        except AssertionError:
            print(i, el, t.root.value)

    for el in elements:
        t.find(el)
        try:
            assert t.root.value == el
        except AssertionError:
            print(el, t.root.value)

    print("All good with random insert-find test!")


if __name__ == "__main__":
    for i in range(20):
        random_insert_find_test(rand_seed=i)

    
