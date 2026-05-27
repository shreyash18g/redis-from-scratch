# 04 - Key Value Server

A minimal Redis-like in-memory key-value server built using non-blocking sockets and an event-driven architecture.

This module extends the previous event-loop server by adding:

- command parsing
- structured binary requests
- key-value storage

---

# Features

- TCP client-server communication
- Event loop using `poll()`
- Non-blocking IO
- Request pipelining
- Binary protocol
- In-memory key-value storage

---

# Supported Commands

## SET

```bash
./client set name shreyash
```

---

## GET

```bash
./client get name
```

---

## DEL

```bash
./client del name
```

---

# Protocol Format

Requests are encoded as:

```text
[len][nstr][len][str1][len][str2]...
```

Example:

```text
set name shreyash
```

---

# Architecture Flow

```text
Client
  ↓
TCP Socket
  ↓
poll() Event Loop
  ↓
Incoming Buffer
  ↓
Protocol Parser
  ↓
Command Processor
  ↓
Outgoing Buffer
  ↓
Socket Write
```

---

# Concepts Implemented

- non-blocking sockets
- event-driven networking
- request parsing
- serialization/deserialization
- buffered IO
- pipelined requests
- per-connection state management

---

# Build

```bash
g++ -Wall -Wextra -O2 -g server.cpp -o server
g++ -Wall -Wextra -O2 -g client.cpp -o client
```

---

# Run

Start server:

```bash
./server
```

Run client:

```bash
./client set name shreyash
./client get name
./client del name
```

---

# Future Improvements

- custom hash table
- TTL expiration
- persistence
- thread pool
- optimized buffers
