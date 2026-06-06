# Timers and Idle Connection Timeouts

## Overview

This module extends the Redis-like event-driven server by introducing timer management and idle connection timeouts.

Until the previous chapter, connections could remain open forever if clients stopped communicating. This module solves that problem by tracking connection activity and automatically closing inactive connections after a fixed timeout period.

The implementation integrates timers directly into the event loop without requiring additional threads.

---

## Features

- Idle connection detection
- Automatic connection cleanup
- Monotonic clock based timing
- Event loop timeout integration
- Intrusive doubly linked list timers
- O(1) timer insertion and removal
- Resource cleanup for inactive clients

---

## Files

| File | Description |
|--------|-------------|
| `12_server.cpp` | Event-loop server with timer support |
| `list.h` | Doubly linked list implementation |
| `avl.cpp` / `avl.h` | AVL tree implementation |
| `hashtable.cpp` / `hashtable.h` | Hash table implementation |
| `zset.cpp` / `zset.h` | Sorted set implementation |
| `common.h` | Shared definitions and utilities |

---

## Why Timers Are Needed

Real-world network applications cannot keep connections open forever.

Timers are commonly used for:

- Idle connection cleanup
- Network timeout handling
- Cache expiration (TTL)
- Resource management

Without timers, disconnected or inactive clients may continue consuming server resources indefinitely.

---

## Timer Design

Each connection stores its last activity timestamp:

```cpp
uint64_t last_active_ms;
```

Whenever a client performs:

- Read operation
- Write operation

the timestamp is updated.

The connection is then moved to the end of the timer list, indicating it is the most recently active connection.

---

## Monotonic Clock

The server uses:

```cpp
clock_gettime(CLOCK_MONOTONIC, &tv);
```

instead of wall-clock time.

### Why?

Wall-clock time can change because of:

- NTP synchronization
- Manual clock changes
- Timezone adjustments

This can make timeout calculations incorrect.

Monotonic clocks only move forward and are ideal for measuring elapsed time.

---

## Doubly Linked List Timers

Timers are stored in an intrusive doubly linked list:

```cpp
struct DList {
    DList *prev;
    DList *next;
};
```

Advantages:

- O(1) insertion
- O(1) removal
- O(1) access to oldest timer
- No extra memory allocations

The list is ordered by activity time.

The front of the list always contains the oldest connection.

---

## Event Loop Integration

The timeout value passed to `poll()` is computed from the nearest timer:

```cpp
poll(fds, nfds, timeout_ms);
```

The event loop wakes up when:

- Socket activity occurs
- A timer expires

This allows timers and network I/O to coexist within the same event loop.

---

## Idle Connection Processing

When the event loop wakes up:

1. Check the oldest connection.
2. Compare current time with its expiration time.
3. Remove expired connections.
4. Stop when the first non-expired connection is found.

Because timers are ordered, only the front of the list needs to be examined.

---

## Connection Lifecycle

```text
New Connection
      |
      v
Added To Timer List
      |
      v
Read / Write Activity
      |
      v
Update Timestamp
      |
      v
Move To Back Of List
      |
      v
Timeout Reached?
   /       \
 No         Yes
 |           |
 v           v
Continue   Close Connection
```

---

## Example

### Start Server

```bash
./server
```

### Connect Using Netcat

```bash
nc 127.0.0.1 1234
```

### Server Output

```text
new client from 127.0.0.1:60742
removing idle connection: 4
```

The server automatically closes the connection after the configured timeout period.

---

## Concepts Learned

- Timers in event-driven systems
- Connection timeout management
- CLOCK_MONOTONIC
- Doubly linked lists
- Intrusive data structures
- poll() timeouts
- Idle connection cleanup
- Resource management
- Event loop scheduling

---

## Build

```bash
g++ -Wall -Wextra -O2 -g \
12_server.cpp \
avl.cpp \
hashtable.cpp \
zset.cpp \
-o server
```

---

## Key Takeaway

Timers are a fundamental part of production network servers.

By combining timers with the event loop, the server can efficiently manage both network I/O and connection lifecycles without additional threads, making the architecture scalable and resource efficient.

---

## Next Step

- Network I/O timeouts
- TTL-based key expiration
- Advanced timer scheduling
- Persistent storage
- More Redis-compatible commands