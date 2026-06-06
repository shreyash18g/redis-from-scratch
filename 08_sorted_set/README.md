# Sorted Set

## Overview

This module implements a Redis-style Sorted Set using two indexes:

* Hashtable for O(1) lookup by name
* AVL Tree for ordered access by score

The same data is indexed simultaneously by both structures using intrusive nodes.

---

## Features

* ZADD
* ZREM
* ZQUERY
* Ordered iteration
* Rank-based traversal
* AVL tree balancing
* Hashtable lookup
* Progressive rehashing

---

## Data Structures

### Hashtable

Provides fast lookup by name.

### AVL Tree

Maintains ordering by `(score, name)`.

### Sorted Set

Combines both structures to support efficient point, range, and rank queries.

---

## Concepts Learned

* Multi-indexed data structures
* Intrusive data structures
* AVL tree augmentation
* Order statistic trees
* Rank queries
* Sorted range scans

---

## Files

* 11_server.cpp
* zset.cpp
* zset.h
* avl.cpp
* avl.h
* hashtable.cpp
* hashtable.h

---

## Build

```bash
g++ 11_server.cpp hashtable.cpp zset.cpp avl.cpp -o server
```

---

## Testing

```bash
g++ test_offset.cpp avl.cpp -o test_offset
./test_offset

python3 test_cmds.py
```

---

## Next Step

Timer and timeout handling for TTL expiration.
