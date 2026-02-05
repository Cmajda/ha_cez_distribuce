# Release Notes – ČEZ HDO

---

## v3.1.1 (2026-02-05)

### 🐛 Fixes

#### Compatibility with Home Assistant 2026.02+

- **Fixed error** `'LovelaceData' object has no attribute 'mode'`
- In HA 2026.02+, the `LovelaceData` structure was changed – the object no longer has a `mode` attribute
- New storage mode detection using resources collection type check

**Fixes:** [#62](https://github.com/Cmajda/ha_cez_distribuce/issues/62)

---

## v3.1.0 (2026-02-04)

### 🚀 Main Changes

Version 3.1.0 brings **CAPTCHA verification support** and new sensors for tracking data validity.

#### CAPTCHA API Protection

- ČEZ Distribuce introduced CAPTCHA protection on their API
- **New configuration step** – displays CAPTCHA image and user enters the code
- Data is fetched once and stored in cache
- **Data validity 6 days** – reconfiguration required after expiry

#### New Entities for Data Validity Tracking

| Type   | Entity                        | Description            |
| ------ | ----------------------------- | ---------------------- |
| Binary | `cez_hdo_data_valid_*`        | Data is valid (on/off) |
| Sensor | `cez_hdo_data_valid_until_*`  | Expiry date            |
| Sensor | `cez_hdo_data_age_days_*`     | Data age in days       |
| Sensor | `cez_hdo_days_until_expiry_*` | Days until expiry      |

#### Automatic Notifications

- **Day 5:** Persistent notification with warning
- **Day 6:** Persistent notification about data expiry

### ✨ Improvements

- Better error handling for CAPTCHA validation
- Options Flow also supports CAPTCHA for data refresh
- Updated documentation with automation examples

### 📚 Documentation

- Added "Data Validity and Refresh" section to user-guide
- Updated known-issues with resolved CAPTCHA issue info
- Added automation examples for expiry notifications

---

## v3.0.1 (2026-02-03)

### 📚 Documentation

- Added CAPTCHA issue notice to README

---

## v3.0.0 (2026-02-02)

### 🚀 Main Changes

Version 3.0.0 brings a **complete redesign** of the integration
with focus on modern Home Assistant architecture.

#### Config Flow – GUI Configuration

- **No YAML** – integration is configured via Settings → Devices & Services
- **4-step wizard:**
  1. Enter EAN
  2. Select signal
  3. Entity suffix (user-configurable)
  4. Set NT/VT prices
- **Options Flow** – change settings anytime after installation
- **Multiple signals per EAN** – same EAN can be added multiple times with different signals

#### Device Registry

- All entities are grouped under a **hub** (last 6 digits of EAN)
- Each signal creates its own **device** with signal code
- Better overview in Home Assistant UI

#### New Data Storage

- Data moved from `www/cez_hdo/` to `custom_components/cez_hdo/data/`
- Migration happens automatically on first run
- Old data remains as backup (can be deleted manually)

#### Lovelace Card

- Automatic registration in Lovelace resources
- Visual editor with all options
- Display of tariff states, times, remaining time, current price
- 7-day HDO schedule

### ⚠️ Breaking Changes

- **YAML configuration removed** – delete from `configuration.yaml`
- **Entity IDs changed** – old automations need updates
- **Folder structure changed** – `www/cez_hdo/` no longer used

### 📚 Documentation

- Complete user-guide rewrite
- Added upgrade-guide for migration from v2.x
- Added developer-guide

---

## Migration from v2.x

See [Upgrade Guide](docs/en/upgrade-guide.md) for detailed migration instructions.
