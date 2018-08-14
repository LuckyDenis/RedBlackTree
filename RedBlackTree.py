# -*- coding: utf8 -*-


class NodeTree:
    __slots__ = ['key', 'payload', 'parent', 'left', 'right', 'color']

    def __init__(self, key, payload, parent=None, left=None, right=None, color='Black'):
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

    def is_left_knot(self):
        return self.parent and self.parent.left == self

    def is_right_knot(self):
        return self.parent and self.parent.right == self

    def is_root(self):
        return not self.parent

    def has_leaf(self):
        return not(self.left or self.right)

    def has_any_children(self):
        return self.left or self.right

    def has_both_children(self):
        return self.left and self.right

    def replace_node_date(self, key, payload, left, right):
        self.key = key
        self.payload = payload
        self.left = left
        self.right = right
        if self.has_left_child():
            self.left.parent = self
        if self.has_right_child():
            self.right.parent = self

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
                if self.is_left_knot():
                    succ = self.parent
                else:
                    self.parent.right = None
                    succ = self.parent.find_successor()
                    self.parent.right = self
        return succ

    def splice_out(self):
        if self.has_leaf():
            if self.is_left_knot():
                self.parent.left = None
            else:
                self.parent.right = None
        elif self.has_any_children():
            if self.has_left_child():
                if self.is_left_knot():
                    self.parent.left = self.left
                else:
                    self.parent.right = self.left
                self.left.parent = self.parent
            else:
                if self.is_left_knot():
                    self.parent.left = self.right
                else:
                    self.parent.right = self.right
                self.right.parent = self.parent

    def __iter__(self):
        if self:
            if self.has_left_child():
                for element in self.left:
                    yield element
            yield self.key
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
        if self.parent:
            if self.parent.is_left_knot():
                return self.parent.parent.has_right_child()
            elif self.parent.is_right_knot():
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


class RedBlackTree:

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
        if key == curr_node.key:
            curr_node.payload = payload
        else:
            if key < curr_node.key:
                if curr_node.has_left_child():
                    self._insert(key, payload, curr_node.left)
                else:
                    curr_node.left = NodeTree(key, payload, parent=curr_node, color='Red')
                    self.size += 1
                    self._fix_insert(curr_node.left)
            else:
                if curr_node.has_right_child():
                    self._insert(key, payload, curr_node.right)
                else:
                    curr_node.right = NodeTree(key, payload, parent=curr_node, color='Red')
                    self.size += 1
                    self._fix_insert(curr_node.right)

    def _fix_insert(self, node):
        while node.get_parent_color() == 'Red':
            if node.parent.is_left_knot():
                if node.has_uncle():
                    if node.get_uncle_color() == 'Red':
                        node.set_parent_color('Black')
                        node.set_uncle_color('Black')
                        node.set_grandfather_color('Red')
                        node = node.get_grandfather()
                else:
                    if node.is_right_knot():
                        node = node.parent
                        self._left_rotate(node)
                    node.set_parent_color('Black')
                    node.set_grandfather_color('Red')
                    self._right_rotate(node.get_grandfather())
            else:
                if node.has_uncle():
                    if node.get_uncle_color() == 'Red':
                        node.set_parent_color('Black')
                        node.set_uncle_color('Black')
                        node.set_grandfather_color('Red')
                        node = node.get_grandfather()
                else:
                    if node.is_left_knot():
                        node = node.parent
                        self._right_rotate(node)
                    node.set_parent_color('Black')
                    node.set_grandfather_color('Red')
                    self._left_rotate(node.get_grandfather())
        self.root.color = 'Black'

    def _left_rotate(self, rot_node):
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

    def __setitem__(self, key, payload):
        self.insert(key, payload)

    def __iter__(self):
        return self.root.__iter__()

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
                return None
        else:
            return None

    def _delete(self, node):
        if node.has_leaf():
            if node.is_left_knot():
                node.parent.left = None
            else:
                node.parent.right = None
        elif node.has_both_children():
            succ = node.find_successor()
            succ.splice_out()
            node.key = succ.key
            node.payload = succ.payload
            self._fix_delete(succ.parent)
        else:
            if node.has_any_children():
                if node.has_left_child():
                    if node.is_left_knot():
                        node.parent.left = node.left
                        node.left.parent = node.parent
                        self._fix_delete(node.parent)
                    elif node.is_right_knot():
                        node.parent.right = node.left
                        node.left.parent = node.parent
                        self._fix_delete(node.parent)
                    else:
                        node.replace_node_date(node.left.key,
                                               node.left.payload,
                                               node.left.left,
                                               node.left.right)
                        self._fix_delete(node)
                else:
                    if node.is_left_knot():
                        node.parent.left = node.right
                        node.right.parent = node.parent
                        self._fix_delete(node.parent)
                    elif node.is_right_knot():
                        node.parent.right = node.right
                        node.right.parent = node.parent
                        self._fix_delete(node.parent)
                    else:
                        node.replace_node_date(node.right.key,
                                               node.right.payload,
                                               node.right.left,
                                               node.right.right)
                        self._fix_delete(node)

    def delete(self, key):
        if self.size > 1:
            remove_node = self._get(key, self.root)
            if remove_node:
                self._delete(remove_node)
                self.size -= 1
            else:
                raise KeyError('key not in tree.')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise ValueError('tree is empty.')

    def __delitem__(self, key):
        self.delete(key)

    def _fix_delete(self, node):
        while not node.is_root() and node.color == 'Black':
            if node.is_left_knot():
                if node.has_right_brother():
                    brother = node.parent.right
                    if brother.color == 'Red':
                        brother.color = 'Black'
                        node.parent.color = 'Red'
                        self._left_rotate(node.parent)
                    if brother.has_both_children():
                        if brother.right.color == 'Black':
                            if brother.left.color == 'Black':
                                brother.color = 'Red'
                            else:
                                brother.left.color = 'Black'
                                brother.color = 'Red'
                                self._right_rotate(brother)
                            brother.color = node.parent.color
                            node.parent.color = 'Black'
                            self._left_rotate(node.parent)
                node = self.root
            else:
                if node.has_left_brother():
                    brother = node.parent.left
                    if brother.color == 'Red':
                        brother.color = 'Black'
                        node.parent.color = 'Red'
                        self._right_rotate(node.parent)
                    if brother.has_both_children():
                        if brother.left.color == 'Black':
                            if brother.right.color == 'Black':
                                brother.color = 'Red'
                            else:
                                brother.right.color = 'Black'
                                brother.color = 'Red'
                                self._right_rotate(brother)
                            brother.color = node.parent.color
                            node.parent.color = 'Black'
                            self._right_rotate(node.parent)
                node = self.root

    def __getitem__(self, key):
        return self.get(key)
