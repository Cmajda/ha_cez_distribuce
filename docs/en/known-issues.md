# 🐛 Known Issues

This file contains a list of known issues and their resolution status.

---

## Current Issues (v3.0.0)

### 1. set_prices service doesn't distinguish devices

**Status:** ⚠️ Known limitation

**Description:** The `cez_hdo.set_prices` service (callable via Developer Tools → Services)
sets prices for all integration instances. It's not possible to specify which
device should have its prices updated.

**Workaround:** Use Options Flow in integration settings to change prices
(Settings → Devices & Services → ČEZ HDO → Configure).

**Planned fix:** Adding `device_id` or `entry_id` parameter to the service
for device-specific price setting.

---

## Archive of Resolved Issues (v3.0.0-RC.1)

> **Status:** All issues from v3.0.0-RC.1 were resolved in RC.2.

### Priority 1 - Critical

### ~~1. Sensors don't update in real-time~~ ✅

**Status:** ✅ Resolved

**Description:** Sensor states for time and active tariff binary sensors only change
when Home Assistant restarts. Data refresh needs to be more frequent
(ideally 1-2 sec for countdown), separate from API data fetching.

**Solution:** Added separate interval for state recalculation (5 seconds),
independent from API data fetching (1 hour).

**Reported by:** @micjon, @pokornyIt

---

### ~~2. UI card not registered~~ ✅

**Status:** ✅ Not a bug

**Description:** Frontend card is not registered in Lovelace, although the log
states it is registered.

**Solution:** Browser refresh required (Ctrl+F5 or Cmd+Shift+R) after HA restart.

**Reported by:** @pokornyIt

---

### ~~3. Cannot change VT/NT prices after setup~~ ✅

**Status:** ✅ Not a bug

**Description:** After initial integration setup, VT/NT prices cannot be changed.
Options flow doesn't work or is not available.

**Solution:** Steps to change prices:
Settings → Devices & Services → ČEZ HDO → Configure (gear icon) →
click through steps → last step is price settings.

Documented in [user-guide.md](user-guide.md#-price-settings).

**Reported by:** @pokornyIt

---

### ~~4. EAN in log - sensitive value~~ ✅

**Status:** ✅ Resolved

**Description:** EAN code is displayed in full in the log. If it's a sensitive
value, it should be masked (e.g., `859182400600xxxxx`).

**Solution:** Added helper functions `mask_ean()` and `ean_suffix()` in `const.py`.
EAN is now masked in logs as `***...XXXXXX` (showing last 6 digits).
Cache/price file names use only EAN suffix (last 6 digits).

**Reported by:** @pokornyIt

---

## Priority 2 - Medium

### ~~5. Multiple signals for one EAN - unintuitive entity names~~ ✅

**Status:** ✅ Resolved

**Description:** If EAN has multiple signals:

1. What name will the device have when adding multiple signals?
2. Entity names are unintuitive (e.g., `binary_sensor.cez_hdo_nizky_tarif_aktivni_1`)

**Solution:** Added new step in config flow for entity suffix input.

- Default suffix: `{EAN4}_{signal}` (e.g., `7606_a1b4dp04`)
- **User can enter custom suffix** (e.g., `cottage`, `apartment`, `house`)
- Entity IDs: `sensor.cez_hdo_lowtariffstart_{suffix}`
- Device: `ČEZ HDO 967606 (a1b4dp04)`
- Same EAN can be added multiple times with different signals

**Reported by:** @pokornyIt

---

### ~~6. Debug log contains emoji icon~~ ✅

**Status:** ✅ Resolved

**Description:** Debug log message contains emoji icon (🔴), which may
cause issues on some systems.

```log
# Before (with emoji)
2026-01-30 09:25:45 DEBUG ... 🔴 IN HIGH TARIFF: 06:15:00-14:10:00

# After (without emoji)
2026-01-30 09:25:45 DEBUG ... [VT] IN HIGH TARIFF: 06:15:00-14:10:00
```

**Solution:** Emojis replaced with text markers `[NT]` and `[VT]`.

**Reported by:** @pokornyIt

---

## Resolved

- **Issue #1:** Sensors don't update in real-time
- **Issue #2:** UI card not registered (browser refresh required)
- **Issue #3:** Cannot change VT/NT prices (documented in user-guide.md)
- **Issue #4:** EAN in log - masked to last 6 digits
- **Issue #5:** Multiple signals for EAN - device contains signal name
- **Issue #6:** Debug log contains emoji icon

---

## How to Report an Issue

1. Check if the issue is already in this list
2. Create a [GitHub Issue](https://github.com/Cmajda/ha_cez_distribuce/issues)
3. Attach diagnostics (Settings → Devices → ČEZ HDO → ⋮ → Download diagnostics)
