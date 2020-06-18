class Node:
    def __init__(self, val, left=None, right=None, parent=None):
        self.value = val
        self.sum_below = 0
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
            self.root.sum_below = val
            return

        current = self.root
        while True:
            if current.value == val:
                break
            if val < current.value:
                if current.left is None:
                    current.left = Node(val)
                    current.left.parent = current
                    SplayTree._update_sums_above(current.left)
                    self._splay(current.left)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(val)
                    current.right.parent = current
                    SplayTree._update_sums_above(current.right)
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
        if max_val < min_val or self.root is None:
            return 0

        init_sum = self.root.sum_below
        self.find(min_val)
        if self.root.left is not None:
            init_sum -= self.root.left.sum_below
        if self.root.value < min_val:
            init_sum -= self.root.value

        self.find(max_val)
        if self.root.right is not None:
            init_sum -= self.root.right.sum_below
        if self.root.value > max_val:
            init_sum -= self.root.value
        return init_sum

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
    def _update_sums_above(node):
        while node is not None:
            node.sum_below = node.value
            if node.left is not None:
                node.sum_below += node.left.sum_below
            if node.right is not None:
                node.sum_below += node.right.sum_below
            node = node.parent

    @staticmethod
    def _merge(left, right):
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
        tree.root.sum_below += right.sum_below
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

        parent.sum_below -= child.sum_below
        if parent.left == child:
            parent.left = child.right
            if child.right is not None:
                parent.sum_below += child.right.sum_below
                child.sum_below -= child.right.sum_below
            child.right = parent
        else:
            parent.right = child.left
            if child.left is not None:
                parent.sum_below += child.left.sum_below
                child.sum_below -= child.left.sum_below
            child.left = parent
        child.sum_below += parent.sum_below

        # Making nodes their kids' parents
        SplayTree._make_parent(child)
        SplayTree._make_parent(parent)
        child.parent = gparent


def random_insert_find_test(n_elements=1000000, rand_seed=1):
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


def random_test_sum_below(n_elements=10000, rand_seed=1):
    import random

    t = SplayTree()
    elements = [random.randint(0, 10**9) for _ in range(n_elements)]
    added_elements = []
    current_sum = 0
    for i, el in enumerate(elements):
        if el not in added_elements:
            current_sum += el
            added_elements.append(el)
        t.insert(el)
        try:
            assert t.root.sum_below == current_sum
        except AssertionError as e:
            raise Exception(f"Iteration: {i}, root sum: {t.root.sum_below}, current sum: {current_sum}").\
                with_traceback(e.__traceback__)

    for j, el in enumerate(added_elements[:-1]):
        current_sum -= el
        t.remove(el)
        try:
            assert t.root.sum_below == current_sum
        except AssertionError as e:
            raise Exception(f"Removal gone wrong. Iteration: {j}, root sum: {t.root.sum_below}, "
                            f"current sum: {current_sum}").with_traceback(e.__traceback__)
    print(f"All good with random sum below (insertions and removals) test!")


def random_sum_range(n_elements=10000, n_tests=100, rand_seed=1):
    import random

    t = SplayTree()
    elements = [random.randint(0, 10**9) for _ in range(n_elements)]
    for el in elements:
        t.insert(el)

    for i in range(n_tests):
        l, r = sorted([random.choice(elements), random.choice(elements)])
        actual_sum = sum([x for x in elements if l <= x <= r])
        tree_sum = t.sum_range(l, r)
        try:
            assert tree_sum == actual_sum
        except AssertionError as e:
            raise Exception(f"Test #: {i}, actual_sum: {actual_sum}, tree_sum: {tree_sum}").\
                with_traceback(e.__traceback__)
    print("All good with random sum range!")


if __name__ == "__main__":
    random_insert_find_test()
    random_test_sum_below()
    random_sum_range()


