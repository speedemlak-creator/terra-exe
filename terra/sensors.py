"""terra.sensors — Gezegenin giriş aygıtları.

Her fonksiyon canlı, açık bir API'den veri çeker ve dict döner.
Hiçbir harici paket gerekmez: sadece standart kütüphane.
"""
import json
import urllib.request

def _get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": "terra-exe/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def earthquakes():
    """USGS: son 24 saatteki tüm depremler (büyüklük >= 2.5)."""
    d = _get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson")
    out = []
    for f in d["features"]:
        p, g = f["properties"], f["geometry"]["coordinates"]
        out.append({"mag": p["mag"], "place": p["place"],
                    "lon": g[0], "lat": g[1], "depth": g[2], "time": p["time"]})
    return out

def iss_position():
    """ISS'in şu anki konumu."""
    d = _get("https://api.wheretheiss.at/v1/satellites/25544")
    return {"lat": float(d["latitude"]),
            "lon": float(d["longitude"]),
            "altitude_km": float(d["altitude"]),
            "time": d["timestamp"]}

def space_weather():
    """NOAA: gezegenlerarası K indeksi (güneş fırtınası şiddeti)."""
    d = _get("https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json")
    last = d[-1]
    if isinstance(last, dict):
        return {"time": last["time_tag"], "kp_index": float(last["Kp"])}
    return {"time": last[0], "kp_index": float(last[1])}
