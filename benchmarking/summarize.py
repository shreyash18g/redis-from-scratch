#!/usr/bin/env python3
"""
Parses results.jsonl (produced by run_sweep.sh) into:
  1. A clean table printed to stdout
  2. Draft resume bullet points based on the actual numbers measured

Run after run_sweep.sh finishes:
    python3 summarize.py
"""
import json
import sys

def load_results(path="results.jsonl"):
    rows = []
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    except FileNotFoundError:
        print(f"ERROR: {path} not found. Run ./run_sweep.sh first.")
        sys.exit(1)
    return rows


def main():
    rows = load_results()

    throughput_rows = [r for r in rows if "concurrency" in r and r.get("workload") == "mixed"]
    workload_rows = [r for r in rows if "concurrency" in r and r.get("concurrency") == 200]
    maxconn_rows = [r for r in rows if "target_connections" in r]

    print("\n=== PHASE 1: Throughput vs Concurrency (mixed 80/20 GET/SET workload) ===")
    print(f"{'Concurrency':>12} {'Ops/sec':>10} {'p50 ms':>8} {'p95 ms':>8} {'p99 ms':>8} {'Errors':>8}")
    best_throughput = None
    for r in sorted(throughput_rows, key=lambda x: x["concurrency"]):
        lat = r["latency_ms"]
        print(f"{r['concurrency']:>12} {r['throughput_ops_per_sec']:>10.1f} "
              f"{lat['p50']:>8} {lat['p95']:>8} {lat['p99']:>8} {r['errors']:>8}")
        if best_throughput is None or r["throughput_ops_per_sec"] > best_throughput["throughput_ops_per_sec"]:
            best_throughput = r

    print("\n=== PHASE 2: Throughput by command type (concurrency=200) ===")
    print(f"{'Workload':>12} {'Ops/sec':>10} {'p50 ms':>8} {'p99 ms':>8}")
    for r in workload_rows:
        lat = r["latency_ms"]
        print(f"{r['workload']:>12} {r['throughput_ops_per_sec']:>10.1f} {lat['p50']:>8} {lat['p99']:>8}")

    print("\n=== PHASE 3: Max concurrent connections ===")
    print(f"{'Target':>10} {'Established':>12} {'Connect errors':>16}")
    max_successful = 0
    for r in sorted(maxconn_rows, key=lambda x: x["target_connections"]):
        print(f"{r['target_connections']:>10} {r['connections_established']:>12} {r['connect_errors']:>16}")
        if r["connect_errors"] == 0:
            max_successful = max(max_successful, r["connections_established"])
        else:
            max_successful = max(max_successful, r["connections_established"])

    print("\n" + "=" * 60)
    print("DRAFT RESUME / TALKING POINTS (based on YOUR measured numbers)")
    print("=" * 60)
    if best_throughput:
        print(f"- Sustained {best_throughput['throughput_ops_per_sec']:.0f} req/sec at "
              f"{best_throughput['concurrency']} concurrent client connections "
              f"(p99 latency {best_throughput['latency_ms']['p99']} ms)")
    if max_successful:
        print(f"- Handled {max_successful} concurrent client connections via a poll()-based "
              f"single-threaded event loop with a 4-thread pool for async cleanup of large data structures")
    print("- NOTE: command execution is single-threaded (same architectural pattern as production")
    print("  Redis); the thread pool only offloads destructor work for large sorted sets (>1000")
    print("  members), not request processing. Be ready to explain this distinction in interviews.")
    print()
    print("Remember: re-run this on a quiet machine (close Chrome tabs, IDEs) for your final")
    print("numbers, and note your exact CPU/RAM in your resume footnote or be ready to state it.")


if __name__ == "__main__":
    main()
