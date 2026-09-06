.PHONY: html check log install clean serve

html:            ## Render Cooling_Mod_Report.md -> site/index.html
	python3 tools/generate_html.py

check:           ## Verify the sensors and tools the logger relies on
	@for h in /sys/class/hwmon/hwmon*; do n=$$(cat $$h/name); case $$n in coretemp|msi_wmi_platform) echo "ok  $$n ($$h)";; esac; done
	@test -e /sys/devices/system/cpu/cpu0/thermal_throttle/package_throttle_count && echo "ok  package_throttle_count" || echo "!!  no throttle counter"
	@command -v nvidia-smi >/dev/null && echo "ok  nvidia-smi" || echo "--  nvidia-smi missing (GPU columns will be NA)"
	@test -r /sys/class/powercap/intel-rapl:0/energy_uj && echo "ok  RAPL readable" || echo "--  RAPL energy is root-only; run the logger with sudo for watts"
	@for t in stress-ng s-tui turbostat nvtop glmark2 sensors; do command -v $$t >/dev/null && echo "ok  $$t" || echo "--  $$t missing"; done

log:             ## Start a 2 s logger with LABEL=<name> (default baseline)
	tools/thermal_baseline.sh 2 $(or $(LABEL),baseline)

install:         ## Symlink the logger and comparer into ~/.local/bin
	mkdir -p $(HOME)/.local/bin
	ln -sf $(CURDIR)/tools/thermal_baseline.sh $(HOME)/.local/bin/thermal-baseline
	ln -sf $(CURDIR)/tools/compare_logs.py $(HOME)/.local/bin/thermal-compare
	@echo "installed thermal-baseline and thermal-compare into ~/.local/bin"

serve: html      ## Serve the rendered site on http://127.0.0.1:8765
	cd site && python3 -m http.server 8765 --bind 127.0.0.1

clean:
	rm -rf site

help:
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | sed 's/:.*##/\t/'
