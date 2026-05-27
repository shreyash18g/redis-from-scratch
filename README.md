# Redis From Scratch (C++)

A Redis-like in-memory database being built completely from scratch using low-level systems programming and networking concepts in C++.

This project focuses on deeply understanding how real-world systems like Redis work internally instead of using frameworks or high-level abstractions.

---

# Project Goals

The goal of this project is to learn and implement:

- TCP/IP networking
- Socket programming
- Request-response protocols
- Binary serialization
- Event-driven architecture
- Non-blocking IO
- Concurrent server design
- Buffer management
- Custom data structures
- Low-level systems programming

---

# Why Build Redis From Scratch?

Redis is much more than a key-value store.

It is one of the best real-world examples of:

- high-performance networking
- event loops
- protocol engineering
- efficient memory usage
- scalable concurrent systems

Building it from scratch helps understand how production systems actually work internally.

---

# Project Structure

| Module | Description |
|---|---|
| 01_tcp_server_client | Basic TCP client-server communication |
| 02_request_response_protocol | Custom binary protocol over TCP |
| 03_event_loop_server | Non-blocking event-driven server |
| 04_key_value_server | Redis-like command parsing and KV storage |

---

# Learning Progression

This project is being developed incrementally.

Each module introduces one major systems programming concept and builds upon the previous implementation.

---

## 01 — TCP Server Client

Learned:

- socket lifecycle
- bind/listen/accept/connect
- blocking IO
- basic request-response communication

---

## 02 — Request Response Protocol

Learned:

- TCP is a byte stream
- message framing
- length-prefixed protocols
- partial reads/writes
- serialization/deserialization

---

## 03 — Event Loop Server

Learned:

- non-blocking IO
- `poll()` syscall
- readiness-based concurrency
- per-connection state
- pipelined requests
- input/output buffering

---

## 04 — Key Value Server

Learned:

- command parsing
- structured binary requests
- request pipelining
- Redis-like protocol behavior
- in-memory key-value handling

---

# Core Concepts Implemented

## Networking

- TCP sockets
- connection management
- socket options
- blocking vs non-blocking IO

---

## Concurrency

- event loops
- readiness notifications
- poll()
- single-threaded concurrent servers

---

## Protocol Engineering

- binary protocols
- length-prefixed messages
- request parsing
- serialization/deserialization

---

## Buffer Management

- incoming buffers
- outgoing buffers
- partial reads
- partial writes
- pipelined request handling

---

# Technologies Used

- C++
- Linux socket APIs
- TCP/IP
- poll()
- Non-blocking IO
- g++
- Git/GitHub

---

# Build

Compile any module:

```bash
g++ server.cpp -o server
g++ client.cpp -o client
```

---

# Future Work

Planned features:

- custom hash table
- TTL expiration
- timers
- thread pool
- sorted sets
- balanced trees
- persistence
- optimized memory management

---

# Key Takeaway

This project is focused on understanding systems programming fundamentals deeply by implementing them manually instead of relying on libraries or frameworks.

---
