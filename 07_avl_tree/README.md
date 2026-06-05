# AVL Tree

## Overview

This module implements a self-balancing AVL Tree from scratch in C++.

AVL Trees maintain balance after insertions and deletions using rotations, ensuring O(log N) search, insertion, and deletion operations.

This data structure will later be used for Redis-like sorted sets and ordered indexing.

---

## Features

* Binary Search Tree
* Parent pointers
* Height tracking
* Left rotation
* Right rotation
* AVL rebalancing
* O(log N) lookup
* O(log N) insertion
* O(log N) deletion

---

## Concepts Learned

* Binary Search Trees
* Tree Rotations
* Height Balancing
* Recursive Data Structures
* Ordered Data Access
* Self-Balancing Trees

---

## Files

* avl.h
* avl.cpp
* test_avl.cpp

---

## Build

```bash
g++ avl.cpp test_avl.cpp -o test_avl
```

## Run

```bash
./test_avl
```

---

## Future Usage

This AVL Tree will serve as the foundation for implementing Redis-style sorted sets and ordered indexes.
