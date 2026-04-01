# Request-Response Protocol

## 📌 Overview

This module extends the basic TCP server-client by introducing a custom binary protocol and handling multiple requests over a single TCP connection.

---

## ⚙️ Features

* Persistent TCP connection (multiple requests per connection)
* Custom binary protocol:

  * `[length (4 bytes)][message]`
* Proper handling of TCP stream:

  * Handles partial reads (`read_full`)
  * Handles partial writes (`write_all`)
* Safe buffer handling with size limits

---

## 🔁 Communication Flow

Client:

* Sends multiple requests (`hello1`, `hello2`, `hello3`)

Server:

* Reads length-prefixed messages
* Processes each request
* Sends response using same protocol

---

## 🧠 Concepts Learned

* TCP is a byte stream (no message boundaries)
* Need for application-level protocol
* Length-prefixed message design
* Partial read/write handling
* Kernel buffer behavior (push-based IO)
* Difference between file IO and socket IO

---

## ▶️ How to Run

### Compile

```bash
g++ server.cpp -o server
g++ client.cpp -o client
```

### Run

```bash
# Terminal 1
./server

# Terminal 2
./client
```

---

## ✅ Expected Output

### Server:

```
client says: hello1
client says: hello2
client says: hello3
EOF
```

### Client:

```
server says: world
server says: world
server says: world
```

---

## ⚠️ Limitations

* Single client at a time (no concurrency)
* Blocking I/O
* No advanced error recovery
* No command parsing (only echo-like behavior)

---

## 🚀 Next Steps

* Event loop (non-blocking I/O)
* Concurrent connections
* Command parsing (GET/SET)
* Data structures (hash table)

---
