"""
Wire protocol for the custom Redis clone (11_thread_pool/11_server.cpp).

Request:
    [total_len: u32][nstr: u32]( [arglen: u32][argbytes] )*nstr

Response:
    [total_len: u32][1-byte tag][tag payload]
    tag NIL=0 -> no payload
    tag ERR=1 -> [u32 code][u32 msglen][msg bytes]
    tag STR=2 -> [u32 len][bytes]
    tag INT=3 -> [i64]
    tag DBL=4 -> [f64]
    tag ARR=5 -> [u32 count][nested items...]
"""
import struct

TAG_NIL = 0
TAG_ERR = 1
TAG_STR = 2
TAG_INT = 3
TAG_DBL = 4
TAG_ARR = 5


def encode_request(args: list[str]) -> bytes:
    """Build one full wire message (length-prefixed) for a command like ['set','foo','bar']."""
    body = struct.pack("<I", len(args))
    for a in args:
        b = a.encode()
        body += struct.pack("<I", len(b)) + b
    return struct.pack("<I", len(body)) + body


def _parse_value(buf: bytes, off: int):
    """Parse one tagged value starting at off. Returns (value, new_off)."""
    tag = buf[off]
    off += 1
    if tag == TAG_NIL:
        return None, off
    if tag == TAG_ERR:
        code = struct.unpack_from("<I", buf, off)[0]
        off += 4
        mlen = struct.unpack_from("<I", buf, off)[0]
        off += 4
        msg = buf[off:off + mlen]
        off += mlen
        return ("ERR", code, msg), off
    if tag == TAG_STR:
        slen = struct.unpack_from("<I", buf, off)[0]
        off += 4
        s = buf[off:off + slen]
        off += slen
        return s, off
    if tag == TAG_INT:
        v = struct.unpack_from("<q", buf, off)[0]
        off += 8
        return v, off
    if tag == TAG_DBL:
        v = struct.unpack_from("<d", buf, off)[0]
        off += 8
        return v, off
    if tag == TAG_ARR:
        n = struct.unpack_from("<I", buf, off)[0]
        off += 4
        items = []
        for _ in range(n):
            val, off = _parse_value(buf, off)
            items.append(val)
        return items, off
    raise ValueError(f"unknown tag {tag} at offset {off-1}")


def decode_response(body: bytes):
    """body is the message payload (after stripping the outer 4-byte length prefix)."""
    val, off = _parse_value(body, 0)
    return val
