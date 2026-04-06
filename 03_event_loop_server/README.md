# Event Loop Based TCP Server (Non-blocking IO)

## Overview
This module implements a high-performance TCP server using an event loop and non-blocking IO.

## Features
- Handles multiple clients using a single thread
- Uses poll() for readiness detection
- Non-blocking read/write
- Input and output buffering
- Supports request pipelining
- Length-prefixed binary protocol

## Key Concepts
- Event-driven architecture
- Per-connection state management
- Partial reads and writes
- State transitions (READ → WRITE)

## Files
- server.cpp → Event loop based server
- client.cpp → Pipelined client

## How to Run
```bash
g++ server.cpp -o server
g++ client.cpp -o client

./server
./client