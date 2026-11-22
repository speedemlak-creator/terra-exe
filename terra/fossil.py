"""terra.fossil — Anı kalıcı kıl. Her çıktı, evrenin kanıtlanmış bir anısıdır."""
import hashlib
import json
import os
from datetime import datetime, timezone

def mint(seed, quakes, iss, kp, out_dir="fossils"):
    ts = datetime.now(timezone.utc)
    name = ts.strftime("fossil_%Y%m%d_%H%M%S")
    data = {
        "seed": seed,
        "utc": ts.isoformat(),
        "kp_index": kp,
        "iss": iss,
        "earthquake_count_24h": len(quakes),
        "strongest_quake": max(quakes, key=lambda q: q["mag"] or 0) if quakes else None,
    }
    data["proof"] = hashlib.sha256(
        json.dumps(data, sort_keys=True).encode()).hexdigest()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return path, data
