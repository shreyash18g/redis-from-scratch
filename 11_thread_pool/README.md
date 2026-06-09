# Thread Pool Redis Server

## Overview

This project implements a Redis-inspired in-memory database server in C++ with support for concurrent request processing using a thread pool. It extends previous implementations by introducing background worker threads to handle expensive operations without blocking the main event loop.

The server supports key-value storage, sorted sets, key expiration (TTL), and efficient data structures including hash tables, AVL trees, and heaps.

## Features

### Key-Value Operations

* SET – Store a key-value pair
* GET – Retrieve a value by key
* DEL – Delete a key
* KEYS – List all stored keys

### Sorted Sets

* ZADD – Add or update a member score
* ZREM – Remove a member
* ZSCORE – Get a member score
* ZQUERY – Query sorted set members

### Key Expiration

* PEXPIRE – Set key expiration in milliseconds
* PTTL – Retrieve remaining TTL
* Automatic key removal after expiration

### Concurrency

* Thread pool based task execution
* Non-blocking event-driven server architecture
* Concurrent request processing
* Efficient resource utilization

## Data Structures Used

### Hash Table

Used for fast key lookups with average O(1) complexity.

### AVL Tree

Maintains sorted set ordering while providing balanced tree operations.

### Binary Heap

Used for managing expiration timers and efficiently locating the nearest expiration event.

### Thread Pool

Executes background tasks using worker threads, preventing long-running operations from blocking the server.

## Project Structure

```text
11_thread_pool/
├── 11_server.cpp
├── thread_pool.cpp
├── thread_pool.h
├── hashtable.cpp
├── hashtable.h
├── avl.cpp
├── avl.h
├── heap.cpp
├── heap.h
├── zset.cpp
├── zset.h
├── list.h
├── common.h
└── README.md
```

## Compilation

```bash
g++ -std=gnu++20 \
11_server.cpp \
hashtable.cpp \
avl.cpp \
heap.cpp \
thread_pool.cpp \
zset.cpp \
-o redis_server \
-pthread
```

## Running the Server

```bash
./redis_server
```

The server listens on:

```text
127.0.0.1:1234
```

## Running the Client

Compile the client:

```bash
g++ -std=gnu++20 client.cpp -o client
```

Example usage:

```bash
./client set foo bar
./client get foo

./client del foo

./client zadd leaderboard 100 alice
./client zscore leaderboard alice

./client set session active
./client pexpire session 5000
./client pttl session
```

## Example Output

```text
(str) bar

(int) 1

(dbl) 100

(int) 4987
```

## Technical Highlights

* Event-driven networking using sockets
* Binary request/response protocol
* Thread pool for concurrent task execution
* Balanced AVL tree implementation
* Heap-based timer management
* Automatic TTL expiration handling
* Efficient in-memory storage

## Learning Outcomes

Through this project:

* Implemented a Redis-like database server from scratch
* Built custom hash table and AVL tree data structures
* Developed a heap-based expiration scheduler
* Learned event-driven network programming
* Implemented multithreading using a thread pool
* Managed concurrency and shared resources efficiently
* Designed a custom client-server protocol

## Future Improvements

* Persistence support
* Publish/Subscribe messaging
* Transactions
* Replication
* Cluster support
* Authentication and access control
* Advanced Redis commands

## Conclusion

This project demonstrates the implementation of a high-performance in-memory database server with concurrent request processing, sorted set support, automatic key expiration, and efficient custom data structures. It provides practical experience in systems programming, networking, concurrency, and database internals.
