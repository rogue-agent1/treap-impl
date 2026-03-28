#!/usr/bin/env python3
"""Treap (tree + heap) balanced BST."""
import sys,random
class Node:
    def __init__(self,key):
        self.key=key;self.pri=random.random();self.left=self.right=None;self.size=1
def size(n): return n.size if n else 0
def update(n):
    if n: n.size=1+size(n.left)+size(n.right)
def split(n,key):
    if not n: return None,None
    if key<n.key:
        l,n.left=split(n.left,key); update(n); return l,n
    else:
        n.right,r=split(n.right,key); update(n); return n,r
def merge(l,r):
    if not l or not r: return l or r
    if l.pri>r.pri: l.right=merge(l.right,r); update(l); return l
    else: r.left=merge(l,r.left); update(r); return r
class Treap:
    def __init__(self): self.root=None
    def insert(self,key):
        l,r=split(self.root,key); self.root=merge(merge(l,Node(key)),r)
    def delete(self,key):
        def _del(n,k):
            if not n: return n
            if k<n.key: n.left=_del(n.left,k)
            elif k>n.key: n.right=_del(n.right,k)
            else: return merge(n.left,n.right)
            update(n); return n
        self.root=_del(self.root,key)
    def kth(self,k):
        n=self.root
        while n:
            ls=size(n.left)
            if k<=ls: n=n.left
            elif k==ls+1: return n.key
            else: k-=ls+1; n=n.right
    def inorder(self):
        res=[];stack=[];n=self.root
        while stack or n:
            while n: stack.append(n); n=n.left
            n=stack.pop(); res.append(n.key); n=n.right
        return res
    def __len__(self): return size(self.root)
def main():
    random.seed(42); t=Treap()
    for x in [5,3,8,1,4,7,9,2,6]: t.insert(x)
    print(f"Inserted: {t.inorder()}")
    print(f"Size: {len(t)}, 3rd smallest: {t.kth(3)}")
    t.delete(5); print(f"After delete(5): {t.inorder()}")
if __name__=="__main__": main()
