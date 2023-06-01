"""
File: linkedbst.py
Author: Ken Lambert
"""

import time
from math import log
from random import sample, shuffle
from abstractcollection import AbstractCollection
from bstnode import BSTNode

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            strng = ""
            if node != None:
                strng += recurse(node.right, level + 1)
                strng += "| " * level
                strng += str(node.data) + "\n"
                strng += recurse(node.left, level + 1)
            return strng

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    # def inorder(self):
    #     """Supports an inorder traversal on a view of self."""
    #     lyst = list()

    #     def recurse(node):
    #         if node != None:
    #             recurse(node.left)
    #             lyst.append(node.data)
    #             recurse(node.right)

    #     recurse(self._root)
    #     return iter(lyst)

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []
        stack = []
        current = self._root

        while current is not None or stack:
            while current is not None:
                stack.append(current)
                current = current.left

            current = stack.pop()
            lyst.append(current.data)
            current = current.right

        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the matched item, or None otherwise."""
        current = self._root
        while current is not None:
            if item == current.data:
                return current.data
            elif item < current.data:
                current = current.left
            else:
                current = current.right
        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return

        current = self._root
        while True:
            if item < current.data:
                if current.left is None:
                    current.left = BSTNode(item)
                    self._size += 1
                    return
                else:
                    current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(item)
                    self._size += 1
                    return
                else:
                    current = current.right


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, top=None):
        """
        Return the height of the tree.
        :param top: Node (optional)
        :return: int
        """
        def height1(node):
            if node is None:
                return 0
            else:
                return 1 + max(height1(node.left), height1(node.right))

        if top is None:
            top = self._root

        return height1(top) - 1


    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        if self.height() < (2 * log(self._size+1) - 1):
            return True
        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = list(self.inorder())
        #Обхід симетричний
        return lst[lst.index(low):lst.index(high)+1]


    def rebalance(self):
        '''
        rebalance
        '''
        nodes = list(self.inorder())
        self.clear()

        def rebalance1(nodes=None, sort=False):
            if nodes is None and sort is False:
                nodes = list(self)
                nodes.sort()
                return rebalance1(nodes, True)
            elif nodes:
                medium = len(nodes) // 2
                root = BSTNode(nodes[medium])
                if self._root is None:
                    self._root = root
                root.left = rebalance1(nodes[:medium], True)
                root.right = rebalance1(nodes[medium + 1:], True)
                self._size += 1
                return root
            else:
                return None
        rebalance1(nodes)



    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        #12345-4
        listie = sorted(list(self.inorder()))
        try:
            element = listie[listie.index(item)+1]
            return element
        except IndexError:
            return None
        except ValueError:
            lst = [i for i in listie if i > item]
            return lst[0]

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        #12345-2
        listie = sorted(list(self.inorder()))
        if not listie:
            return None
        lst = [i for i in listie if i<item]
        if lst:
            return max(lst)
        return None

    @classmethod
    def read_file(cls, path):
        '''Reads file'''
        with open(path, 'r', encoding = 'utf-8') as file:
            read = [i.strip() for i in file.readlines()]
            return read

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        dct_srt = LinkedBST.read_file(path)
        dct_not_srt = LinkedBST.read_file(path)
        shuffle(dct_not_srt)
        words = sample(dct_srt, 1000)
        sort_bst = LinkedBST(dct_srt[:20000])
        not_sort_bst = LinkedBST(dct_not_srt[:20000])

        #Час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику
        #(пошук у списку слів з використанням методів вбудованого типу list)
        print('\n')
        print('Час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику:')
        start = time.time()
        for i in words:
            dct_srt.index(i)
        end = time.time()
        print(f'{end-start} c.')

        #Час пошуку 10000 випадкових слів у словнику, який представлений \
        #у вигляді бінарного дерева пошуку(словник впорядкований за абеткою)
        print('\n')
        print('Час пошуку 10000 випадкових слів у словнику, який представлений \
у вигляді бінарного дерева пошуку(словник впорядкований за абеткою):')
        start = time.time()
        for i in words:
            sort_bst.find(i)
        end = time.time()
        print(f'{end-start} c.')

        #Час пошуку 10000 випадкових слів у словнику, який представлений у
        #вигляді бінарного дерева пошуку(словник не впорядкований за абеткою)
        print('\n')
        print('Час пошуку 10000 випадкових слів у словнику, який представлений \
у вигляді бінарного дерева пошуку(словник не впорядкований за абеткою):')
        start = time.time()
        for i in words:
            not_sort_bst.find(i)
        end = time.time()
        print(f'{end-start} c.')

        #Час пошуку 10000 випадкових слів у словнику, який представлений у
        #вигляді бінарного дерева пошуку після його балансування.
        print('\n')
        print('Час пошуку 10000 випадкових слів у словнику, який представлений у\
 вигляді бінарного дерева пошуку після його балансування:')
        sort_bst.rebalance()
        start = time.time()
        for i in words:
            sort_bst.find(i)
        end = time.time()
        print(f'{end-start} c.')

if __name__ == '__main__':
    LinkedBST().demo_bst('words.txt')
