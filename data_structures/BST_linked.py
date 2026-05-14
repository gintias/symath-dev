"""
-------------------------------------------------------
Linked version of the BST ADT.
-------------------------------------------------------
"""
from copy import deepcopy


class _BST_Node:

    def __init__(self, value):
        """
        -------------------------------------------------------
        Initializes a BST node containing value. Child pointers 
        are None, height is 1.
        Use: node = _BST_Node(value)
        -------------------------------------------------------
        Parameters:
            value - value for the node (?)
        Returns:
            A _BST_Node object (_BST_Node)            
        -------------------------------------------------------
        """
        self._value = deepcopy(value)
        self._left = None
        self._right = None
        self._height = 1
        self._count = 0

    def _update_height(self):
        """
        -------------------------------------------------------
        Updates the height of the current node.
        Use: node._update_height()
        -------------------------------------------------------
        Returns:
            _height is 1 plus the maximum of the node's two children.
        -------------------------------------------------------
        """
        if self._left is None:
            left_height = 0
        else:
            left_height = self._left._height

        if self._right is None:
            right_height = 0
        else:
            right_height = self._right._height
        self._height = max(left_height, right_height) + 1
        return

    def __str__(self):
        """
        USE FOR TESTING ONLY
        -------------------------------------------------------
        Returns node height and value as a string - for debugging.
        -------------------------------------------------------
        """
        return "h: {}, v: {}".format(self._height, self._value)


