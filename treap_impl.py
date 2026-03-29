#!/usr/bin/env python3
"""treap_impl - Randomized treap."""
import sys, argparse, json, random

class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.left = self.right = None
        self.size = 1

def _size(n): return n.size if n else 0
def _update(n):
    if n: n.size = 1 + _size(n.left) + _size(n.right)

def split(node, key):
    if not node: return None, None
    if node.key <= key:
        node.right, right = split(node.right, key)
        _update(node)
        return node, right
    else:
        left, node.left = split(node.left, key)
        _update(node)
        return left, node

def merge(left, right):
    if not left or not right: return left or right
    if left.priority > right.priority:
        left.right = merge(left.right, right)
        _update(left)
        return left
    else:
        right.left = merge(left, right.left)
        _update(right)
        return right

class Treap:
    def __init__(self):
        self.root = None
    def insert(self, key):
        left, right = split(self.root, key - 0.5)
        self.root = merge(merge(left, TreapNode(key)), right)
    def remove(self, key):
        left, mid_right = split(self.root, key - 0.5)
        _, right = split(mid_right, key)
        self.root = merge(left, right)
    def inorder(self):
        result = []
        def dfs(n):
            if not n: return
            dfs(n.left); result.append(n.key); dfs(n.right)
        dfs(self.root)
        return result
    @property
    def size(self): return _size(self.root)

def main():
    p = argparse.ArgumentParser(description="Treap CLI")
    p.add_argument("values", nargs="+", type=int)
    p.add_argument("--remove", nargs="*", type=int, default=[])
    args = p.parse_args()
    t = Treap()
    for v in args.values: t.insert(v)
    for v in args.remove: t.remove(v)
    print(json.dumps({"size": t.size, "sorted": t.inorder()}, indent=2))

if __name__ == "__main__":
    main()
