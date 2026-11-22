"""terra.engine — Sensör verisini evrensel tohuma çeviren motor.

Aynı gezegen durumu her zaman aynı çıktıyı üretir (deterministik).
Ama gezegen asla aynı durumda olmaz.
"""
import hashlib
import math
import json

def build_seed(quakes, iss, kp):
    """Gezegenin o anki parmak izi."""
    payload = json.dumps({"q": quakes, "iss": iss, "kp": kp},
                         sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()

def _bytes(seed, n):
    """Tohumdan deterministik olarak n bayt türet (zincirleme hash)."""
    out, block, i = b"", seed.encode(), 0
    while len(out) < n:
        out += hashlib.sha256(block + str(i).encode()).digest()
        i += 1
    return list(out[:n])

def notes(seed, count=16):
    """Tohumdan 16 notalık bir dizi üret."""
    scale = [0, 2, 3, 5, 7, 8, 10]  # minör pentatonik hissi
    b = _bytes(seed, count)
    base = 48  # MIDI C3
    return [base + scale[x % 7] + 12 * (x // 128) for x in b]

def _hsl(h, s, l):
    """hsl -> 'rgb(r,g,b)' (her yerde uyumlu olması için)."""
    import colorsys
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, l / 100.0, s / 100.0)
    return f"rgb({int(r*255)},{int(g*255)},{int(b*255)})"

def svg(seed, quakes, kp, size=800):
    """Tohumdan üretilen generatif görsel: gezegenin o anki portresi."""
    b = _bytes(seed, 32)
    hue = int((kp / 9.0) * 120 + 180) % 360  # fırtına arttıkça kızıllaşır
    parts = [f'<rect width="{size}" height="{size}" fill="{_hsl(hue, 30, 8)}"/>']
    for i, q in enumerate(quakes[:40]):
        x = (b[i % 32] / 255) * size
        y = (b[(i + 7) % 32] / 255) * size
        r = max(2.0, (q["mag"] or 1) ** 2 * (b[(i + 13) % 32] / 255 + 0.3))
        parts.append(
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="none" '
            f'stroke="{_hsl(hue + i * 9, 80, 60)}" stroke-width="1.4" '
            f'opacity="{0.35 + 0.6 * (b[(i + 3) % 32] / 255):.2f}"/>')
    pts = " ".join(
        f"{i / 79 * size:.0f},{size / 2 + math.sin(v / 255 * math.pi * 4) * size * 0.2:.0f}"
        for i, v in enumerate(_bytes(seed, 80)))
    parts.append(f'<polyline points="{pts}" fill="none" '
                 f'stroke="{_hsl(hue + 60, 90, 70)}" stroke-width="2" opacity="0.9"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">'
            + "".join(parts) + "</svg>")
