# Redis From Scratch (C/C++)

A Redis-like in-memory database built completely from scratch using low-level systems programming and networking concepts in C++.

The goal of this project is to understand how high-performance systems like Redis work internally by implementing networking, protocols, concurrency models, serialization, and core data structures manually without relying on frameworks.

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

| Module                       | Description                                      |
| ---------------------------- | ------------------------------------------------ |
| 01_tcp_server_client         | Basic TCP client-server communication            |
| 02_request_response_protocol | Custom binary protocol over TCP                  |
| 03_event_loop_server         | Non-blocking event-driven server                 |
| 04_key_value_server          | Redis-like command parsing and key-value storage |
| 05_hashtable_kv_store        | Custom hashtable with progressive rehashing      |
| 06_data_serialization        | Binary serialization for typed Redis responses   |

---

# Implemented Concepts

## Networking

* TCP sockets
* bind / listen / accept / connect
* blocking and non-blocking IO
* socket options
* connection management

---

## Protocol Engineering

* custom binary protocols
* request-response messaging
* length-prefixed message framing
* serialization and deserialization
* pipelined request handling

---

## Event-Driven Concurrency

* single-threaded event loop
* poll()-based readiness notifications
* non-blocking reads and writes
* per-connection state management
* buffered IO

---

## Data Structures

* custom chaining hashtable
* intrusive linked-list nodes
* progressive rehashing
* incremental key migration

---

## Data Serialization

* typed binary responses
* TLV-style serialization
* strings
* integers
* arrays
* errors
* null values

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
* poll()-based event loop
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

## 06 — Data Serialization

Implemented:

* typed response protocol
* binary serialization
* array responses
* error responses
* null handling
* dynamic response generation

---

# Technologies Used

* C++
* Linux Socket APIs
* TCP/IP
* poll()
* Non-blocking IO
* g++
* Git / GitHub

---

# Build

Compile a module:

```bash
g++ server.cpp -o server
g++ client.cpp -o client
```

Modules containing additional source files:

```bash
g++ server.cpp hashtable.cpp -o server
```

---

# Future Work

Planned features:

* balanced binary trees
* sorted sets
* TTL expiration
* timers
* thread pool
* cache eviction
* persistence
* optimized buffer management
* RESP protocol compatibility

---

# Key Takeaway

The objective of this project is not only to build a Redis clone, but to gain a deep understanding of the networking, concurrency, protocol design, serialization, and data structure techniques that power modern high-performance backend systems.
