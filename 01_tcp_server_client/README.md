# TCP Server-Client (Basic)

## 📌 Overview

This module implements a basic TCP client-server communication system using low-level Linux socket APIs.
It serves as the foundation for building a Redis-like in-memory database from scratch.

---

## ⚙️ Features

### 🔹 Server

* Creates a TCP socket
* Binds to a port (`1234`)
* Listens for incoming connections
* Accepts client connections
* Reads data from client
* Sends a fixed response (`"world"`)

### 🔹 Client

* Creates a TCP socket
* Connects to server (`127.0.0.1:1234`)
* Sends a message (`"hello"`)
* Receives response from server

---

## 🔁 Communication Flow

Client:

```text
connect → send "hello"
```

Server:

```text
accept → read "hello" → send "world"
```

Client:

```text
read → "world"
```

---

## 🧠 Concepts Learned

* TCP socket lifecycle:

  * `socket()` → `bind()` → `listen()` → `accept()` (server)
  * `socket()` → `connect()` (client)

* Blocking I/O using:

  * `read()`
  * `write()`

* Byte order conversion:

  * `htons()` (host to network short)
  * `htonl()` (host to network long)

* Difference between:

  * Listening socket vs Connection socket

* Basic request-response communication model

---

## ▶️ How to Run

### 1. Compile

```bash
g++ server.cpp -o server
g++ client.cpp -o client
```

### 2. Run Server

```bash
./server
```

### 3. Run Client (in another terminal)

```bash
./client
```

---

## ✅ Expected Output

### Server:

```text
client says: hello
```

### Client:

```text
server says: world
```

---

## ⚠️ Limitations (To Be Improved Later)

* Handles only one client at a time
* Does not handle partial reads/writes
* No concurrency (single-threaded, blocking)
* No message framing (raw TCP byte stream)
* No error recovery or retry logic

---

## 🚀 Next Steps

* Implement request-response protocol
* Handle TCP stream properly (message boundaries)
* Add concurrency (event loop / non-blocking I/O)
* Build key-value storage (Redis core)

---

## 📚 Notes

This module focuses on understanding how applications interact with the OS using system calls and how TCP connections are established and used at a low level.

---
