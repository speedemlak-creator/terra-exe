# TERRA.EXE

> You don't run this program. **The planet does.**

TERRA.EXE is a program with no user input. Its input device is **Earth itself**:

- **Earthquakes** (USGS, live) — the clock cycles of the machine
- **The Sun** (NOAA planetary K-index) — the entropy source
- **The ISS** (live telemetry) — the cursor drifting across the sky

Every execution produces a **fossil**: a cryptographically hashed proof
(SHA-256) of the exact state of the planet at that moment, plus a
generative portrait and a melody derived from the same seed.
No two fossils can ever be identical — because the planet is never
in the same state twice.

## Run it

python3 main.py

Zero dependencies. Pure Python standard library.

## Output

Every run mints two files in `fossils/`:

- `fossil_<timestamp>.json` — the seed, live planetary data, and its proof hash
- `fossil_<timestamp>.svg` — the planet's portrait at that exact second

## The philosophy

Software has always been written *by* humans *for* humans.
TERRA.EXE asks: what if the universe is the author?

The repository itself is alive: a GitHub Action re-runs the program
every hour and commits the new fossil. The git history is a growing
archive of moments that will never happen again.

## Roadmap

- [x] Planetary seed engine (quakes + solar wind + ISS)
- [x] Fossil minting with SHA-256 proof
- [x] Generative portrait (SVG)
- [ ] MIDI output of the planet's melody
- [ ] Seismic clock: program advances one step per earthquake
- [ ] LIGO gravitational-wave interrupts
- [ ] Live README: this page updates itself hourly

## License

MIT. The planet remains the original author.
