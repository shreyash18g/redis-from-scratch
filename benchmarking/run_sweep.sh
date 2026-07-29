#!/usr/bin/env bash
# Full benchmark sweep for the custom redis-clone (11_thread_pool).
#
# USAGE:
#   1. In one terminal:  cd ~/Desktop/Redis/11_thread_pool && ./redis_server
#   2. In another:       cd ~/Desktop/Redis_bench && ./run_sweep.sh
#
# Produces results.jsonl (one JSON object per line) plus a human-readable
# summary printed to stdout. Takes about 3-4 minutes total.

set -e
HOST=127.0.0.1
PORT=1234
OUT=results.jsonl
rm -f "$OUT"

echo "=================================================="
echo " Checking server is reachable on $HOST:$PORT ..."
echo "=================================================="
python3 -c "
import socket
s = socket.socket()
s.settimeout(2)
try:
    s.connect(('$HOST', $PORT))
    print('OK: server is listening')
except Exception as e:
    print('ERROR: could not connect ->', e)
    print('Make sure ./redis_server is running first.')
    raise SystemExit(1)
"

echo
echo "=================================================="
echo " PHASE 1: Throughput sweep across concurrency levels"
echo " workload=mixed (80% GET / 20% SET), 8s each"
echo "=================================================="
for CONNS in 1 10 50 100 250 500 1000; do
    echo "--- concurrency=$CONNS ---"
    python3 load_test.py --host $HOST --port $PORT \
        --conns $CONNS --duration 8 --workload mixed --keyspace 50000 \
        --out "$OUT"
    sleep 1
done

echo
echo "=================================================="
echo " PHASE 2: Workload comparison at fixed concurrency=200"
echo "=================================================="
for WL in get set zadd ping_like; do
    echo "--- workload=$WL ---"
    python3 load_test.py --host $HOST --port $PORT \
        --conns 200 --duration 8 --workload "$WL" --keyspace 50000 \
        --out "$OUT"
    sleep 1
done

echo
echo "=================================================="
echo " PHASE 3: Max concurrent connections"
echo " (tries to open increasing connection counts, holds 3s each)"
echo "=================================================="
for N in 500 1000 2000 5000 10000; do
    echo "--- target_connections=$N ---"
    python3 load_test.py --host $HOST --port $PORT \
        --mode max_conns --conns $N --hold_seconds 3 \
        --out "$OUT" || echo "  (failed at $N -- this is useful data, the limit was below $N)"
    sleep 1
done

echo
echo "=================================================="
echo " DONE. Raw results in $OUT"
echo " Run: python3 summarize.py to get a clean table + resume-ready lines"
echo "=================================================="
