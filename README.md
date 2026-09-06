# crosshair15-cooling

Cooling modification guide and Linux thermal tooling for the **MSI Crosshair 15 B12UGSZ**
(i9-12900H, RTX 3070 Ti Laptop) running Ubuntu 24.04.

The guide covers four hardware mods with researched alternatives, a zero-hardware software
path, a decision matrix, and Linux-native tuning and validation to replace the usual
Windows tooling (MSI Center, ThrottleStop, HWiNFO64, Afterburner).

- **Read the guide:** [Cooling_Mod_Report.md](Cooling_Mod_Report.md), or the rendered site
  published by the Pages workflow.
- **Research digests** with per-claim confidence and source URLs: [research/](research/).

## Tooling

| Tool | What it does |
|---|---|
| `tools/thermal_baseline.sh` | Logs package/core temps, core spread, fan RPM, package watts, throttle count and GPU stats to a CSV every N seconds. Ctrl-C prints a summary. |
| `tools/compare_logs.py` | Compares two baseline CSVs (before/after a mod) and prints the deltas. |
| `tools/generate_html.py` | Renders the markdown guide to `site/index.html` (Tailwind, TOC, dark mode, print CSS). |
| `tools/rapl-limits.service` | systemd oneshot template that persists RAPL PL1/PL2 after boot. |

## Quick start

```bash
make check                      # sensors the logger needs are present
tools/thermal_baseline.sh 2 stock-idle      # log; Ctrl-C to stop
sudo tools/thermal_baseline.sh 2 after-mod4 # sudo unlocks package watts
tools/compare_logs.py logs/thermal_stock-idle_*.csv logs/thermal_after-mod4_*.csv
make html                       # build site/index.html
make install                    # symlink the logger into ~/.local/bin
```

Requirements: bash, awk, Python 3.10+ (stdlib only), `lm-sensors` and the `coretemp` and
`msi_wmi_platform` kernel drivers for fans, `nvidia-smi` for GPU columns. Optional:
`stress-ng`, `s-tui`, `turbostat`, `nvtop`, `glmark2` for the validation protocol.

## Safety

The guide documents commands that write to the embedded controller, RAPL power limits and
GPU clocks. Nothing in this repo runs them for you. Read Part 0 and the safety note in
Part 6b before stress testing a machine that already throttles at idle.

## Author

`~❯ JW3B._` Built by [John @ jw3b.dev](https://jw3b.dev) · [github.com/jw3b-dev](https://github.com/jw3b-dev)

`// STAY WEIRD 👽`

## License

**Code and documentation:** MIT, see [LICENSE](LICENSE). Research digests summarise
third-party sources; see each file's Sources list.

**Brand assets:** © 2026 John Wellard (jw3b.dev), all rights reserved. The `JW3B.` mark,
the `~❯ JW3B._` prompt treatment, the `// STAY WEIRD 👽` tagline and the header/footer
components in [brand/](brand/) are excluded from the MIT grant. See
[brand/LICENSE-BRAND.md](brand/LICENSE-BRAND.md). Forks must remove or replace them.
