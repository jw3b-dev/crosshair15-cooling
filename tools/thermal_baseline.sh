#!/usr/bin/env bash
# thermal_baseline.sh — log laptop thermals to CSV every N seconds; summary on Ctrl-C.
# Usage: ./thermal_baseline.sh [interval_s] [label]
#   sudo ./thermal_baseline.sh 2 after-repaste   # sudo only needed for RAPL package watts
# Output: logs/thermal_<label>_<YYYYmmdd-HHMMSS>.csv  (nothing is printed per sample)
set -u

INTERVAL="${1:-2}"
LABEL="${2:-baseline}"
DIR="$(cd "$(dirname "$0")/.." && pwd)/logs"
mkdir -p "$DIR"
OUT="$DIR/thermal_${LABEL}_$(date +%Y%m%d-%H%M%S).csv"

# --- locate sensors -------------------------------------------------------
hw() { for h in /sys/class/hwmon/hwmon*; do [ "$(cat "$h/name" 2>/dev/null)" = "$1" ] && { echo "$h"; return; }; done; }
CT="$(hw coretemp)"
MSI="$(hw msi_wmi_platform)"
RAPL=/sys/class/powercap/intel-rapl:0/energy_uj
THR=/sys/devices/system/cpu/cpu0/thermal_throttle/package_throttle_count
PL1=/sys/class/powercap/intel-rapl:0/constraint_0_power_limit_uw
PL2=/sys/class/powercap/intel-rapl:0/constraint_1_power_limit_uw
GPU_OK=0; command -v nvidia-smi >/dev/null && GPU_OK=1
RAPL_OK=0; [ -r "$RAPL" ] && RAPL_OK=1

PKG_FILE=""; CORE_FILES=()
for l in "$CT"/temp*_label; do
  [ -e "$l" ] || continue
  n="$(cat "$l")"; i="${l%_label}_input"
  case "$n" in "Package id"*) PKG_FILE="$i" ;; Core*) CORE_FILES+=("$i") ;; esac
done

# --- header ---------------------------------------------------------------
{
  echo "# label=$LABEL interval=${INTERVAL}s host=$(hostname) kernel=$(uname -r)"
  echo "# PL1_W=$(( $(cat "$PL1" 2>/dev/null || echo 0) / 1000000 )) PL2_W=$(( $(cat "$PL2" 2>/dev/null || echo 0) / 1000000 )) rapl_readable=$RAPL_OK"
  echo "# msi-ec: shift=$(cat /sys/devices/platform/msi-ec/shift_mode 2>/dev/null) fan=$(cat /sys/devices/platform/msi-ec/fan_mode 2>/dev/null) boost=$(cat /sys/devices/platform/msi-ec/cooler_boost 2>/dev/null)"
  echo "time,pkg_c,core_min_c,core_max_c,core_spread_c,cpu_mhz,fan1_rpm,fan2_rpm,pkg_w,throttle_count,gpu_c,gpu_w,gpu_sm_mhz,gpu_util"
} > "$OUT"
echo "logging to $OUT  (Ctrl-C for summary)"

# --- sampling -------------------------------------------------------------
prev_e=""; prev_t=""
sample() {
  local pkg cmin cmax spread mhz f1 f2 pw thr g
  pkg=$(( $(cat "$PKG_FILE" 2>/dev/null || echo 0) / 1000 ))
  cmin=999; cmax=0
  for f in "${CORE_FILES[@]}"; do
    v=$(( $(cat "$f") / 1000 )); (( v < cmin )) && cmin=$v; (( v > cmax )) && cmax=$v
  done
  spread=$(( cmax - cmin ))
  mhz=$(awk '{s+=$1;n++} END{printf "%d", s/n/1000}' /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq 2>/dev/null)
  f1=$(cat "$MSI/fan1_input" 2>/dev/null || echo NA); f2=$(cat "$MSI/fan2_input" 2>/dev/null || echo NA)
  pw=NA
  if (( RAPL_OK )); then
    e=$(cat "$RAPL"); t=$(date +%s%N)
    [ -n "$prev_e" ] && pw=$(awk -v de=$((e-prev_e)) -v dt=$((t-prev_t)) 'BEGIN{printf "%.1f", de/1e6/(dt/1e9)}')
    prev_e=$e; prev_t=$t
  fi
  thr=$(cat "$THR" 2>/dev/null || echo NA)
  g="NA,NA,NA,NA"
  (( GPU_OK )) && g=$(nvidia-smi --query-gpu=temperature.gpu,power.draw,clocks.sm,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | tr -d ' ' || echo "$g")
  echo "$(date +%H:%M:%S),$pkg,$cmin,$cmax,$spread,$mhz,$f1,$f2,$pw,$thr,$g" >> "$OUT"
}

summary() {
  echo
  awk -F, '!/^#/ && NR>1 && $2+0>0 {
      n++; s+=$2; if($2>mx)mx=$2; if($5>sp)sp=$5; if($11+0>gm)gm=$11
      if(t0=="")t0=$10; t1=$10; if($9!="NA"){pw+=$9;pn++}
    } END {
      if(n==0){print "no samples"; exit}
      printf "samples=%d  pkg avg=%.1fC max=%dC  worst core spread=%dC  throttle delta=%d  gpu max=%dC", n, s/n, mx, sp, t1-t0, gm
      if(pn) printf "  pkg avg=%.1fW", pw/pn
      print ""
    }' "$OUT"
  echo "file: $OUT"
  exit 0
}
trap summary INT TERM

while :; do sample; sleep "$INTERVAL"; done