class BST:

    def __init__(self):
        """
        -------------------------------------------------------
        Initializes an empty BST.
        Use: bst = BST()
        -------------------------------------------------------
        Returns:
            A BST object (BST)
        -------------------------------------------------------
        """
        self._root = None
        self._count = 0

    def is_empty(self):
        """
        -------------------------------------------------------
        Determines if bst is empty.
        Use: b = bst.is_empty()
        -------------------------------------------------------
        Returns:
            True if bst is empty, False otherwise.
        -------------------------------------------------------
        """
        # your code here
        return self._root is None

    def __len__(self):
        """
        -------------------------------------------------------
        Returns the number of nodes in the BST.
        Use: n = len(bst)
        -------------------------------------------------------
        Returns:
            the number of nodes in the BST.
        -------------------------------------------------------
        """
        # your code here
        return self._count

    def insert(self, value):
        """
        -------------------------------------------------------
        Inserts a copy of value into the bst. Values may appear 
        only once in a tree.
        Use: b = bst.insert(value)
        -------------------------------------------------------
        Parameters:
            value - data to be inserted into the bst (?)
        Returns:
            inserted - True if value is inserted into the BST,
                False otherwise. (boolean)
        -------------------------------------------------------
        """
        self._root, inserted = self._insert_aux(self._root, value)
        return inserted

    def _insert_aux(self, node, value):

        if node is None:
            self._count += 1
            node = _BST_Node(value)
            inserted = True

        elif node._value == value:
            inserted = False

        else:
            if value > node._value:
                node._right, inserted = self._insert_aux(node._right, value)

            elif value < node._value:
                node._left, inserted = self._insert_aux(node._left, value)

        if inserted:
            node._update_height()
        return node, inserted

    def retrieve(self, key):
        """
        -------------------------------------------------------
        Retrieves a copy of a value matching key in a BST. (Iterative)
        Use: v = bst.retrieve(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            value - value in the node containing key, otherwise None (?)
        -------------------------------------------------------
        """
        found = False
        node = self._root
        while node is not None and not found:
            if node._value == key:
                found = True
                value = deepcopy(node._value)
            else:
                if key > node._value:
                    node = node._right
                elif key < node._value:
                    node = node._left
        if not found:
            value = None
        return value

    def remove(self, key):
        """
        -------------------------------------------------------
        Removes a node with a value matching key from the bst.
        Returns the value matched. Updates structure of bst as 
        required.
        Use: value = bst.remove(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            value - value matching key if found, otherwise None.
        -------------------------------------------------------
        """
        self._root, value = self._remove_aux(self._root, key)
        return value

    def _remove_aux(self, node, key):
        if node is None:
            value = None

        elif node._value == key:
            value = node._value

            if node._left is not None and node._right is not None:

                if node._left._right is None:
                    rep_node = node._left
                else:
                    rep_node = self._delete_node_left(node)
                    rep_node._left = node._left

                rep_node._right = node._right
                node = rep_node

            elif node._left is not None:
                node = node._left
            elif node._right is not None:
                node = node._right
            else:
                node = None

            self._count -= 1

        else:
            if key > node._value:
                node._right, value = self._remove_aux(node._right, key)
            elif key < node._value:
                node._left, value = self._remove_aux(node._left, key)

        if node is not None and value is not None:
            node._update_height()

        return node, value

    def _delete_node_left(self, parent):
        """
        -------------------------------------------------------
        Finds a replacement node for a node to be removed from the tree.
        Private operation called only by _remove_aux.
        Use: repl_node = self._delete_node_left(node, node._right)
        -------------------------------------------------------
        Parameters:
            parent - node to search for largest value (_BST_Node)
        Returns:
            rep_node - the node that replaces the deleted node. This node 
                is the node with the maximum value in the deleted node's left
                subtree (_BST_Node)
        -------------------------------------------------------
        """
        child = parent._right

        if child._right is None:
            rep_node = child
            parent._right = child._left

        else:
            rep_node = self._delete_node_left(child)

        parent._update_height()
        return rep_node

    def remove_root(self):
        """
        -------------------------------------------------------
        Removes the root node and returns its value.
        Use: value = bst._remove_root()
        -------------------------------------------------------
        Returns:
            value - value in root.
        -------------------------------------------------------
        """
        assert self._root is not None, "Cannot remove the room of an empty BST"

        value = self._root._value
        rep_node = self._delete_node_left(self._root)
        rep_node._right = self._root._right
        rep_node._left = self._root._left
        self._root = rep_node
        return value

    def __contains__(self, key):
        """
        ---------------------------------------------------------
        Determines if the bst contains key.
        Use: b = key in bst
        -------------------------------------------------------
        Parameters:
            key - a comparable data element (?)
        Returns:
            True if the bst contains key, False otherwise.
        -------------------------------------------------------
        """
        contains = self._contains_aux(self._root, key)
        return contains

    def _contains_aux(self, node, key):
        if node is not None:
            if node._value == key:
                contains = True
            elif key > node._value:
                contains = self._contains_aux(node._right, key)
            elif key < node._value:
                contains = self._contains_aux(node._left, key)
        else:
            contains = False

        return contains

    def height(self):
        """
        -------------------------------------------------------
        Returns the maximum height of a BST, i.e. the length of the
        largest path from root to a leaf node in the tree.
        Use: h = bst.height()
        -------------------------------------------------------
        Returns:
            maximum height of bst (int)
        -------------------------------------------------------
        """
        if self._root is None:
            max_height = 0
        else:
            max_height = self._root._height

        return max_height

    def print_tree(self) -> None:
        """
        -------------------------------------------------------
        Prints the BST sideways, with the root at the left.
        Right children appear above their parent, and left children
        appear below their parent.
        Use: bst.print_tree()
        -------------------------------------------------------
        """
        if self._root is None:
            print("<empty>")
        else:
            self._print_tree_aux(self._root, 0)

    def _print_tree_aux(self, node, depth: int) -> None:
        if node is not None:
            self._print_tree_aux(node._right, depth + 1)
            print("    " * depth + str(node._value))
            self._print_tree_aux(node._left, depth + 1)

    def print_tree_top_down(self) -> None:
        """
        -------------------------------------------------------
        Prints the BST top-down, with the root centered above
        its children.
        Use: bst.print_tree_top_down()
        -------------------------------------------------------
        """
        if self._root is None:
            print("<empty>")
        else:
            height = self.height()
            node_width = max(len(str(value)) for value in self)

            if node_width % 2 == 0:
                node_width += 1

            level = [self._root]

            for depth in range(height):
                first_spacing = (2 ** (height - depth - 1) - 1) * node_width
                between_spacing = (2 ** (height - depth) - 1) * node_width
                line = " " * first_spacing
                next_level = []

                for node in level:
                    if node is None:
                        line += " " * node_width
                        next_level.extend([None, None])
                    else:
                        line += str(node._value).center(node_width)
                        next_level.extend([node._left, node._right])

                    line += " " * between_spacing

                print(line.rstrip())
                level = next_level

    def __eq__(self, target):
        """
        ---------------------------------------------------------
        Determines whether two BSTs are equal.
        Values in self and target are compared and if all values are equal
        and in the same location, returns True, otherwise returns False.
        Use: equals = source == target
        ---------------
        Parameters:
            target - a bst (BST)
        Returns:
            equals - True if source contains the same values
                as target in the same location, otherwise False. (boolean)
        -------------------------------------------------------
        """
        if not isinstance(target, BST):
            return NotImplemented

        equals = self._eq_aux(self._root, target._root)
        return equals

    def _eq_aux(self, s_node, t_node):
        if s_node is None and t_node is None:
            equals = True

        elif s_node is not None and t_node is None:
            equals = False

        elif s_node is None and t_node is not None:
            equals = False
        else:
            equals = s_node._value == t_node._value
            if equals:
                equals = self._eq_aux(s_node._left, t_node._left)
            if equals:
                equals = self._eq_aux(s_node._right, t_node._right)
        return equals

    def parent_r(self, key):
        """
        ---------------------------------------------------------
        Returns the value of the parent node of a key node in a bst.
        ---------------------------------------------------------
        Parameters:
            key - a key value (?)
        Returns:
            value - a copy of the value in a node that is the parent of the
            key node, None if the key is not found. (?)
        ---------------------------------------------------------
        """
        assert self._root is not None, "Cannot locate a parent in an empty BST"

        value = self._parent_r_aux(None, self._root, key)
        return value

    def _parent_r_aux(self, parent, node, key):
        if node is None:
            value = None

        elif node._value == key:
            if parent is None:
                value = None
            else:
                value = parent._value

        else:
            if key > node._value:
                value = self._parent_r_aux(node, node._right, key)
            elif key < node._value:
                value = self._parent_r_aux(node, node._left, key)

        return value

    def parent(self, key):
        """
        ---------------------------------------------------------
        Returns the value of the parent node in a bst given a key.
        ---------------------------------------------------------
        Parameters:
            key - a key value (?)
        Returns:
            value - a copy of the value in a node that is the parent of the
            key node, None if the key is not found.
        ---------------------------------------------------------
        """
        assert self._root is not None, "Cannot locate a parent in an empty BST"

        parent = None
        child = self._root
        found = False

        while child is not None and not found:
            if child._value == key:
                if parent is None:
                    value = None
                else:
                    value = deepcopy(parent._value)
                found = True
            else:
                parent = child
                if key > child._value:
                    child = child._right
                else:
                    child = child._left
        if not found:
            value = None
        return value

    def max(self):
        """
        -------------------------------------------------------
        Finds the maximum value in BST. (Iterative algorithm)
        Use: value = bst.max()
        -------------------------------------------------------
        Returns:
            value - a copy of the maximum value in the BST (?)
        -------------------------------------------------------
        """
        assert self._root is not None, "Cannot find maximum of an empty BST"

        node = self._root

        while node._right is not None:
            node = node._right

        value = deepcopy(node._value)

        return value

    def max_r(self):
        """
        ---------------------------------------------------------
        Returns the largest value in a bst. (Recursive algorithm)
        Use: value = bst.max_r()
        ---------------------------------------------------------
        Returns:
            value - a copy of the maximum value in the BST (?)
        ---------------------------------------------------------
        """
        assert self._root is not None, "Cannot find maximum of an empty BST"

        value = self._max_r_aux(self._root)
        return value

    def _max_r_aux(self, node):
        if node._right is None:
            value = deepcopy(node._value)
        else:
            value = self._max_r_aux(node._right)
        return value

    def min(self):
        """
        -------------------------------------------------------
        Finds the minimum value in BST. (Iterative algorithm)
        Use: value = bst.min()
        -------------------------------------------------------
        Returns:
            value - a copy of the minimum value in the BST (?)
        -------------------------------------------------------
        """
        assert self._root is not None, "Cannot find minimum of an empty BST"

        node = self._root
        while node._left is not None:
            node = node._left
        value = deepcopy(node._value)
        return value

    def min_r(self):
        """
        ---------------------------------------------------------
        Returns the minimum value in a bst. (Recursive algorithm)
        Use: value = bst.min_r()
        ---------------------------------------------------------
        Returns:
            value - a copy of the minimum value in the BST (?)
        ---------------------------------------------------------
        """
        assert self._root is not None, "Cannot find minimum of an empty BST"

        value = self._min_r_aux(self._root)
        return value

    def _min_r_aux(self, node):
        if node._left is None:
            value = deepcopy(node._value)
        else:
            value = self._min_r_aux(node._left)
        return value

    def leaf_count(self):
        """
        ---------------------------------------------------------
        Returns the number of leaves (nodes with no children) in bst.
        Use: n = bst.leaf_count()
        (Recursive algorithm)
        ---------------------------------------------------------
        Returns:
            count - number of nodes with no children in bst (int)
        ---------------------------------------------------------
        """
        count = self._leaf_count_aux(self._root)
        return count

    def _leaf_count_aux(self, node):
        if node is None:
            count = 0
        elif node._left is None and node._right is None:
            count = 1
        else:
            count = 0
            if node._right is not None:
                count += self._leaf_count_aux(node._right)
            if node._left is not None:
                count += self._leaf_count_aux(node._left)
        return count

    def two_child_count(self):
        """
        ---------------------------------------------------------
        Returns the number of the three types of nodes in a BST.
        Use: count = bst.two_child_count()
        -------------------------------------------------------
        Returns:
            count - number of nodes with two children in bst (int)
        ----------------------------------------------------------
        """
        count = self._two_child_count_aux(self._root)
        return count

    def _two_child_count_aux(self, node):
        if node is None:
            count = 0
        elif node._right is not None and node._left is not None:
            count = 1
            count += self._two_child_count_aux(node._right)
            count += self._two_child_count_aux(node._left)
        else:
            count = 0
            if node._right is not None:
                count += self._two_child_count_aux(node._right)
            if node._left is not None:
                count += self._two_child_count_aux(node._left)

        return count

    def one_child_count(self):
        """
        ---------------------------------------------------------
        Returns the number of the three types of nodes in a BST.
        Use: count = bst.one_child_count()
        -------------------------------------------------------
        Returns:
            count - number of nodes with one child in bst (int)
        ----------------------------------------------------------
        """
        count = self._one_child_count_aux(self._root)
        return count

    def _one_child_count_aux(self, node):
        if node is None:
            count = 0
        elif node._right is None and node._left is None:
            count = 0
        elif node._right is not None and node._left is None:
            count = 1
            count += self._one_child_count_aux(node._right)
        elif node._right is None and node._left is not None:
            count = 1
            count += self._one_child_count_aux(node._left)
        else:
            count = 0
            count += self._one_child_count_aux(node._left)
            count += self._one_child_count_aux(node._right)
        return count

    def node_counts(self):
        """
        ---------------------------------------------------------
        Returns the number of the three types of nodes in a BST.
        Use: zero, one, two = bst.node_counts()
        -------------------------------------------------------
        Returns:
            zero - number of nodes with zero children (int)
            one - number of nodes with one child (int)
            two - number of nodes with two children (int)
        ----------------------------------------------------------
        """
        zero = self._leaf_count_aux(self._root)
        one = self._one_child_count_aux(self._root)
        two = self._two_child_count_aux(self._root)
        return zero, one, two

    def is_balanced(self):
        """
        ---------------------------------------------------------
        Returns whether a bst is balanced, i.e. the difference in
        height between all the bst's node's left and right subtrees is <= 1.
        Use: b = bst.is_balanced()
        ---------------------------------------------------------
        Returns:
            balanced - True if the bst is balanced, False otherwise (boolean)
        ---------------------------------------------------------
        """
        balanced = self._is_balanced_aux(self._root)
        return balanced

    def _is_balanced_aux(self, node):
        if node is None:
            balanced = True
        else:
            if abs(self._node_height(node._right) - self._node_height(node._left)) > 1:
                balanced = False
            else:
                balanced = self._is_balanced_aux(node._left)
                if balanced:
                    balanced = self._is_balanced_aux(node._right)

        return balanced

    def _node_height(self, node):
        """
        ---------------------------------------------------------
        Helper function to determine the height of node - handles empty node.
        Private operation called only by _is_valid_aux.
        Use: h = self._node_height(node)
        ---------------------------------------------------------
        Parameters:
            node - the node to get the height of (_BST_Node)
        Returns:
            height - 0 if node is None, node._height otherwise (int)
        ---------------------------------------------------------
        """
        if node is None:
            height = 0
        else:
            height = node._height
        return height

    def retrieve_r(self, key):
        """
        -------------------------------------------------------
        Retrieves a _value in a BST. (Recursive)
        Use: v = bst.retrieve(key)
        -------------------------------------------------------
        Parameters:
            key - data to search for (?)
        Returns:
            value - If bst contains key, returns value, else returns None.
        -------------------------------------------------------
        """
        value = self._retrieve_r_aux(self._root, key)
        return value

    def _retrieve_r_aux(self, node, key):
        if node is None:
            value = None

        elif node._value == key:
            value = node._value
        else:
            if key > node._value:
                value = self._retrieve_r_aux(node._right, key)
            elif key < node._value:
                value = self._retrieve_r_aux(node._left, key)
        return value

    def is_valid(self):
        """
        ---------------------------------------------------------
        Determines if a tree is a is_valid BST, i.e. the values in all left nodes
        are smaller than their parent, and the values in all right nodes are
        larger than their parent, and height of any node is 1 + max height of
        its children.
        Use: b = bst.is_valid()
        ---------------------------------------------------------
        Returns:
            valid - True if tree is a BST, False otherwise (boolean)
        ---------------------------------------------------------
        """
        valid = self._is_valid_aux(self._root, None, None)
        return valid

    def _is_valid_aux(self, node, lower, upper):
        if node is None:
            valid = True
        elif lower is not None and node._value <= lower:
            valid = False
        elif upper is not None and node._value >= upper:
            valid = False
        elif self._node_height(node) != max(self._node_height(node._left), self._node_height(node._right)) + 1:
            valid = False
        else:
            valid = self._is_valid_aux(node._left, lower, node._value)
            if valid:
                valid = self._is_valid_aux(node._right, node._value, upper)

        return valid

    def inorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in inorder order.
        Use: a = bst.inorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in inorder (list of ?)
        -------------------------------------------------------
        """
        lst = []
        lst = self._inorder_aux(self._root, lst)
        return lst

    def _inorder_aux(self, node, lst):
        if node is not None:
            lst = self._inorder_aux(node._left, lst)
            lst.append(deepcopy(node._value))
            lst = self._inorder_aux(node._right, lst)
        return lst

    def preorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in preorder order.
        Use: a = bst.preorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in preorder (list of ?)
        -------------------------------------------------------
        """
        lst = []
        lst = self._preorder_aux(self._root, lst)
        return lst

    def _preorder_aux(self, node, lst):
        if node is not None:
            lst.append(node._value)
            lst = self._preorder_aux(node._left, lst)
            lst = self._preorder_aux(node._right, lst)

        return lst

    def postorder(self):
        """
        -------------------------------------------------------
        Generates a list of the contents of the tree in postorder order.
        Use: a = bst.postorder()
        -------------------------------------------------------
        Returns:
            a - copy of the contents of the tree in postorder (list of ?)
        -------------------------------------------------------
        """
        lst = []
        lst = self._postorder_aux(self._root, lst)
        return lst

    def _postorder_aux(self, node, lst):
        if node is not None:
            lst = self._postorder_aux(node._left, lst)
            lst = self._postorder_aux(node._right, lst)
            lst.append(node._value)
        return lst

    def levelorder(self):
        """
        -------------------------------------------------------
        Copies the contents of the tree in levelorder order to a list.
        Use: values = bst.levelorder()
        -------------------------------------------------------
        Returns:
            values - a list containing the values of bst in levelorder.
            (list of ?)
        -------------------------------------------------------
        """
        levelorder_lst = []
        q = []
        node = self._root

        if self._root is not None:
            q.append(self._root)

            while len(q) != 0:
                node = q.pop(0)
                levelorder_lst.append(node._value)

                if node._left is not None:
                    q.append(node._left)

                if node._right is not None:
                    q.append(node._right)

        return levelorder_lst

    def count(self):
        """
        ---------------------------------------------------------
        Returns the number of nodes in a BST.
        Use: number = bst.count()
        -------------------------------------------------------
        Returns:
            number - count of nodes in tree (int)
        ----------------------------------------------------------
        """
        count = self._count_aux(self._root)
        return count

    def _count_aux(self, node):
        if node is None:
            count = 0
        else:
            count = 1
            if node._left is not None:
                count += self._count_aux(node._left)
            if node._right is not None:
                count += self._count_aux(node._right)
        return count

    def __iter__(self):
        """
        -------------------------------------------------------
        Generates a Python iterator. Iterates through a BST node
        in level order.
        Use: for v in bst:
        -------------------------------------------------------
        Returns:
            yields
            value - the values in the BST node and its children (?)
        -------------------------------------------------------
        """
        if self._root is not None:
            # Put the nodes for one level into a queue.
            queue = []
            queue.append(self._root)

            while len(queue) > 0:
                # Add a copy of the data to the sublist
                node = queue.pop(0)
                yield node._value

                if node._left is not None:
                    queue.append(node._left)
                if node._right is not None:
                    queue.append(node._right)
