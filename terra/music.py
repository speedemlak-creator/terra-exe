"""terra.music — Gezegenin sesi.

Tohumdan üretilen melodiyi, deprem davullarını ve güneş temposunu
gerçek bir MIDI dosyasına yazar. Sıfır bağımlılık: MIDI binary
formatı doğrudan standart kütüphaneyle yazılır.
"""
import struct

def _varlen(n):
    """MIDI variable-length quantity."""
    out = [n & 0x7F]
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)

def _track(events):
    """events: [(delta_ticks, bytes), ...] -> track chunk."""
    body = b"".join(_varlen(d) + e for d, e in events)
    body += _varlen(0) + b"\xff\x2f\x00"  # end of track
    return b"MTrk" + struct.pack(">I", len(body)) + body

def write(path, melody, quakes, kp, ticks=480):
    """Melodi + deprem davulları + güneş temposundan .mid üret."""
    bpm = int(60 + kp * 12)          # fırtına arttıkça tempo hızlanır
    us_per_beat = int(60_000_000 / bpm)
    events = []
    # tempo meta-event
    events.append((0, b"\xff\x51\x03" + us_per_beat.to_bytes(3, "big")))
    # melodi: kanal 0, her nota 1 vuruş
    for n in melody:
        vel = 70 + (n % 30)
        events.append((0, bytes([0x90, n, vel])))
        events.append((ticks, bytes([0x80, n, 0])))
    # depremler: kanal 9 (davul), büyüklük = vuruş şiddeti
    for q in quakes[:16]:
        mag = q["mag"] or 1
        vel = min(127, int(30 + mag ** 2 * 6))
        events.append((0, bytes([0x99, 38, vel])))   # snare
        events.append((ticks // 2, bytes([0x89, 38, 0])))
    header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, ticks)
    with open(path, "wb") as f:
        f.write(header + _track(events))
    return path
