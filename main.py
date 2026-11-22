#!/usr/bin/env python3
"""TERRA.EXE — Sen bu programı çalıştırmazsın. Gezegen çalıştırır.

Kullanım:  python3 main.py
Çıktılar:  fossils/ klasörü (JSON kanıt + SVG portre)
"""
from terra import sensors, engine, fossil

def main():
    print(">> Gezegene bağlanılıyor...")
    quakes = sensors.earthquakes()
    iss = sensors.iss_position()
    kp = sensors.space_weather()
    print(f">> Son 24 saatte {len(quakes)} deprem algılandı.")
    print(f">> ISS şu an: {iss['lat']:.2f} enlem, {iss['lon']:.2f} boylam.")
    print(f">> Güneş fırtınası (Kp): {kp['kp_index']}")

    seed = engine.build_seed(quakes, iss, kp)
    print(f">> Evrensel tohum: {seed[:24]}...")

    melody = engine.notes(seed)
    print(f">> Gezegenin melodisi (MIDI): {melody}")

    path, data = fossil.mint(seed, quakes, iss, kp)
    art = engine.svg(seed, quakes, kp["kp_index"])
    art_path = path.replace(".json", ".svg")
    with open(art_path, "w") as f:
        f.write(art)

    print(f">> Fossil kazındı: {path}")
    print(f">> Portre: {art_path}")
    print(f">> Kanıt (SHA-256): {data['proof'][:32]}...")
    print(">> Bu an bir daha asla üretilemeyecek. Gezegen ilerledi.")

if __name__ == "__main__":
    main()
