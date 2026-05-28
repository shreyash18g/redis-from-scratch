# Redis From Scratch (C/C++)

A Redis-like in-memory database being built completely from scratch using low-level systems programming and networking concepts in C++.

This project focuses on understanding how real-world systems like Redis work internally by implementing networking, protocols, concurrency models, and core data structures manually instead of relying on high-level frameworks.

---

# Goals

This project is being built to deeply understand:

* TCP/IP networking
* Socket programming
* Request-response protocols
* Binary serialization
* Event-driven architecture
* Non-blocking IO
* Concurrent server design
* Buffer management
* Custom data structures
* Systems programming fundamentals

---

# Project Structure

| Module                       | Description                                 |
| ---------------------------- | ------------------------------------------- |
| 01_tcp_server_client         | Basic TCP client-server communication       |
| 02_request_response_protocol | Custom binary protocol over TCP             |
| 03_event_loop_server         | Non-blocking event-driven server            |
| 04_key_value_server          | Redis-like command parsing and KV storage   |
| 05_hashtable_kv_store        | Custom hashtable with progressive rehashing |

---

# Implemented Concepts

## Networking

* TCP sockets
* bind / listen / accept / connect
* blocking vs non-blocking IO
* socket options
* connection management

---

## Protocol Engineering

* custom binary protocols
* request-response messaging
* serialization/deserialization
* length-prefixed message parsing
* pipelined request handling

---

## Event-Driven Concurrency

* single-threaded event loop
* `poll()` based readiness notifications
* non-blocking reads/writes
* per-connection state management
* buffered IO

---

## Data Structures

* custom chaining hashtable
* intrusive linked-list nodes
* progressive rehashing
* incremental key migration

---

# Architecture Evolution

## 01 — TCP Server Client

Implemented:

* socket lifecycle
* blocking IO
* basic request-response communication

---

## 02 — Request Response Protocol

Implemented:

* length-prefixed binary protocol
* partial read/write handling
* TCP stream parsing

---

## 03 — Event Loop Server

Implemented:

* non-blocking sockets
* `poll()` based event loop
* concurrent connection handling
* input/output buffering
* request pipelining

---

## 04 — Key Value Server

Implemented:

* command parsing
* Redis-like request handling
* structured binary requests
* in-memory key-value operations

---

## 05 — Hashtable KV Store

Implemented:

* custom hashtable
* chaining collision handling
* progressive rehashing
* incremental resizing

---

# Technologies Used

* C++
* Linux Socket APIs
* TCP/IP
* `poll()`
* Non-blocking IO
* g++
* Git/GitHub

---

# Build

Compile a module:

```bash
g++ server.cpp -o server
g++ client.cpp -o client
```

Example with multiple files:

```bash
g++ server.cpp hashtable.cpp -o server
```

---

# Future Work

Planned features:

* TTL expiration
* timers
* thread pool
* balanced trees
* sorted sets
* persistence
* optimized buffer management
* RESP protocol compatibility

---

# Key Takeaway

The focus of this project is not just building a Redis clone, but understanding the low-level systems concepts that power modern high-performance backend infrastructure.
