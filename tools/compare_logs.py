#!/usr/bin/env python3
"""Compare two thermal_baseline.sh CSV logs (before vs after) and print the deltas.

Usage: compare_logs.py BEFORE.csv AFTER.csv
       compare_logs.py --selftest
"""
import csv
import sys
from statistics import mean

COLS = ["pkg_c", "core_spread_c", "cpu_mhz", "fan1_rpm", "fan2_rpm", "pkg_w", "gpu_c", "gpu_w", "gpu_sm_mhz"]


def load(path):
    rows = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            rows.append(line)
    data = list(csv.DictReader(rows))
    return [r for r in data if r.get("pkg_c") not in (None, "", "0")]


def stats(rows):
    out = {}
    for c in COLS:
        vals = []
        for r in rows:
            v = r.get(c, "NA")
            try:
                vals.append(float(v))
            except ValueError:
                pass
        out[c] = (mean(vals), max(vals)) if vals else None
    thr = [int(r["throttle_count"]) for r in rows if r.get("throttle_count", "NA").isdigit()]
    out["throttle_delta"] = (thr[-1] - thr[0]) if len(thr) > 1 else None
    out["samples"] = len(rows)
    return out


def report(a, b, na, nb):
    print(f"{'metric':<16}{'before':>14}{'after':>14}{'delta':>10}")
    print(f"{'samples':<16}{a['samples']:>14}{b['samples']:>14}")
    for c in COLS:
        if a[c] is None or b[c] is None:
            continue
        am, ax = a[c]
        bm, bx = b[c]
        print(f"{c + ' avg':<16}{am:>14.1f}{bm:>14.1f}{bm - am:>+10.1f}")
        print(f"{c + ' max':<16}{ax:>14.1f}{bx:>14.1f}{bx - ax:>+10.1f}")
    if a["throttle_delta"] is not None and b["throttle_delta"] is not None:
        print(f"{'throttle events':<16}{a['throttle_delta']:>14}{b['throttle_delta']:>14}{b['throttle_delta'] - a['throttle_delta']:>+10}")
    print(f"\nbefore: {na}\nafter:  {nb}")


def selftest():
    import io
    sample = "# header\ntime,pkg_c,core_min_c,core_max_c,core_spread_c,cpu_mhz,fan1_rpm,fan2_rpm,pkg_w,throttle_count,gpu_c,gpu_w,gpu_sm_mhz,gpu_util\n"
    a = sample + "1,90,60,90,30,2000,6800,6200,NA,100,45,25,800,10\n2,92,61,92,31,2100,6800,6200,NA,140,45,25,800,10\n"
    b = sample + "1,70,60,72,12,3000,4000,3900,45.0,500,44,25,800,10\n2,71,60,73,13,3100,4000,3900,45.5,500,44,25,800,10\n"
    sa = stats(list(csv.DictReader(io.StringIO(a.split("\n", 1)[1]))))
    sb = stats(list(csv.DictReader(io.StringIO(b.split("\n", 1)[1]))))
    assert sa["pkg_c"][1] == 92 and sb["pkg_c"][1] == 71
    assert sa["throttle_delta"] == 40 and sb["throttle_delta"] == 0
    assert sa["pkg_w"] is None and sb["pkg_w"] is not None
    print("selftest ok")


def main(argv):
    if argv[1:] == ["--selftest"]:
        selftest()
        return 0
    if len(argv) != 3:
        print(__doc__)
        return 2
    a, b = load(argv[1]), load(argv[2])
    if not a or not b:
        print("no samples in one of the files")
        return 1
    report(stats(a), stats(b), argv[1], argv[2])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
