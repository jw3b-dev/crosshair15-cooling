# Linux tuning/monitoring research — MSI Crosshair 15 B12UGSZ (i9-12900H / RTX 3070 Ti Laptop)

Target: Ubuntu 24.04.4, kernel 7.0.0-31-generic, X11, NVIDIA 595.84, BIOS E1583IMS.112, EC 1583EMS1.111.
Locally verified facts are marked **[local]**; everything else is from web sources with confidence ratings.

---

## 1. msi-ec / msi_wmi_platform

**[local]** `modinfo msi_ec` → out-of-tree DKMS module, version 0.13, from `/lib/modules/.../updates/dkms/msi-ec.ko.zst` — this machine is running the **BeardOverflow/msi-ec out-of-tree DKMS driver**, not an in-tree one. `msi_wmi_platform` is separately loaded as an **in-tree** driver (`intree: Y`, `docs.kernel.org/7.0/...`).

- **Claim:** For firmware `1583EMS1.105/.109/.110/.111` (Crosshair 15 B12UEZ/B12UGSZ, Pulse GL66 12U(E/G)K), msi-ec's config block is `CONF_G2_1`. Confirmed by fetching the raw source (`msi-ec.c`, lines ~1122-1230):
  - `shift_mode`: EC address `0xd2`, modes = `turbo=0xc4`, `eco=0xc2`, `comfort=0xc1`. **"sport" (0xc0) is NOT included in this config's mode table**, even though `0xc0` = `SM_SPORT_NAME` in ~10 other config blocks in the same file (e.g. lines 91,177,333,404,478,557,639,783,851,994).
  - `fan_mode`: EC address `0xd4`, modes = `auto=0x0d`, `silent=0x1d`, `advanced=0x8d`.
  - `cooler_boost`: EC address `0x98`, bit 7.
  - `cpu`: rt_temp @ `0x68`, rt_fan_speed @ `0x71`. `gpu`: rt_temp @ `0x80`, rt_fan_speed @ `0x89` (this config, unlike some others, does define GPU sensors — consistent with the observed `gpu/realtime_*` attributes).
  - Confidence: **high** — read directly from source, not summarized secondhand.
  - Source: https://raw.githubusercontent.com/BeardOverflow/msi-ec/main/msi-ec.c (verified via `curl`, grep for `1583EMS1`).

- **Claim / interpretation of `shift_mode = "unknown (192)"`:** 192 decimal = `0xc0` = the EC's real register value for **sport mode** (full clock/voltage, "default desktop mode") on this hardware family, but the CONF_G2_1 struct in the driver simply omits the sport entry, so the driver can't map it to a name and prints "unknown (192)" instead of "sport". This is very likely a hole/incomplete port for the Crosshair 15 B12UGSZ specifically (other Crosshair/Katana/Pulse configs elsewhere in the file do list sport). No GitHub issue was found reporting this exact string ("unknown (192)") for this model — issue #398 (MSI Crosshair 15 B12UEZ, closed via PR #405) is a support/EC-dump request but does not discuss shift_mode value 192 or a missing sport mode explicitly.
  - Confidence: **medium-high** for the register-meaning inference (0xc0=sport is a strong, repeated pattern in-source); **low** for "this is definitely why your unit shows 192" absent a matching issue/PR quote. Flag as version-dependent: driver v0.13 config table, could change in a later release.
  - Sources: msi-ec.c (as above); https://github.com/BeardOverflow/msi-ec/issues/398 (single-issue, does not confirm the specific symptom).

