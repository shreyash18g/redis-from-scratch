# 05 - Hashtable KV Store

A Redis-like in-memory key-value store implemented using a custom chaining hashtable with progressive rehashing.

This module extends the event-loop server by replacing temporary storage with a real database structure.

---

# Features

- Event-driven TCP server
- Non-blocking IO using `poll()`
- Binary request-response protocol
- Custom chaining hashtable
- Progressive rehashing
- In-memory key-value storage

---

# Supported Commands

## SET

```bash
./client set name shreyash
```

## GET

```bash
./client get name
```

## DEL

```bash
./client del name
```

---

# Hashtable Design

The hashtable uses:

- chaining collision handling
- linked-list buckets
- progressive resizing
- incremental rehashing

Two tables are maintained during resizing:

- newer table
- older table

Keys are migrated gradually to avoid latency spikes.

---

# Concepts Implemented

- custom hash table
- intrusive data structures
- progressive rehashing
- non-blocking sockets
- event-driven networking
- binary protocols

---

# Build

```bash
g++ -Wall -Wextra -O2 -g server.cpp hashtable.cpp -o server
```

---

# Run

Start server:

```bash
./server
```

Use the client from:

```text
04_key_value_server/
```

Example:

```bash
./client set key value
./client get key
./client del key
```