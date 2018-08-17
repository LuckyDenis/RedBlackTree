# -*- coding: utf8 -*-


class NodeTree(object):
    __slots__ = ['key', 'payload', 'parent', 'left', 'right', 'color']

    def __init__(self, key, payload, parent=None, left=None, right=None, color='Red'):
        self.key = key
        self.payload = payload
        self.parent = parent
        self.left = left
        self.right = right
        self.color = color

    def has_left_child(self):
        return self.left

    def has_right_child(self):
        return self.right

    # node.parent.left == node
    def is_left_knot(self):
        return self.parent and self.parent.left == self

    # node.parent.right == node
    def is_right_knot(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    def has_leaf(self):
        return not (self.left or self.right)

    def has_any_children(self):
        return self.left or self.right

    def has_both_children(self):
        return self.left and self.right

    # swap node with left or right child
    def replace_node_date(self, key, payload, left, right):
        self.key = key
        self.payload = payload
        self.left = left
        self.right = right
        if self.has_left_child():
            self.left.parent = self
        if self.has_right_child():
            self.right.parent = self

    # looking for the bottom left node
    def find_min(self):
        curr = self
        while curr.has_left_child():
            curr = curr.left
        return curr

    def find_successor(self):
        succ = None
        if self.has_right_child():
            succ = self.right.find_min()
        else:
            if self.parent:
                # node.parent.left == node
                if self.is_left_knot():
                    succ = self.parent
                # node.parent.right == node
                else:
                    # we say that we are not
                    self.parent.right = None
                    # looking for a parent now
                    succ = self.parent.find_successor()
                    # come back
                    self.parent.right = self
        return succ

    # cut node
    def splice_out(self):
        if self.has_leaf():
            # node.parent.left == node
            if self.is_left_knot():
                self.parent.left = None
            # node.parent.right == node
            else:
                self.parent.right = None
        elif self.has_any_children():
            if self.has_left_child():
                # node.parent.left == node
                if self.is_left_knot():
                    self.parent.left = self.left
                # node.parent.right == node
                else:
                    self.parent.right = self.left
                self.left.parent = self.parent
            else:
                # node.parent.left == node
                if self.is_left_knot():
                    self.parent.left = self.right
                # node.parent.right == node
                else:
                    self.parent.right = self.right
                self.right.parent = self.parent

    def __iter__(self):
        if self:
            if self.has_left_child():
                for element in self.left:
                    yield element
            yield self.key, self.color
            if self.has_right_child():
                for element in self.right:
                    yield element

    def get_grandfather(self):
        return self.parent.parent

    def get_grandfather_color(self):
        return self.parent.parent.color

    def set_grandfather_color(self, color):
        self.parent.parent.color = color

    def has_uncle(self):
        if self.parent.parent:
            # node.parent.parent.left == node.parent
            if self.parent.is_left_knot():
                # return node.parent.parent.right
                return self.parent.parent.has_right_child()
            # node.parent.parent.right == node.parent
            elif self.parent.is_right_knot():
                # return node.parent.parent.left
                return self.parent.parent.has_left_child()

    def get_uncle_color(self):
        if self.has_uncle():
            if self.parent.is_left_knot():
                return self.parent.parent.right.color
            else:
                return self.parent.parent.left.color

    def set_uncle_color(self, color):
        if self.has_uncle():
            if self.parent.is_left_knot():
                self.parent.parent.right.color = color
            else:
                self.parent.parent.left.color = color

    def get_parent_color(self):
        if self.parent:
            return self.parent.color

    def set_parent_color(self, color):
        if self.parent:
            self.parent.color = color

    def has_left_brother(self):
        if self.parent:
            return self.parent.left != self and self.parent.left is not None

    def has_right_brother(self):
        if self.parent:
            return self.parent.right != self and self.parent.right is not None

    def get_brother_color(self):
        if self.has_right_brother():
            return self.parent.right.color
        if self.has_left_brother():
            return self.parent.left.color

    def set_brother_color(self, color):
        if self.has_right_brother():
            self.parent.right.color = color
        if self.has_left_brother():
            self.parent.left.color = color

    def brother_has_both_children(self):
        if self.has_right_brother():
            return self.parent.right.has_both_children()
        if self.has_left_brother():
            return self.parent.left.has_both_children()


class RedBlackTree(object):

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, key, payload):
        if self.root:
            self._insert(key, payload, self.root)
        else:
            self.root = NodeTree(key, payload, color='Black')
            self.size += 1

    def _insert(self, key, payload, curr_node):
        # ban on the insertion of identical keys
        if key == curr_node.key:
            curr_node.payload = payload

        # recursive search for the node insertion point
        else:
            # go to the left
            if key < curr_node.key:
                # node.left is not None
                if curr_node.has_left_child():
                    self._insert(key, payload, curr_node.left)
                # node.left is None, insert
                else:
                    curr_node.left = NodeTree(key, payload, parent=curr_node, color='Red')
                    self.size += 1
                    self._fix_insert(curr_node.left)

            # go to the right
            else:
                # node.right is not None
                if curr_node.has_right_child():
                    self._insert(key, payload, curr_node.right)
                # node.right is None, insert
                else:
                    curr_node.right = NodeTree(key, payload, parent=curr_node, color='Red')
                    self.size += 1
                    self._fix_insert(curr_node.right)

    def _fix_insert(self, node):
        while node.get_parent_color() == 'Red':
            # node.parent.parent.left == node.parent
            if node.parent.is_left_knot():
                # The case when the father and uncle are red
                if node.get_uncle_color() == 'Red':
                    node.set_parent_color('Black')
                    node.set_uncle_color('Black')
                    node.set_grandfather_color('Red')
                    node = node.get_grandfather()
                # the case when the father is red but there is no uncle
                else:
                    if node.is_right_knot():
                        node = node.parent
                        self._left_rotate(node)
                    node.set_parent_color('Black')
                    node.set_grandfather_color('Red')
                    self._right_rotate(node.get_grandfather())

            # node.parent.parent.right == node.parent
            else:
                # The case when the father and uncle are red
                if node.get_uncle_color() == 'Red':
                    node.set_parent_color('Black')
                    node.set_uncle_color('Black')
                    node.set_grandfather_color('Red')
                    node = node.get_grandfather()
                # the case when the father is red but there is no uncle
                else:
                    if node.is_left_knot():
                        node = node.parent
                        self._right_rotate(node)
                    node.set_parent_color('Black')
                    node.set_grandfather_color('Red')
                    self._left_rotate(node.get_grandfather())
        self.root.color = 'Black'

    def _left_rotate(self, rot_node):
        # rot_node.right = rot_node.right.left
        new_node = rot_node.right
        rot_node.right = new_node.left
        if new_node.has_left_child():
            new_node.left.parent = rot_node
        new_node.parent = rot_node.parent
        if rot_node.is_root():
            self.root = new_node
            new_node.parent = None
        else:
            if rot_node.is_left_knot():
                rot_node.parent.left = new_node
            else:
                rot_node.parent.right = new_node
        new_node.left = rot_node
        rot_node.parent = new_node

    def _right_rotate(self, rot_node):
        # rot_node.left = rot_node.left.right
        new_node = rot_node.left
        rot_node.left = new_node.right
        if new_node.has_right_child():
            new_node.right.parent = rot_node
        new_node.parent = rot_node.parent
        if rot_node.is_root():
            self.root = new_node
            new_node.parent = None
        else:
            if rot_node.is_left_knot():
                rot_node.parent.left = new_node
            else:
                rot_node.parent.right = new_node
        new_node.right = rot_node
        rot_node.parent = new_node

    def _get(self, key, curr_node):
        if not curr_node:
            return None
        elif key == curr_node.key:
            return curr_node
        elif key < curr_node.key:
            return self._get(key, curr_node.left)
        else:
            return self._get(key, curr_node.right)

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None  # can be replaced with raise KeyError()
        else:
            return None  # can be replaced with raise KeyError()

    def _delete(self, node):
        # node.left is None and node.right is None
        if node.has_leaf():
            if node.is_left_knot():
                node.parent.left = None
            else:
                node.parent.right = None
        # node.left is not None and node.right is not None
        elif node.has_both_children():
            succ = node.find_successor()
            succ.splice_out()
            node.key = succ.key
            node.payload = succ.payload
        # node.left is not None or node.right is not None
        else:
            if node.has_any_children():
                # node.left is not None
                if node.has_left_child():
                    # node.parent.left == node
                    if node.is_left_knot():
                        node.parent.left = node.left
                        node.left.parent = node.parent
                    # node.parent.right == node
                    elif node.is_right_knot():
                        node.parent.right = node.left
                        node.left.parent = node.parent
                    # node is root, swap left child
                    else:
                        node.replace_node_date(node.left.key,
                                               node.left.payload,
                                               node.left.left,
                                               node.left.right)
                # node.right is not None
                else:
                    # node.parent.left == node
                    if node.is_left_knot():
                        node.parent.left = node.right
                        node.right.parent = node.parent
                    # node.parent.right == node
                    elif node.is_right_knot():
                        node.parent.right = node.right
                        node.right.parent = node.parent
                    # node is root, swap right child
                    else:
                        node.replace_node_date(node.right.key,
                                               node.right.payload,
                                               node.right.left,
                                               node.right.right)

    def delete(self, key):
        if self.size > 1:
            remove_node = self._get(key, self.root)
            if remove_node:
                self._delete(remove_node)
                # if the black balance is deleted, the balance may be violated
                if remove_node.color == 'Black':
                    self._fix_delete(remove_node)
                self.size -= 1
            else:
                raise KeyError('key not in tree.')
        # there is only a root
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('tree is empty.')

    def _fix_delete(self, node):
        while not node.is_root() and node.color == 'Black':
            # node.parent.right is not None and node.parent.right != node
            if node.has_right_brother():
                brother = node.parent.right
                if brother.color == 'Red':
                    brother.color = 'Black'
                    node.parent.color = 'Red'
                    self._left_rotate(node.parent)
                # node.parent.right has both children
                if brother.has_both_children():
                    # brother.right is Black
                    if brother.right.color == 'Black':
                        # brother.left is Black
                        if brother.left.color == 'Black':
                            brother.color = 'Red'
                        # brother.left is not Black
                        else:
                            brother.left.color = 'Black'
                            brother.color = 'Red'
                            self._right_rotate(brother)
                        brother.color = node.parent.color
                        node.parent.color = 'Black'
                        self._left_rotate(node.parent)
                node = self.root
            # node.parent.left is not None and node.parent.left != node
            if node.has_left_brother():
                brother = node.parent.left
                if brother.color == 'Red':
                    brother.color = 'Black'
                    node.parent.color = 'Red'
                    self._right_rotate(node.parent)
                # node.parent.left has both children
                if brother.has_both_children():
                    # brother.left is Black
                    if brother.left.color == 'Black':
                        # brother.right is Black
                        if brother.right.color == 'Black':
                            brother.color = 'Red'
                        # brother.right is not Black
                        else:
                            brother.right.color = 'Black'
                            brother.color = 'Red'
                            self._right_rotate(brother)
                        brother.color = node.parent.color
                        node.parent.color = 'Black'
                        self._right_rotate(node.parent)
                node = self.root

    def clear_tree(self):
        self.root = None
        self.size = 0

    def __len__(self):
        return self.size

    def __getitem__(self, key):
        return self.get(key)

    def __delitem__(self, key):
        self.delete(key)

    def __setitem__(self, key, payload):
        self.insert(key, payload)

    def __iter__(self):
        if self.root:
            return self.root.__iter__()
        return iter([])