- **Custom fan curves:** msi-ec (both this config and generally) exposes only the three discrete `fan_mode` states (auto/silent/advanced) — **no 7-point/custom curve attribute exists in the current driver** for any model, this one included. `available_fan_modes` / `fan_mode` are the only relevant sysfs nodes. (One search result claimed the EC's "advanced" mode "allows defining custom 7-point fan curves written directly into EC registers" — this describes what the underlying EC hardware/Windows Dragon Center can do, **not** something msi-ec exposes as a Linux sysfs knob. Third-party tool `msi-fanctl` (YaxOFF/msi-fanctl) claims to add curve/profile control on top of msi-ec, unverified/low-adoption.)
  - Confidence: **high** that stock msi-ec has no curve attribute; **low** on msi-fanctl's actual capability (single small repo, not independently corroborated).
  - Sources: https://github.com/BeardOverflow/msi-ec/blob/main/README.md ; https://github.com/YaxOFF/msi-fanctl (unverified, single source).

- **How to set values:**
  ```
  echo advanced   | sudo tee /sys/devices/platform/msi-ec/fan_mode
  echo comfort    | sudo tee /sys/devices/platform/msi-ec/shift_mode   # eco/comfort/turbo confirmed valid for this config; "sport" not in the driver's table for this model even though EC reports it
  echo on         | sudo tee /sys/devices/platform/msi-ec/cooler_boost
  ```
  Confidence: **high** (matches observed `available_fan_modes`/`available_shift_modes` and README examples).

- **In-tree vs out-of-tree:** msi-ec as a whole is **not in mainline** except for the AC/battery charge-threshold bits (merged as generic `power_supply` charge control attributes around 6.4+). Everything else (shift_mode, fan_mode, cooler_boost, per-model EC tables) remains out-of-tree/DKMS only; the README explicitly warns "never mix with DKMS" (i.e., don't have a stale non-DKMS install alongside the DKMS one — not a warning against DKMS itself). Kernel 7.x has **not** absorbed the msi-ec driver; you are running the correct (only) option for full feature access.
  - Confidence: **medium** (README wording combined with search synthesis, not independently re-verified against the exact current README text for the DKMS sentence).
  - Source: https://github.com/BeardOverflow/msi-ec/blob/main/README.md

- **msi_wmi_platform (in-tree, kernel 6.10+):** Exposes fan RPM via hwmon (`Get_Fan()` WMI method, RPM = 480000/reading) — matches the observed `fan1_input`/`fan2_input` under its hwmon node. As of the kernel 7.0 docs tree, it does **not** yet expose `platform_profile` or fan-curve control in shipped/merged form — those are the subject of an **unmerged** LKML patch series ("[PATCH v1 00/10] platform/x86: msi-wmi-platform: Add fan curves/platform profile/tdp/battery limiting", Armin Wolf, May 2025), where Wolf himself states fan-curve support "needs to be disabled by default and requires quirk support, as it is not supported on all models." No evidence this landed by kernel 7.0 (Sept 2026) — treat as **not yet available** on this system.
  - Confidence: **medium** (kernel docs confirm current scope; patch-series non-merge status inferred from lack of any "merged in 6.1x" confirmation across multiple searches — absence of evidence, not perfect proof).
  - Sources: https://docs.kernel.org/7.0/wmi/devices/msi-wmi-platform.html ; https://lkml.org/lkml/2025/5/19/69

- **Conflict between msi-ec and msi_wmi_platform:** Both talk to the **same underlying EC memory** — the kernel docs for msi-wmi-platform state plainly: "The underlying embedded controller interface is used by the `msi-ec` driver" (i.e., msi-wmi-platform's WMI methods are largely just EC-memory reads under the hood, same as msi-ec's direct EC I/O). A related LKML thread ("[PATCH 1/2] platform/x86: msi-wmi-platform: Only load on MSI devices", Nov 2025) discusses tightening msi-wmi-platform's DMI/GUID matching specifically because its WMI GUID isn't unique to MSI and can misfire on non-MSI hardware — this is about *false loading on other vendors' laptops*, not specifically about msi-ec+msi-wmi-platform racing each other on the same MSI machine. No source explicitly documents observed corruption/races from running both simultaneously on a real MSI unit; your observed setup (both loaded, both giving sane readings) suggests read-only access from both doesn't visibly conflict in practice, but **writes from both drivers to the EC concurrently are unverified as safe**.
  - Confidence: **medium** (shared-EC-access fact is documented; actual write-write conflict risk is inferred, not demonstrated).
  - Sources: https://docs.kernel.org/7.0/wmi/devices/msi-wmi-platform.html ; https://lkml.iu.edu/2511.1/01820.html ; https://github.com/BeardOverflow/msi-ec/issues/108

---

## 2. GUI/CLI control tools

| Tool | Status (2026) | Notes | Confidence |
|---|---|---|---|
| **MControlCenter** (dmitry-s93/MControlCenter) | Actively maintained; repo content dated as recently as Jul 2026; package `mcontrolcenter-bin` | Since v0.5.0 it rides on the kernel/DKMS msi-ec driver rather than shipping its own EC logic — so your device support is gated purely by msi-ec's CONF_G2_1 table (see §1), including the missing "sport" label. Ubuntu 24.04 is in its test matrix (via the related MsiController project). | medium — synthesized from search snippets, not the repo's actual CI config file |
| **msi-perkeys** | No independent confirmation found of an actively maintained project by this exact name for per-key RGB on this chassis; searches surfaced MControlCenter/MsiController/msi-ec instead | Likely conflated with MSI per-key keyboard tools for different chassis (Katana/Vector) with RGB matrix; the Crosshair 15 B12UGSZ per your platform attrs only exposes `leds`/single-zone kbd backlight (`msiacpi::kbd_backlight`, 0-3 levels), consistent with msi-ec's `kbd_bl` struct (bl_modes 0x00/0x08, max_state 3) — i.e. **no per-key RGB matrix support is exposed by msi-ec for this model**, so a per-key tool would have nothing to control here regardless of its maintenance status. | low on the tool's existence/status; medium-high on "this laptop's EC exposes single-zone, not per-key, backlight" (from msi-ec.c kbd_bl struct read directly) |
| **MSI-EC-GUI** | Referenced only as a generic "GUI interface to msi-ec" in search snippets; no separate strong evidence of active 2026 maintenance distinct from MControlCenter | Treat as effectively superseded/duplicative of MControlCenter | low |
| **LACT** (ilya-zlobintsev/LACT) | Actively developed in 2026 (0.10.0 release covered by igorslab.de Aug 2026; GamingOnLinux Aug 2026 article on "more NVIDIA GPU overclocking options") | Does support NVIDIA, including on recent driver branches — power limit, clock offset (V/F curve moved to an offset model), and even hotspot/junction temperature via NvAPI (LACT is called out as "the only tool that surfaces hotspot via NvAPI" on Linux). "Voltage Boost" on NVIDIA is explicitly **not** a true manual voltage offset — it only widens headroom the driver/firmware already allow. No laptop-specific (RTX 30 mobile) success/failure report found — most 2026 coverage is desktop RTX 40/50 (Blackwell) tuning. **Unverified specifically for RTX 3070 Ti Laptop on driver 595.84.** | medium (general NVIDIA support, recent and active); low (mobile-GPU-specific behavior) |
| **CoreCtrl** | Actively developed, cross-desktop, works under both X11 and Wayland | NVIDIA support in CoreCtrl is historically AMD-first; no 2026 source found confirming meaningful NVIDIA power-limit/clock control (as opposed to AMD). Treat NVIDIA support as **limited/unverified** for this GPU. | low |
| **GreenWithEnvy (GWE)** | Still X11-only by design (needs the NV-CONTROL X extension) — a Wayland MR (#80) exists but is a draft/unmerged, and issue #125 tracking Wayland support remains open | Fine for your setup since you're on X11. No clear 2026 "still actively released" confirmation found (GitLab activity referenced is from open issues/MRs of unknown recency) — **treat GWE's own maintenance status as unverified**, only its X11-only requirement is well corroborated. | medium (X11 requirement); low (current maintenance cadence) |
| **nvidia-settings + Coolbits (X11)** | Works, is the standard mechanism | `sudo nvidia-xconfig -a --cool-bits=28` then `nvidia-settings -a [gpu:0]/GPUGraphicsClockOffsetAllPerformanceLevels=<MHz*2>` (or per-level `GPUGraphicsClockOffset[N]`). `GPUOverVoltageOffset` is reported **read-only on some GPUs** even with Coolbits=28 — true voltage control is often not exposed at all on modern NVIDIA driver branches (see §3). | medium |

---

## 3. NVIDIA on laptops (driver 595.84, RTX 3070 Ti Laptop)

- **`nvidia-smi -pl` on RTX 30 mobile:** Widely reported to return **"Changing power management limit is not supported for GPU"** (or silently reject) on laptop GPUs from around driver 535 onward — multiple forum threads across driver versions from 535 through current confirm NVIDIA locked out manual power-limit control specifically for **mobile (Optimus/MUXless)** GPUs, distinct from desktop cards where `-pl` still works. Given your driver is 595.84 (well past 535) and `nvidia-smi` already shows a *default* 115W with a *max* 140W (i.e. the driver knows the boost ceiling but you don't have write access to it directly), expect `-pl` to fail or be ignored.
  - Workarounds reported: enabling `nvidia-powerd.service` (lets Dynamic Boost ramp power under load, reportedly reaching 115–140W depending on device even though idle `nvidia-smi` shows a lower "current" limit) and ensuring a `balanced`/`performance` power profile via `tuned`/`power-profiles-daemon`. Rolling back to driver 525 has been reported (unreliable/unsupported, old thread) to restore `-pl`, not recommended.
  - Confidence: **medium-high** on the lockout being real and driver-version-dependent; **medium** on the nvidia-powerd workaround actually delivering full 140W boost (forum-report level evidence, not a vendor doc).
  - Sources: https://forums.developer.nvidia.com/t/rtx-3080-mobile-power-limit-shows-n-a-but-worked-before/254925 ; https://forums.developer.nvidia.com/t/changing-power-management-limit-is-not-supported-for-gpu-pascal-gtx1060-laptop-mobile-linux-555-nvidia-smi-powerlimit/298873 ; https://forums.developer.nvidia.com/t/power-limit-on-3000-mobile-series/193443 ; https://bbs.archlinux.org/viewtopic.php?id=302133

- **`nvidia-smi -lgc` (lock GPU clocks):** Also frequently reported as failing/ignored specifically on **laptop** GPUs ("the system reporting that the GPU doesn't support it… particularly common on laptop GPUs"), even though it works on many desktop cards. **Unverified specifically for your RTX 3070 Ti Laptop + 595.84** — you'll need to test it directly; expect a decent chance it's rejected.
  - Confidence: **medium** (consistent pattern across several forum threads, but no single authoritative statement of "RTX 30 mobile" as a blanket rule).
  - Source: https://forums.developer.nvidia.com/t/how-to-force-lock-sm-and-memory-clocks-on-rtx-5090-headless-linux/348794 (context on the command, not laptop-specific) plus general search synthesis.

- **GPU undervolt / clock-offset curve on Linux:** No true voltage-offset control exists via the standard NVIDIA Linux driver stack for Ampere-class GPUs — `GPUOverVoltageOffset` via nvidia-settings/Coolbits is commonly **read-only** ("not used"/rejected) despite `Coolbits=28`. Practical Linux "undervolting" for NVIDIA generally means a **clock-offset + power-limit combination** (raise/lower clock offset while capping power, exploiting the V/F curve rather than truly setting voltage) — this is exactly what LACT's newer "voltage boost"/offset-curve UI and manual `nvidia-settings -a GPUGraphicsClockOffset...` achieve, not literal mV control.
  - Confidence: **medium**.
  - Sources: https://forums.developer.nvidia.com/t/nvidia-rt3070-eth-oc-in-ubuntu20-04-nvidia-settings-a-gpugraphicsclockoffset-gpumemorytransferrateoffset-not-working/178687 ; https://forums.developer.nvidia.com/t/option-coolbits-is-not-used-optimus-enabled-laptop-running-an-rtx-2070-manjaro-linux/111771 ; https://github.com/NVIDIA/open-gpu-kernel-modules/discussions/236

- **`temperature.gpu.tlimit` / hotspot exposure:** Standard `nvidia-smi`/`nvidia-settings` on Linux expose only the **core** GPU temperature (`temperature.gpu`), **not** the junction/hotspot temperature — this is a well-known Linux-driver gap versus Windows tools (Afterburner/HWiNFO). LACT is the one Linux tool reported to surface hotspot temp, by calling **NvAPI** directly (not the public NVML path `nvidia-smi` uses), and that NvAPI hotspot path has mainly been validated on newer (Blackwell) parts per a live LACT GitHub issue — **unverified whether it correctly reports hotspot on an Ampere-mobile (GA104) part** like your 3070 Ti Laptop.
  - `temperature.gpu.tlimit` as a literal `nvidia-smi --query-gpu` field name was not independently confirmed to exist in current NVML; what does reliably exist is `temperature.gpu` plus slowdown/shutdown/target temps reported by `nvidia-smi -q`. Treat "`temperature.gpu.tlimit`" as **likely not a real query key** on your driver — verify locally with `nvidia-smi --help-query-gpu | grep -i tlimit`.
  - Confidence: **medium** (core-only exposure is well corroborated); **low** (whether the exact query key name exists) — **flag as needing local verification**.
  - Sources: https://github.com/ilya-zlobintsev/LACT/issues/1114 ; https://wiki.archlinux.org/title/NVIDIA/Tips_and_tricks ; https://nvidia.custhelp.com/app/answers/detail/a_id/3751/~/useful-nvidia-smi-queries

- **Running on iGPU with dGPU powered down (PRIME, X11):** Standard, well-documented path:
  1. Configure Xorg for **PRIME Render Offload**: an X screen driven by the Intel iGPU (`modesetting` driver) as the primary/boot display, with the NVIDIA GPU available as an offload-only "GPU screen" (X.org ≥1.20.7 auto-enables GPU screens; your BIOS must boot to iGPU-driven display, i.e. Optimus/MSHybrid mode not "Discrete-only" in BIOS).
  2. Launch specific apps on the dGPU on demand with `__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia <app>`.
  3. With **Dynamic Power Management** (`nvidia` driver's runtime PM, `/proc/driver/nvidia/gpus/.../power` showing `Runtime D3 status: Enabled`), the dGPU should autosuspend to D3cold when no offloaded app is running.
  - This is explicitly an **X11** mechanism (PRIME render offload docs are X-server-specific); Wayland compositors use a different, less mature "explicit sync"/GBM-based offload path with historically patchier runtime-PM behavior — since you're on X11 this is not a concern, but don't assume the same setup transfers if you later move to Wayland.
  - Confidence: **medium-high** (standard, long-documented NVIDIA feature); exact autosuspend reliability is hardware/BIOS-dependent and **unverified for this specific 1583/E1583IMS.112 BIOS**.
  - Sources: https://download.nvidia.com/XFree86/Linux-x86_64/450.57/README/primerenderoffload.html ; https://wiki.archlinux.org/title/PRIME ; https://bbs.archlinux.org/viewtopic.php?id=250844

---

## 4. Intel 12th-gen (Alder Lake-H) undervolting

- **Voltage-offset MSR 0x150 lock (Plundervolt):** After the 2019 Plundervolt disclosure, Intel introduced a firmware-level lock ("CFG Lock") for MSR 0x150 writes; most OEM laptop BIOSes since ship with this lock **enabled by default**, hiding or disabling the undervolt UI entirely. This applies broadly across Comet Lake/Tiger Lake/Alder Lake/Raptor Lake-H mobile parts, MSI included.
  - Confidence: **high** (broad, repeated, cross-source corroboration — Arch forums, Overclockers forum, multiple undervolt-tool project pages).
- **MSI hidden BIOS menu (Right Ctrl+Right Shift+Left Alt+F2):** Confirmed as the standard key-combo to unlock MSI's "Advanced"/hidden BIOS mode across many MSI models (multiple forum threads corroborate the exact combo). Once in Advanced mode, the relevant toggles are typically under **OC → CPU Lock Configuration**: "Overclocking Lock", "CFG Lock", "Undervolt Protection" — disabling these is reported (single-source-level detail, not vendor-documented) to expose the voltage-offset MSR to OS writes.
  - **Not independently confirmed for the specific 1583 BIOS (E1583IMS.112)** whether this hidden menu (a) exists at all on this exact SKU/region BIOS, and (b) actually contains those three toggles rather than being locked/grayed-out regardless (some OEMs leave the menu items visible but non-functional, a pattern seen on other Plundervolt-mitigated laptops). One report (Linux Mint forum, MSI GP65 + i7-10750H) shows undervolting appearing to work but causing **random reboots** — i.e. even where the lock is bypassed, stability is not guaranteed, and that's a *different* chassis/CPU generation (Comet Lake, not Alder Lake).
  - Confidence: **medium** for menu existence in general on MSI boards; **low** for it working/being present specifically on 1583/E1583IMS.112 and for Alder Lake in particular — **flag as unverified for this firmware**.
  - Sources: https://forums.tomshardware.com/threads/voltage-control-suddenly-disabled-on-msi-laptop.3822367/ ; https://forums.linuxmint.com/viewtopic.php?t=456082 ; https://www.notebookcheck.net/XMG-reintroduces-BIOS-based-undervolting-on-laptops-with-Intel-Raptor-Lake-CPUs.708045.0.html (notable: as of this article, even XMG — a vendor known for unlocked BIOSes — had to specifically *reintroduce* undervolting for Raptor Lake, implying it's the exception, not the rule, industry-wide on 12th/13th gen).

- **`intel-undervolt` / `undervolt` (georgewhewell) on Linux post-unlock:** Both tools work by writing MSR 0x150 (same mechanism as Windows ThrottleStop) — if the BIOS lock is genuinely disabled, these tools should function on Alder Lake the same as on older generations; if CFG Lock is re-asserted (some BIOSes re-lock it every boot regardless of the setting, or the setting doesn't actually address the newer microcode-level restriction), writes will silently no-op or `rdmsr 0x150` will read back 0/unchanged. A 2024 writeup ("Unlocking Intel processors for CPU undervolting from Linux") documents a broader unlock methodology (NVRAM/BIOS variable patching akin to the `UnderVolter` project's approach) implying stock BIOS toggles alone are not always sufficient on newer platforms.
  - No 2025-2026-dated report found of anyone specifically undervolting an Alder Lake-H **MSI Crosshair 15** via these tools — **flag as unverified for this exact machine/generation combo**.
  - Confidence: **medium** (tool mechanism is well understood); **low** (real-world success on Alder Lake-H specifically, and on this chassis).
  - Sources: https://github.com/georgewhewell/undervolt ; https://code-dev.fixnum.org/2024-11-16-intel-cpu-undervolt-unlock/ ; https://github.com/wesmar/UnderVolter

---

## 5. RAPL on Linux (PL1=30W / PL2=45W observed)

**[local]** Confirmed: `intel-rapl:0` exposes `constraint_0` (long_term = PL1), `constraint_1` (short_term = PL2), and `constraint_2` (peak_power) — writable via `constraint_N_power_limit_uw` (microwatts) and `constraint_N_time_window_us`. thermald is active (adaptive mode: `--adaptive` flag present in the running process). `intel_pstate` is in `active` mode; governor `powersave`; `energy_performance_preference` currently `performance`. `msr`/`intel_rapl_msr`/`intel_rapl_common` modules are loaded (root/msr access available for turbostat).

- **Writing the powercap files directly:** `sudo sh -c 'echo 30000000 > /sys/class/powercap/intel-rapl:0/constraint_0_power_limit_uw'` (and `constraint_1_power_limit_uw` for PL2) works at the kernel level, but is **not persistent** across reboots/suspend and can be **overwritten by userspace daemons or by the EC/BIOS reasserting its own limits**.
- **thermald reasserting/overriding RAPL:** thermald actively manages RAPL/PowerClamp/cpufreq as one of its cooling mechanisms and can re-clamp a manually-set PL1/PL2 back to its own policy. `thermal-conf.xml` supports a `<PPCC>`-like power-limit section (`PowerLimitMaximum`, `PowerLimitMinimum`, `TimeWindowMinimum/Maximum`, `StepSize`) you can define per-platform to change what thermald itself will clamp to; alternatively, disabling thermald (`sudo systemctl disable --now thermald`) removes its interference entirely, at the cost of losing Intel's official DTS-based thermal management — the general community recommendation when *not* disabling it is to set your desired PL1 very high (rather than truly "disable" RAPL) so thermald's own ceiling, not a stale low value, is what binds.
  - Confidence: **medium** (thermal-conf.xml PPCC-equivalent behavior corroborated by the Arch/manpage-level docs; specific claim that thermald "re-clamps" a manual write mid-session is a reasonable inference from its documented adaptive-control loop rather than a directly observed/quoted bug report).
  - Sources: https://man.archlinux.org/man/extra/thermald/thermal-conf.xml.5.en ; https://github.com/intel/thermal_daemon ; https://bugs.launchpad.net/ubuntu/+source/thermald/+bug/1940485 (documents thermald "often limits CPU frequency while on AC" — real-world friction with thermald's own defaults, Ubuntu-specific bug).
- **MSI EC / Intel DPTF / PPCC reassertion:** No direct source found describing the MSI EC itself independently re-asserting PL1/PL2 outside of thermald's DPTF-driven policy (DPTF and thermald overlap in role; Ubuntu typically runs thermald, not a separate DPTF daemon, for this purpose) — **flag as unverified**: whether MSI firmware has an out-of-band (SMM/EC) power-limit re-assertion independent of what the OS's thermal daemon does was not confirmed either way in available sources.
- **Persisting RAPL settings / governor / EPB via systemd or TLP/auto-cpufreq:**
  - A simple persistence approach: a small systemd oneshot service (`ExecStart=/bin/sh -c 'echo ... > .../constraint_0_power_limit_uw'`) run `After=multi-user.target` on boot and (ideally) on resume-from-suspend (`systemd-sleep` hook), since RAPL limits don't survive a full power cycle.
  - **TLP** can set `CPU_ENERGY_PERF_POLICY_ON_AC/BAT` (i.e. `energy_performance_preference`) directly; **auto-cpufreq does not** manage EPP/EPB the same way and instead dynamically drives the governor based on load — **do not run TLP and auto-cpufreq together**, they fight over the same governor/frequency controls.
  - `intel_pstate=active` + HWP available (true on Alder Lake) means writing `scaling_governor` powersave/performance is actually translated into an EPP hint to the CPU's autonomous P-state controller, not a literal frequency clamp — this is the mechanism behind `energy_performance_preference`.
  - Confidence: **medium** (TLP/auto-cpufreq conflict and intel_pstate/HWP/EPP relationship are ArchWiki-level well-established facts; the specific "systemd oneshot for RAPL persistence" pattern is a standard community idiom, not something drawn from a single canonical doc).
  - Sources: https://linrunner.de/tlp/settings/processor.html ; https://wiki.archlinux.org/title/CPU_frequency_scaling ; https://github.com/AdnanHodzic/auto-cpufreq/issues/9
- **Disabling turbo / capping frequency, cpupower usage:**
  ```
  sudo cpupower frequency-set -g powersave          # set governor
  sudo cpupower frequency-set -u 3.0GHz             # cap max freq (all cores)
  echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo   # disable turbo (intel_pstate specific)
  cpupower frequency-info                            # inspect current state
  ```
  Confidence: **high** (standard, stable cpupower/intel_pstate interface).

---

## 6. Stress/monitor tooling

- **stress-ng, 10-minute CPU thermal soak:**
  ```
  stress-ng --cpu 0 --cpu-method all --timeout 10m --metrics-brief --tz
  ```
  `--cpu 0` = spawn one stressor per online CPU (i.e., saturate all 20 logical threads on the 12900H); `--cpu-method all` cycles through its bundled compute kernels rather than one fixed pattern; `--timeout 10m` bounds the soak; `--metrics-brief` prints a bogo-ops/throughput summary; `--tz` appends a thermal-zone temperature report at the end. Add `--times` for a resource-usage summary. Confidence: **high** (stable, documented CLI, matches Debian/Ubuntu manpage and multiple 2026 how-tos).
  Source: https://manpages.debian.org/testing/stress-ng/stress-ng.1.en.html ; https://wiki.ubuntu.com/Kernel/Reference/stress-ng

- **s-tui:** Terminal UI (curses) that live-charts CPU frequency, temperature, and power (via RAPL) while optionally driving stress-ng itself as the load generator; typically needs to be run with elevated privileges (or the user in appropriate groups) to read RAPL energy counters and MSR-backed temperature/frequency data reliably — **treat "needs root" as generally true but not independently re-confirmed against current s-tui release notes in this session** (no direct source fetched for s-tui specifically; this is carried over from well-known community practice, not a quoted doc). Confidence: **low-medium**.

- **turbostat:** Requires root (reads MSRs directly, hence the `msr` kernel module — **[local]** confirmed loaded: `msr`, `intel_rapl_msr`, `intel_rapl_common`). Typical soak-monitoring invocation: `sudo turbostat --interval 5` while the stress-ng run is active, to watch package power (PkgWatt), core/package temps, frequency, and C-state residency. Confidence: **high** (standard, well-known tool behavior; msr module presence verified locally).

- **GPU soak tools on Linux:**
  - **glmark2** — OpenGL benchmark, usable as a light/medium GPU load generator, packaged in Ubuntu repos; not a dedicated "burn-in" tool (lower sustained power draw than a true stress tool).
  - **vkmark** — Vulkan analogue of glmark2; similarly benchmark-oriented rather than max-power stress.
  - **Unigine (Superposition/Heaven/Valley)** — proprietary, higher and more sustained GPU load, good thermal-soak candidate, requires separate download (not in standard apt repos).
  - **FurMark (Linux/"GPU Burner", FurMark 2)** — now natively cross-platform with a Vulkan/OpenGL Linux build; explicitly designed as a worst-case power/thermal stress tool ("infinite falling donut" scene) — closest Linux analogue to the classic Windows FurMark for actually hitting thermal/power limits.
  - **nvtop** — ncurses live monitor (like htop) for GPU utilization/memory/temperature/power; supports NVIDIA (and AMD/Intel) — use alongside any of the above as the "what's actually happening" view. Available via apt on Ubuntu 24.04.
  - Confidence: **medium** (general tool descriptions well corroborated across multiple roundup articles; no source specifically validated FurMark2-Linux or vkmark against an RTX 3070 Ti Laptop + 595.84 combination — **unverified for this exact GPU/driver**).
  - Sources: https://www.pcsuggest.com/gpu-benchmarking-and-stress-testing-in-linux/ ; https://ubuntuhandbook.org/index.php/2024/11/benchmark-stress-test-gpu/ ; https://linuxvox.com/blog/gpu-stress-test-linux/

- **`package_throttle_count` as "the" throttling indicator:** **[local]** confirmed present at `/sys/devices/system/cpu/cpu0/thermal_throttle/package_throttle_count` (alongside `core_throttle_count`, `core_throttle_max_time_ms`, `package_throttle_max_time_ms`, `core_throttle_total_time_ms`, `package_throttle_total_time_ms`). It counts transitions of the package-level **PROCHOT/thermal-status flag** (i.e., the CPU actually hit its thermal trip point and hardware-throttled) — a real, meaningful, and simple signal, but it is **not** the right indicator for **RAPL power-limit (PL1/PL2) throttling**, which can clamp frequency well before any thermal trip fires and does **not** increment this counter. For power-limit-specific throttling, `turbostat`'s reported package power vs. your configured PL1/PL2, or reading the "power limit" reason bits via `MSR_CORE_PERF_LIMIT_REASONS` (not exposed as a friendly sysfs file), are the more accurate signals. So: **use `package_throttle_count` for "did the CPU thermally trip," not for "is RAPL power-capping me" — those are different mechanisms.**
  - Confidence: **high** on the counter's documented meaning (kernel docs); **medium** on the "RAPL throttling won't show here, use turbostat instead" guidance (reasonable inference from how RAPL and thermal-status-flag throttling are architecturally distinct, not from a single explicit doc stating this contrast).
  - Sources: https://docs.kernel.org/admin-guide/thermal/intel_thermal_throttle.html

---

## Unverified for this firmware (E1583IMS.112 / 1583EMS1.111)

- Whether the MSI hidden BIOS menu (Right Ctrl+Right Shift+Left Alt+F2) even exists on this exact BIOS build, and whether its OC Lock/CFG Lock/Undervolt Protection toggles are functional (vs. present-but-ineffective) on this SKU.
- Whether `intel-undervolt`/`undervolt` actually take effect on this CPU after any BIOS unlock (no Alder-Lake-H + Crosshair-15-specific report found).
- Whether running msi-ec and msi_wmi_platform simultaneously causes any real-world write conflict on EC registers on this specific board (only theoretical/shared-interface risk documented).
- Whether the exact `shift_mode` "unknown (192)" symptom has a filed, confirmed GitHub issue/PR for this model (inferred from source code, not from a matching bug report).
- Whether LACT's NVIDIA power-limit/clock-offset/hotspot-via-NvAPI features actually work correctly on an Ampere-mobile (GA104, RTX 3070 Ti Laptop) part specifically, vs. the Blackwell/desktop parts most 2026 coverage discusses.
- Whether `nvidia-smi -pl` / `-lgc` are hard-rejected or partially honored on this specific unit/driver-595.84 combination (pattern is well established for "laptop GPUs" broadly, not this exact card/driver tested).
- Whether `nvidia-smi --query-gpu` on driver 595.84 actually has a `temperature.gpu.tlimit` key at all (recommend running `nvidia-smi --help-query-gpu | grep -i tlimit` locally to confirm/deny).
- Whether MSI's EC/firmware independently re-asserts RAPL PL1/PL2 outside of thermald's own DPTF-style policy loop.
- s-tui's actual root/capability requirements on current Ubuntu 24.04 packaging (not independently re-checked against current release notes).
- FurMark2/vkmark real-world behavior on this specific RTX 3070 Ti Laptop + 595.84 combination.

---

## Sources

1. https://github.com/BeardOverflow/msi-ec (repo)
2. https://raw.githubusercontent.com/BeardOverflow/msi-ec/main/msi-ec.c (source, fetched directly and grepped for `1583EMS1`)
3. https://github.com/BeardOverflow/msi-ec/blob/main/README.md
4. https://github.com/BeardOverflow/msi-ec/issues/398
5. https://github.com/BeardOverflow/msi-ec/issues/108
6. https://github.com/BeardOverflow/msi-ec/discussions/277
7. https://docs.kernel.org/7.0/wmi/devices/msi-wmi-platform.html
8. https://lkml.org/lkml/2025/5/19/69 (Armin Wolf, msi-wmi-platform fan-curve/platform-profile/tdp/battery patch series)
9. https://lkml.iu.edu/2511.1/01820.html (msi-wmi-platform DMI/GUID matching discussion)
10. https://www.phoronix.com/news/MSI-WMI-Platform-Driver-Linux
11. https://github.com/dmitry-s93/MControlCenter
12. https://github.com/YaxOFF/msi-fanctl
13. https://www.igorslab.de/en/lact-0-10-0-nvidia-tuning-linux-voltage-boost-gddr7-temperatures/
14. https://www.gamingonlinux.com/2026/08/linux-gpu-configuration-and-monitoring-tool-lact-adds-more-nvidia-gpu-overclocking-options/
15. https://github.com/ilya-zlobintsev/LACT/issues/1114
16. https://gitlab.com/leinardi/gwe/-/merge_requests/80
17. https://gitlab.com/leinardi/gwe/-/issues/125
18. https://forums.developer.nvidia.com/t/rtx-3080-mobile-power-limit-shows-n-a-but-worked-before/254925
19. https://forums.developer.nvidia.com/t/changing-power-management-limit-is-not-supported-for-gpu-pascal-gtx1060-laptop-mobile-linux-555-nvidia-smi-powerlimit/298873
20. https://forums.developer.nvidia.com/t/power-limit-on-3000-mobile-series/193443
21. https://bbs.archlinux.org/viewtopic.php?id=302133
22. https://forums.developer.nvidia.com/t/how-to-force-lock-sm-and-memory-clocks-on-rtx-5090-headless-linux/348794
23. https://forums.developer.nvidia.com/t/nvidia-rt3070-eth-oc-in-ubuntu20-04-nvidia-settings-a-gpugraphicsclockoffset-gpumemorytransferrateoffset-not-working/178687
24. https://forums.developer.nvidia.com/t/option-coolbits-is-not-used-optimus-enabled-laptop-running-an-rtx-2070-manjaro-linux/111771
25. https://github.com/NVIDIA/open-gpu-kernel-modules/discussions/236
26. https://download.nvidia.com/XFree86/Linux-x86_64/450.57/README/primerenderoffload.html
27. https://wiki.archlinux.org/title/PRIME
28. https://bbs.archlinux.org/viewtopic.php?id=250844
29. https://forums.tomshardware.com/threads/voltage-control-suddenly-disabled-on-msi-laptop.3822367/
30. https://forums.linuxmint.com/viewtopic.php?t=456082
31. https://www.notebookcheck.net/XMG-reintroduces-BIOS-based-undervolting-on-laptops-with-Intel-Raptor-Lake-CPUs.708045.0.html
32. https://github.com/georgewhewell/undervolt
33. https://code-dev.fixnum.org/2024-11-16-intel-cpu-undervolt-unlock/
34. https://github.com/wesmar/UnderVolter
35. https://man.archlinux.org/man/extra/thermald/thermal-conf.xml.5.en
36. https://github.com/intel/thermal_daemon
37. https://bugs.launchpad.net/ubuntu/+source/thermald/+bug/1940485
38. https://linrunner.de/tlp/settings/processor.html
39. https://wiki.archlinux.org/title/CPU_frequency_scaling
40. https://github.com/AdnanHodzic/auto-cpufreq/issues/9
41. https://manpages.debian.org/testing/stress-ng/stress-ng.1.en.html
42. https://wiki.ubuntu.com/Kernel/Reference/stress-ng
43. https://www.pcsuggest.com/gpu-benchmarking-and-stress-testing-in-linux/
44. https://ubuntuhandbook.org/index.php/2024/11/benchmark-stress-test-gpu/
45. https://linuxvox.com/blog/gpu-stress-test-linux/
46. https://docs.kernel.org/admin-guide/thermal/intel_thermal_throttle.html
