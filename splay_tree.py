import sys


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
            # current.sum_below += val
            if val < current.value:
                if current.left is None:
                    current.left = Node(val)
                    current.left.parent = current
                    self._splay(current.left)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(val)
                    current.right.parent = current
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
                    # self._splay(current)
                    return False
                current = current.left
            elif val > current.value:
                if current.right is None:
                    # self._splay(current)
                    return False
                current = current.right

    def remove(self, val):
        if self.find(val):  # Now val is the root
            self.root = self._merge(self.root.left, self.root.right)

    def sum_range(self, min_val=float("-inf"), max_val=float("inf")):
        answer = 0
        current = self.root
        previous_value = float("-inf")
        stack = []
        while True:
            while current is not None:
                stack.append(current)
                current = current.left

            if current is None and stack:
                current = stack.pop()
                if min_val <= current.value <= max_val:
                    answer += current.value
                current = current.right

            if current is None and not stack:
                return answer

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
        self.root.parent = None

    @staticmethod
    def _merge(left, right):
        """
        :param left: Node
        :param right: Node
        :return: root node of merged tree
        """
        if left is None and right is None:
            return None
        if left is None:
            right.parent = None
            return right
        if right is None:
            left.parent = None
            return left
        tree = SplayTree()
        SplayTree._set_root(tree, left)
        current = tree.root
        while current.right is not None:
            current = current.right
        tree._splay(current)
        tree.root.right = right
        tree.root.right.parent = tree.root
        # tree.root.sum_below += right.sum_below
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

        # parent.sum_below -= child.sum_below
        if parent.left == child:
            parent.left = child.right
            # if child.right is not None:
                # parent.sum_below += child.right.sum_below
                # child.sum_below -= child.right.sum_below
            child.right = parent
        else:
            parent.right = child.left
            # if child.left is not None:
                # parent.sum_below += child.left.sum_below
                # child.sum_below -= child.left.sum_below
            child.left = parent
        # child.sum_below += parent.sum_below

        # Making nodes their kids' parents
        SplayTree._make_parent(child)
        SplayTree._make_parent(parent)
        child.parent = gparent


def pass_stepik_tests():
    reader = (x.split() for x in sys.stdin)
    n = int(next(reader)[0])
    t = SplayTree()
    s = 0
    for _ in range(n):
        query, *rest = next(reader)
        if len(rest) == 1:
            a = (s + int(rest[0])) % 1_000_000_001
        else:
            a = [(s + int(x)) % 1_000_000_001 for x in rest]
        if query == "?":
            print(["Not found", "Found"][t.find(a)])
        elif query == "+":
            t.insert(a)
        elif query == "-":
            t.remove(a)
        else:  #  query == "s"
            s = t.sum_range(*a)
            print(s)


def random_insert_find_test(n_elements=10000, rand_seed=1):
    import random

    t = SplayTree()
    random.seed(rand_seed)
    elements = set([random.randint(0, 10**3) for _ in range(n_elements)])
    total_sum = sum(elements)
    for i, el in enumerate(elements):
        t.insert(el)
        try:
            assert t.root.value == el
        except AssertionError as e:
            raise Exception(f"Element: {el}, root value: {t.root.value}").\
                with_traceback(e.__traceback__)

    for el in elements:
        t.find(el)
        try:
            assert t.root.value == el
        except AssertionError as e:
            raise Exception(f"Element: {el}, root value: {t.root.value}").\
                with_traceback(e.__traceback__)
    print("All good with random insert-find test!")


def random_test_sum_below(n_elements=100, rand_seed=1):
    import random

    t = SplayTree()
    elements = [random.randint(0, 10**3) for _ in range(n_elements)]
    added_elements = []
    current_sum = 0
    for el in elements:
        if el not in added_elements:
            current_sum += el
            added_elements.append(el)
        t.insert(el)
        try:
            assert t.root.sum_below == current_sum
        except AssertionError as e:
            raise Exception(f"Root sum: {t.root.sum_below}, current sum: {current_sum}").\
                with_traceback(e.__traceback__)
    print("If there were no messages above it's all good!")


def random_sum_range(n_elements=10000, n_tests=100, rand_seed=1):
    import random

    t = SplayTree()
    elements = [random.randint(0, 10**9) for _ in range(n_elements)]
    for el in elements:
        t.insert(el)
    for _ in range(n_tests):
        l, r = sorted([random.choice(elements), random.choice(elements)])
        actual_sum = sum([x for x in elements if l <= x <= r])
        tree_sum = t.sum_range(l, r)
        try:
            assert tree_sum == actual_sum
        except AssertionError as e:
            raise Exception(f"Actual_sum: {actual_sum}, tree_sum: {tree_sum}").\
                with_traceback(e.__traceback__)

    print("All good with random sum range!")




if __name__ == "__main__":
    # random_insert_find_test()
    # random_sum_range()
    pass_stepik_tests()


