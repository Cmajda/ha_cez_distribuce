# ČEZ HDO – Upgrade Guide

This document describes the procedure for upgrading the integration to a new version.

---

## ⚠️ Upgrade to v3.x (from v2.x) – IMPORTANT CHANGES

Version 3.x brings **major changes** to the integration architecture.
Please read the entire procedure carefully.

### Changes from v2.x

| Feature | v2.x | v3.x |
|---------|------|--------|
| **Configuration** | YAML (`configuration.yaml`) | GUI (Settings → Integrations) |
| **Entity Management** | Individual entities | Device Registry (grouped under device) |
| **Data Storage** | `www/cez_hdo/` | Home Assistant `.storage` |
| **Price Settings** | Card editor | Options Flow integration |
| **Cache** | Shared file | Per-EAN files in `.storage` |
| **Diagnostics** | Manual logs | UI export |
| **Multiple EAN** | Complicated | Fully supported |
| **Multiple signals per EAN** | Not supported | Fully supported |
| **Entity IDs** | Automatic | User-configurable suffix |

### Upgrade Procedure

#### Step 1: Backup (recommended)

Before upgrading, create a Home Assistant backup (Settings → System → Backups).

#### Step 2: Delete YAML Configuration

In `configuration.yaml`, **delete** all ČEZ HDO blocks:

```yaml
# DELETE these blocks:
sensor:
  - platform: cez_hdo
    ean: "Your EAN"

binary_sensor:
  - platform: cez_hdo
    ean: "Your EAN"
```

#### Step 3: Update the Integration

- **HACS:** Open HACS → ČEZ HDO → Update to the latest 3.x version
- **Manually:** Download and overwrite `custom_components/cez_hdo/`

#### Step 4: Restart Home Assistant

After the update, perform a **full restart** of Home Assistant (not just reload).

#### Step 5: Delete Old Entities

1. **Settings → Devices & Services → Entities**
2. Type `cez_hdo` in the search box
3. Select all old entities (will be without assigned device)
4. Click **Remove selected**

#### Step 6: Add Integration via GUI

1. **Settings → Devices & Services**
2. Click **+ Add Integration**
3. Search for **ČEZ HDO**
4. Complete the current configuration steps: EAN, CAPTCHA, signal, suffix, and prices.
5. In price settings, keep fixed prices or optionally select price entities.
6. Finish setup using the [user guide](user-guide.md).

#### Step 7: Remove the Legacy Folder if Present

If it remains from v2.x, delete the old `www/cez_hdo/` folder; the current version does not use it:

```bash
# Via SSH or File Editor addon
rm -rf /config/www/cez_hdo
```

The current version stores its cache in Home Assistant-managed `.storage`.

#### Step 8: Update Card

1. Open Lovelace dashboard
2. Press `Ctrl+F5` to clear cache
3. Edit the `custom:cez-hdo-card` card
4. **Prices are now configured in the integration**, not in the card

### ✅ Verify Upgrade

After upgrade, you should see:

1. **Settings → Devices & Services → ČEZ HDO**
   - Device "ČEZ HDO ({signal})"
   - All entities grouped under this device

2. **Entities with new names:**
   - `sensor.cez_hdo_lowtariffstart_{suffix}`
   - `binary_sensor.cez_hdo_lowtariffactive_{suffix}`
   - etc. (where `{suffix}` is your chosen suffix)

3. **Diagnostics available:**
   - Settings → Devices → ČEZ HDO → ⋮ → Download diagnostics

---

## 🔄 Changing Settings After Installation

### Changing EAN, Signal, or Prices

1. **Settings → Devices & Services → ČEZ HDO**
2. Click on **Configure**
3. Go through the EAN → CAPTCHA → Signal → Suffix → Prices steps
4. Save changes

### Multiple EAN (Multiple Delivery Points)

For each EAN, add the integration again:

1. Settings → Devices & Services → + Add Integration → ČEZ HDO
2. Enter additional EAN

Each EAN will have:

- Its own device in Device Registry
- Its own entities (with unique suffix)
- Its own cache files

### Same EAN with Different Signals

If you have one EAN with multiple signals (e.g., for different circuits):

1. Add the integration for each signal separately
2. Each instance will have a different suffix

---

## 🔧 When Something Doesn't Work

### Card Not Displaying

1. Press `Ctrl+F5`
2. Check that URL `/cez_hdo_card/cez-hdo-card.js?v=3.3.1` returns 200

### Entities Not Available

1. Check Settings → Devices & Services → ČEZ HDO
2. Verify the integration has no errors
3. Click "Reload" on the integration

### Complete Reset

If nothing helps:

1. Settings → Devices & Services → ČEZ HDO → Delete
2. Cache, price, and refresh-state files are in Home Assistant-managed `.storage`; they normally do not need to be removed manually.
3. Restart Home Assistant
4. Add the integration again

---

## 📊 Export Diagnostic Data

To report a bug:

1. **Settings → Devices & Services → ČEZ HDO**
2. Click on the device
3. Click **⋮** (three dots) → **Download diagnostics**
4. Attach the JSON file to an issue on GitHub

Diagnostics contain:

- Sensor states (values, attributes)
- Cache contents (schedule, prices)
- Integration settings
- **No sensitive data** (EAN is masked)
