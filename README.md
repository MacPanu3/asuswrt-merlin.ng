<div align="center">

# Asuswrt-Merlin Custom Build — ASUS RT-AX82U V1

**Personal fork of [GNUton's Asuswrt-Merlin](https://github.com/gnuton/asuswrt-merlin.ng) synced with upstream [RMerl/asuswrt-merlin.ng](https://github.com/RMerl/asuswrt-merlin.ng) (`3004.388.13`) and tailored specifically for the ASUS RT-AX82U V1.**

[![Latest Release](https://img.shields.io/github/v/release/MacPanu3/asuswrt-merlin.ng?label=latest%20release)](https://github.com/MacPanu3/asuswrt-merlin.ng/releases)
[![Build Status](https://github.com/MacPanu3/asuswrt-merlin.ng/actions/workflows/github-actions.yml/badge.svg?branch=ax82u-388.13-plus)](https://github.com/MacPanu3/asuswrt-merlin.ng/actions/workflows/github-actions.yml)

[Releases & Downloads](https://github.com/MacPanu3/asuswrt-merlin.ng/releases) · [Changelog](Changelog-NG.txt) · [Upstream Documentation](https://github.com/RMerl/asuswrt-merlin.ng/wiki/About-Asuswrt) · [SNBForums](https://www.snbforums.com/forums/asuswrt-merlin.42/)

</div>

---

## Target Hardware

- **Supported Model:** [ASUS RT-AX82U V1](https://www.asus.com/Networking-IoT-Servers/WiFi-6/All-series/RT-AX82U/) (`RT-AX82U` / `RTAX82U`, SDK `src-rt-5.02axhnd.675x`)
- **Active Branch:** `ax82u-388.13-plus`

> [!WARNING]
> This repository builds **only for RT-AX82U V1** (all other models in [`.github/workflows/github-actions.yml`](.github/workflows/github-actions.yml) are marked `skip: true`).
> Do **not** flash V1 images onto **RT-AX82U V2** (`5.04axhnd.675x`). Check your hardware revision via SSH (`nvram get productid` / `nvram get hw_ver`) or the router label before flashing.

---

## What Changed Since GNUton `3004.388.11_1-gnuton1`

### 1. Upstream RMerl Sync (`3004.388.12` → `3004.388.12_2` → `3004.388.13`)
- Synced upstream Asuswrt-Merlin `3004.388.13` onto GNUton's `3004.388.11_1-gnuton1` base:
  - OpenSSL 3.5 migration (with 1.1.1 / 1.0.0 compatibility shims for proprietary blobs).
  - GPL `388_25633` merge with weak-symbol compatibility for pre-`388_25633` RT-AX82U closed-source blobs.
  - Updated core components (`dnsmasq`, `miniupnpd`, `tor` with IPv6 support, `curl`, `wget`, `dropbear`, `amtm`, `zoneinfo`, `haveged`, DNSSEC `KSK-2024` trust anchor) and Dual WAN / WebUI / security fixes.

### 2. Custom RT-AX82U V1 Modifications & Backports (`3004.388.13_0-plus1`)
- **Permanent Front Aura RGB Disable:** Defaults `ledg_scheme` to `"0"` and updates `ledg` (`defaults.c`, `init.c`, `ledbtn.c`) so the front Aura RGB bar stays permanently off after boot and cancels its timer (`alarmtimer(0, 0)`) with zero CPU overhead, while keeping the 4 white top status LEDs functioning normally.
- **OpenVPN 2.7.9:** Backported from upstream RMerl `main` (memory scrubbing of auth tokens/keys).
- **CA Bundle Update:** Removed deprecated emSign signing keys (backported from RMerl `main`).
- **Linux 4.1 IPv4 Kernel Fix:** Frees `inet_opt` and `opt` after an RCU grace period in `af_inet.c` and `tcp_ipv4.c` (`CVE-2026-98432`).
- **wsdd2 Security Patches:** Backported LLMNR out-of-bounds read and WSD HTTP NULL-dereference DoS fixes from RMerl `3004.388`.
- **httpd UPnP XSS Guard:** Sanitizes UPnP IPv4/IPv6 lease text on status pages (RMerl PR #925).

See [Changelog-NG.txt](Changelog-NG.txt) for the full consolidated release notes.

---

## Automated CI & Releases

Firmware images are built in GitHub Actions via [`.github/workflows/github-actions.yml`](.github/workflows/github-actions.yml) using `gnuton/asuswrt-merlin-toolchains-docker:latest`.

Tagging a release (e.g. `3004.388.13_0-plus1`) automatically builds and publishes to [GitHub Releases](https://github.com/MacPanu3/asuswrt-merlin.ng/releases):
- Firmware image (`RT-AX82U_<version>_puresqubi.w`) and `.md5` checksum
- Release notes extracted from the top section of [Changelog-NG.txt](Changelog-NG.txt) via [`tools/get-last-notes.py`](tools/get-last-notes.py)

---

## Credits & Disclaimer

- **Upstream Asuswrt-Merlin:** [RMerl/asuswrt-merlin.ng](https://github.com/RMerl/asuswrt-merlin.ng) and contributors
- **GNUton's Fork & CI Toolchain:** [gnuton/asuswrt-merlin.ng](https://github.com/gnuton/asuswrt-merlin.ng)
- **ASUS:** GPL source code releases

> This is a personal custom firmware build provided as-is, with no warranty. Flash at your own risk.
