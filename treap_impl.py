#!/usr/bin/env python3
"""Treap — randomized BST with heap priorities."""
import sys, random

class Node:
    def __init__(self, key, pri=None):
        self.key, self.pri = key, pri or random.random()
        self.left = self.right = None

class Treap:
    def __init__(self): self.root = None
    def _rot_right(self, n):
        t = n.left; n.left = t.right; t.right = n; return t
    def _rot_left(self, n):
        t = n.right; n.right = t.left; t.left = n; return t
    def _insert(self, n, key):
        if not n: return Node(key)
        if key < n.key:
            n.left = self._insert(n.left, key)
            if n.left.pri > n.pri: n = self._rot_right(n)
        elif key > n.key:
            n.right = self._insert(n.right, key)
            if n.right.pri > n.pri: n = self._rot_left(n)
        return n
    def _delete(self, n, key):
        if not n: return None
        if key < n.key: n.left = self._delete(n.left, key)
        elif key > n.key: n.right = self._delete(n.right, key)
        else:
            if not n.left: return n.right
            if not n.right: return n.left
            if n.left.pri > n.right.pri:
                n = self._rot_right(n); n.right = self._delete(n.right, key)
            else:
                n = self._rot_left(n); n.left = self._delete(n.left, key)
        return n
    def insert(self, key): self.root = self._insert(self.root, key)
    def delete(self, key): self.root = self._delete(self.root, key)
    def search(self, key):
        n = self.root
        while n:
            if key == n.key: return True
            n = n.left if key < n.key else n.right
        return False
    def inorder(self):
        res = []; stack = []; n = self.root
        while stack or n:
            while n: stack.append(n); n = n.left
            n = stack.pop(); res.append(n.key); n = n.right
        return res

def main():
    t = Treap()
    for x in [5,3,8,1,4,7,9]: t.insert(x)
    print(f"Inorder: {t.inorder()}")
    print(f"Search 4: {t.search(4)}, Search 6: {t.search(6)}")
    t.delete(3); print(f"After delete 3: {t.inorder()}")

if __name__ == "__main__": main()
