#!/usr/bin/env python3
"""Treap (tree + heap) — zero-dep."""
import random

class TreapNode:
    def __init__(self, key, priority=None):
        self.key=key; self.priority=priority or random.random()
        self.left=self.right=None; self.size=1

def size(n): return n.size if n else 0
def update(n):
    if n: n.size=1+size(n.left)+size(n.right)

def split(node, key):
    if not node: return None,None
    if key<node.key:
        l,node.left=split(node.left,key); update(node); return l,node
    else:
        node.right,r=split(node.right,key); update(node); return node,r

def merge(left, right):
    if not left or not right: return left or right
    if left.priority>right.priority:
        left.right=merge(left.right,right); update(left); return left
    else:
        right.left=merge(left,right.left); update(right); return right

class Treap:
    def __init__(self): self.root=None
    def insert(self, key):
        l,r=split(self.root,key)
        self.root=merge(merge(l,TreapNode(key)),r)
    def delete(self, key):
        def _del(node,key):
            if not node: return node
            if key<node.key: node.left=_del(node.left,key)
            elif key>node.key: node.right=_del(node.right,key)
            else: return merge(node.left,node.right)
            update(node); return node
        self.root=_del(self.root,key)
    def find(self, key):
        n=self.root
        while n:
            if key==n.key: return True
            n=n.left if key<n.key else n.right
        return False
    def kth(self, k):
        n=self.root
        while n:
            ls=size(n.left)
            if k<=ls: n=n.left
            elif k==ls+1: return n.key
            else: k-=ls+1; n=n.right
    def inorder(self):
        result=[]
        def _in(n):
            if n: _in(n.left); result.append(n.key); _in(n.right)
        _in(self.root); return result

if __name__=="__main__":
    random.seed(42); t=Treap()
    for x in [5,3,8,1,4,7,9,2,6]: t.insert(x)
    print(f"Inorder: {t.inorder()}")
    print(f"Find 4: {t.find(4)}, Find 10: {t.find(10)}")
    print(f"3rd smallest: {t.kth(3)}")
    t.delete(5); print(f"After delete 5: {t.inorder()}")
