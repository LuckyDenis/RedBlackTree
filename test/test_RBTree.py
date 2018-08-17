# _-*- coding: utf8 -*-


import math
import pytest
from random import randint

from RedBlackTree import RedBlackTree


def setup_tree(n):
    tree = RedBlackTree()
    for i in range(n):
        tree[i] = i
    return tree


def test_size():
    """
    Check size tree

    test 1: check for dimensional accuracy (10 000)
    test 2: check for is empty tree
    """

    # test 1
    n = 10000
    tree = setup_tree(n)
    assert len(tree) == n

    # test 2
    tree.clear_tree()
    assert len(tree) == 0


def test_insert():
    """
    Check insert in tree

    test 1: insert of 10000 items with duplicate keys
    test 2 insert of 10000 items
    test 3: insert 10000 elements, then remove the keys from 5000 to 10000 and add 1000
    """

    tree = setup_tree(0)

    # test 1
    for i in range(10000):
        tree[randint(1, 100)] = i
    assert len(tree) == 100
    tree.clear_tree()

    # test 2
    n = 10000
    for i in range(n):
        tree[i] = i
    assert len(tree) == n

    # test 3
    for i in range(5000, n):
        del tree[i]
    for i in range(n, n + 1000):
        tree[i] = i
    assert len(tree) == 6000


def test_get():
    """
    Check get in tree

    test 1: random get key
    test 2: del key from 0 to 500, random get key from 501, 999
    """

    n = 1000
    tree = setup_tree(n)
    # test 1
    for i in range(100):
        t = randint(0, 999)
        assert tree[t] == t

    # test 2
    for i in range(500):
        del tree[i]
    for i in range(100):
        t = randint(501, 999)
        assert tree[t] == t


def test_delete():
    """
    Check del element in tree

    test 1: del all element
    test 2: del root
    test 3: del left child root
    test 4: del right child root
    """
    n = 10000
    tree = setup_tree(n)

    # test 1
    for i in range(n):
        del tree[i]
    assert len(tree) == 0

    # test 2
    for i in range(1, 4):
        tree[i] = i
    del tree[2]
    assert tree.root.key == 3

    # test 3
    tree[2] = 2
    del tree[1]
    assert tree.root.key == 2
    assert tree.root.left is None
    assert tree.root.right.key == 3

    # test 4
    tree[1] = 1
    del tree[3]
    assert tree.root.key == 2
    assert tree.root.right is None
    assert tree.root.left.key == 1


def test_bin_search_tree():
    """
    Validate for the validity of a binary search tree.

    test 1: Validation on insertion
    test 2: Validation on delete
    """

    n = 10000
    tree = setup_tree(n)
    min_key = - math.inf
    max_key = math.inf

    def check(node, min_key, max_key):
        if node is None:
            return True
        if min_key < node.key < max_key:
            return check(node.left, min_key, node.key) and check(node.right, node.key, max_key)
        return False

    # test 1
    assert check(tree.root, min_key, max_key)

    # test 2
    for i in range(0, 5000):
        del tree[i]
    assert check(tree.root, min_key, max_key)

def test_errors():
    """
    Check for raising exceptions

    test 1: void insert
    test 2: incomplete implementation
    test 3: delete void
    test 4: delete element not in tree
    """
    tree = setup_tree(0)

    # test 1
    with pytest.raises(TypeError):
        tree.insert()

    # test 2
    with pytest.raises(TypeError):
        tree.insert(1, )

    # test 3
    with pytest.raises(TypeError):
        tree.delete()

    # test 4
    with pytest.raises(KeyError):
        tree.delete(6)
