"""
Async load tester for the custom redis-clone server (11_thread_pool).

Usage:
    python3 load_test.py --host 127.0.0.1 --port 1234 --conns 100 --duration 10 --workload set

Each "connection" is one asyncio task holding one TCP connection open,
sending request -> waiting for response -> repeat, for `duration` seconds.
This measures *request-response* throughput (not pipelined burst throughput),
which matches how a real client would use this server.

Records per-request latency so we can report p50/p95/p99, not just an average.
"""
import asyncio
import argparse
import struct
import time
import random
import string
import sys
import json
from protocol import encode_request, decode_response


async def read_one_response(reader: asyncio.StreamReader) -> bytes:
    header = await reader.readexactly(4)
    (length,) = struct.unpack("<I", header)
    body = await reader.readexactly(length)
    return body


def rand_str(n=8):
    return "".join(random.choices(string.ascii_lowercase, k=n))


def make_command(workload: str, keyspace: int, _state: dict):
    """Build one command (list of str args) according to the chosen workload."""
    if workload == "set":
        k = f"key:{random.randint(0, keyspace)}"
        v = rand_str(16)
        return ["set", k, v]
    elif workload == "get":
        k = f"key:{random.randint(0, keyspace)}"
        return ["get", k]
    elif workload == "mixed":
        # 80% GET, 20% SET -- typical cache-like access pattern
        k = f"key:{random.randint(0, keyspace)}"
        if random.random() < 0.8:
            return ["get", k]
        else:
            return ["set", k, rand_str(16)]
    elif workload == "zadd":
        member = f"member:{random.randint(0, keyspace)}"
        score = str(random.random() * 1000)
        return ["zadd", "bench_zset", score, member]
    elif workload == "ping_like":
        # smallest possible roundtrip: GET on a key that doesn't exist
        return ["get", "nonexistent_key_for_latency_floor"]
    else:
        raise ValueError(f"unknown workload {workload}")


async def worker(
    worker_id: int,
    host: str,
    port: int,
    duration: float,
    workload: str,
    keyspace: int,
    results: dict,
    stop_event: asyncio.Event,
    connect_only: bool = False,
):
    """One persistent connection issuing request/response pairs until stop_event or duration elapses."""
    try:
        reader, writer = await asyncio.open_connection(host, port)
    except Exception as e:
        results["connect_errors"] += 1
        return

    results["connections_established"] += 1

    if connect_only:
        # used for the "max concurrent connections" test -- just hold the socket open
        try:
            await stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            writer.close()
        return

    local_latencies = []
    local_errors = 0
    local_ops = 0
    end_time = time.monotonic() + duration

    while time.monotonic() < end_time and not stop_event.is_set():
        cmd = make_command(workload, keyspace, results)
        req = encode_request(cmd)
        t0 = time.perf_counter()
        try:
            writer.write(req)
            await writer.drain()
            body = await read_one_response(reader)
            decode_response(body)  # parse to make sure it's well-formed
        except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError, OSError):
            local_errors += 1
            break
        t1 = time.perf_counter()
        local_latencies.append(t1 - t0)
        local_ops += 1

    writer.close()
    try:
        await writer.wait_closed()
    except Exception:
        pass

    results["latencies"].extend(local_latencies)
    results["errors"] += local_errors
    results["ops"] += local_ops


def percentile(sorted_list, p):
    if not sorted_list:
        return float("nan")
    k = (len(sorted_list) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_list) - 1)
    if f == c:
        return sorted_list[f]
    d0 = sorted_list[f] * (c - k)
    d1 = sorted_list[c] * (k - f)
    return d0 + d1


async def run_load_test(host, port, conns, duration, workload, keyspace, ramp_up):
    results = {
        "latencies": [],
        "errors": 0,
        "ops": 0,
        "connect_errors": 0,
        "connections_established": 0,
    }
    stop_event = asyncio.Event()

    tasks = []
    for i in range(conns):
        tasks.append(asyncio.create_task(
            worker(i, host, port, duration, workload, keyspace, results, stop_event)
        ))
        if ramp_up > 0:
            await asyncio.sleep(ramp_up / max(conns, 1))

    t_start = time.monotonic()
    await asyncio.gather(*tasks)
    wall_time = time.monotonic() - t_start

    lat = sorted(results["latencies"])
    summary = {
        "workload": workload,
        "concurrency": conns,
        "wall_time_sec": round(wall_time, 3),
        "total_ops": results["ops"],
        "errors": results["errors"],
        "connect_errors": results["connect_errors"],
        "connections_established": results["connections_established"],
        "throughput_ops_per_sec": round(results["ops"] / wall_time, 1) if wall_time > 0 else 0,
        "latency_ms": {
            "min": round(lat[0] * 1000, 3) if lat else None,
            "p50": round(percentile(lat, 0.50) * 1000, 3) if lat else None,
            "p95": round(percentile(lat, 0.95) * 1000, 3) if lat else None,
            "p99": round(percentile(lat, 0.99) * 1000, 3) if lat else None,
            "max": round(lat[-1] * 1000, 3) if lat else None,
            "avg": round((sum(lat) / len(lat)) * 1000, 3) if lat else None,
        },
    }
    return summary


async def run_max_connections_test(host, port, target_conns, hold_seconds):
    """Try to open `target_conns` simultaneous connections and see how many succeed."""
    results = {
        "latencies": [],
        "errors": 0,
        "ops": 0,
        "connect_errors": 0,
        "connections_established": 0,
    }
    stop_event = asyncio.Event()
    tasks = []
    batch = 50  # open in batches to get a clean progress signal
    for i in range(0, target_conns, batch):
        n = min(batch, target_conns - i)
        for j in range(n):
            tasks.append(asyncio.create_task(
                worker(i + j, host, port, 0, "set", 1, results, stop_event, connect_only=True)
            ))
        await asyncio.sleep(0.05)

    await asyncio.sleep(hold_seconds)
    stop_event.set()
    await asyncio.gather(*tasks, return_exceptions=True)

    return {
        "target_connections": target_conns,
        "connections_established": results["connections_established"],
        "connect_errors": results["connect_errors"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=1234)
    ap.add_argument("--mode", choices=["throughput", "max_conns"], default="throughput")
    ap.add_argument("--conns", type=int, default=50)
    ap.add_argument("--duration", type=float, default=10.0)
    ap.add_argument("--workload", choices=["set", "get", "mixed", "zadd", "ping_like"], default="mixed")
    ap.add_argument("--keyspace", type=int, default=10000)
    ap.add_argument("--ramp_up", type=float, default=0.0, help="seconds to spread out connection startup")
    ap.add_argument("--hold_seconds", type=float, default=3.0, help="for max_conns mode: how long to hold connections open")
    ap.add_argument("--out", default=None, help="optional path to append JSON line result")
    args = ap.parse_args()

    if args.mode == "throughput":
        summary = asyncio.run(run_load_test(
            args.host, args.port, args.conns, args.duration, args.workload, args.keyspace, args.ramp_up
        ))
    else:
        summary = asyncio.run(run_max_connections_test(args.host, args.port, args.conns, args.hold_seconds))

    print(json.dumps(summary, indent=2))
    if args.out:
        with open(args.out, "a") as f:
            f.write(json.dumps(summary) + "\n")


if __name__ == "__main__":
    main()
