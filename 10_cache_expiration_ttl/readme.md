# Cache Expiration with TTL

## Overview

This project extends a Redis-like in-memory database by adding **Time-To-Live (TTL)** support for keys.

TTL enables automatic removal of keys after a specified duration, making the database suitable for caching scenarios where stale data should be removed without manual intervention.

The implementation introduces a **Min Heap** to efficiently manage expiration timers while preserving fast key lookups through a hash table.

---

## Features

### Key-Value Operations

* SET
* GET
* DEL
* KEYS

### Sorted Set Operations

* ZADD
* ZREM
* ZSCORE
* ZQUERY

### TTL Operations

* EXPIRE `<key> <milliseconds>`
* TTL `<key>`
* PERSIST `<key>`

### Automatic Expiration

* Keys expire automatically after their TTL elapses.
* Expired entries are removed during timer processing.
* Expiration work is rate-limited to prevent blocking the event loop.

---

## System Design

### Hash Table

All keys are stored in a hash table for fast average-case lookups, insertions, and deletions.

### AVL Tree

Sorted sets are implemented using an AVL tree to maintain ordered elements and support efficient range queries.

### Min Heap

TTL timers are stored in a Min Heap.

Each heap item contains:

```cpp
struct HeapItem {
    uint64_t val;      // expiration timestamp
    size_t *ref;       // reference to heap index
};
```

The heap guarantees that the root always contains the nearest expiration time.

### Entry Structure

Each key maintains the position of its associated heap node:

```cpp
struct Entry {
    HNode node;
    std::string key;
    size_t heap_idx = -1;
};
```

This allows efficient updates and deletion of TTL information.

---

## Heap Operations

### Insert

New timers are appended to the heap and moved upward until heap order is restored.

**Complexity:** O(log N)

### Update

When a TTL changes, the heap node is adjusted either upward or downward depending on the new expiration time.

**Complexity:** O(log N)

### Delete

The target node is swapped with the last heap element and removed, followed by heap restoration.

**Complexity:** O(log N)

### Find Next Expiration

The minimum expiration timestamp is always stored at the root.

**Complexity:** O(1)

---

## Timer Processing

The event loop periodically checks for:

1. Idle client connections
2. Expired TTL entries

Expired keys are:

1. Removed from the hash table
2. Removed from the heap
3. Freed from memory

To avoid long pauses, expiration processing is limited per iteration:

```cpp
const size_t k_max_works = 2000;
```

This ensures responsiveness even when many keys expire simultaneously.

---

## Building

Compile using:

```bash
g++ -std=gnu++20 \
10_server.cpp \
avl.cpp \
hashtable.cpp \
heap.cpp \
zset.cpp \
-o server
```

---

## Running

Start the server:

```bash
./server
```

The server listens for client connections and processes requests using an event-driven architecture.

---

## Project Structure

```text
10_cache_expiration_ttl/
├── 10_server.cpp
├── avl.cpp
├── avl.h
├── common.h
├── hashtable.cpp
├── hashtable.h
├── heap.cpp
├── heap.h
├── list.h
├── test_heap.cpp
├── zset.cpp
├── zset.h
└── README.md
```

---

## Time Complexity

### Hash Table

| Operation | Complexity   |
| --------- | ------------ |
| Lookup    | O(1) Average |
| Insert    | O(1) Average |
| Delete    | O(1) Average |

### AVL Tree

| Operation | Complexity |
| --------- | ---------- |
| Search    | O(log N)   |
| Insert    | O(log N)   |
| Delete    | O(log N)   |

### Min Heap

| Operation    | Complexity |
| ------------ | ---------- |
| Find Minimum | O(1)       |
| Insert       | O(log N)   |
| Update       | O(log N)   |
| Delete       | O(log N)   |

---

## Key Learning Concepts

* Event-driven server architecture
* In-memory database design
* Hash tables
* AVL trees
* Heap data structures
* Timer scheduling
* Cache expiration mechanisms
* Efficient TTL management
* Memory-safe deletion of expired entries

