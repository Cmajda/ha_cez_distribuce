# ⚡️ ČEZ HDO (Home Assistant) ⚡️

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![Release](https://img.shields.io/github/v/release/Cmajda/ha_cez_distribuce?label=stable&logo=github)](https://github.com/Cmajda/ha_cez_distribuce/releases/latest)
[![Pre-release](https://img.shields.io/github/v/release/Cmajda/ha_cez_distribuce?include_prereleases&label=pre-release&logo=github)](https://github.com/Cmajda/ha_cez_distribuce/releases)
[![Validate](https://github.com/Cmajda/ha_cez_distribuce/actions/workflows/hacs.yaml/badge.svg?branch=main)](https://github.com/Cmajda/ha_cez_distribuce/actions/workflows/hacs.yaml)
[![License](https://img.shields.io/badge/License-Apache%202.0%20%2B%20Commons%20Clause-blue)](./LICENSE)

[![Downloads](https://img.shields.io/github/downloads/Cmajda/ha_cez_distribuce/total)](https://github.com/Cmajda/ha_cez_distribuce/releases)
![Unique Views](https://raw.githubusercontent.com/Cmajda/ha_cez_distribuce/traffic/views_unique.svg)
![Unique Clones](https://raw.githubusercontent.com/Cmajda/ha_cez_distribuce/traffic/clones_unique.svg)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/Cmajda/ha_cez_distribuce)](https://github.com/Cmajda/ha_cez_distribuce/commits/main)

> ℹ️ **AUTOMATIC DATA REFRESH:** From version 3.2.1, the integration automatically refreshes HDO data.
> During configuration, you will enter a code from the CAPTCHA image. Data is then refreshed automatically.
> Data is stored in `.storage/cez_hdo/` and survives updates via HACS.
---
> 🚨 **BREAKING CHANGE v3.2.X:** Cache location changed from `custom_components/cez_hdo/data/` to `.storage/cez_hdo/`.
> After updating from version 3.2.0 or older, you need to:
>
> - **Reconfigure the integration**, or
> - **Manually copy data:**, from /config/custom_components/cez_hdo/data/*.json to /config/.storage/cez_hdo
>
>   ```bash
>   mkdir -p /config/.storage/cez_hdo
>   cp /config/custom_components/cez_hdo/data/*.json /config/.storage/cez_hdo/
>   ```

🇨🇿 [Česká verze](README.md)

> 🔴 **WARNING FOR v2.x USERS:**
> Before upgrading to v3.0.0, read the [**Upgrade Guide**](docs/en/upgrade-guide.md)!
> Version 3.0.0 brings major changes and requires manual steps.

Home Assistant integration that fetches HDO (low/high tariff) data
from ČEZ Distribuce API and creates entities + Lovelace card.

> ⚠️ **Unofficial integration** – This project is not an official product
> of ČEZ Distribuce a.s. It is a community project created
> for Home Assistant users. The author has no affiliation with ČEZ.

If you want to support me, you can do so here:

[![Buy me a beer](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20beer&emoji=%F0%9F%8D%BA&slug=cmajda&button_colour=FF813F&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/cmajda)

## 🤝 Contributors

Thanks to all co-authors who actively contribute to the development of this integration:

<!-- readme: collaborators -start -->
<table>
    <tbody>
        <tr>
            <td align="center">
                <a href="https://github.com/pokornyIt">
                    <img src="https://github.com/pokornyIt.png" width="96;" alt="pokornyIt"/>
                    <br />
                    <sub><b>pokornyIt</b></sub>
                </a>
            </td>
            <td align="center">
                <a href="https://github.com/VojtechJurcik">
                    <img src="https://github.com/VojtechJurcik.png" width="96;" alt="VojtechJurcik"/>
                    <br />
                    <sub><b>VojtechJurcik</b></sub>
                </a>
            </td>
        </tr>
    </tbody>
</table>
<!-- readme: collaborators -end -->

## 🚀 Quick Start

### 1. Install via HACS

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

### 2. Restart Home Assistant

### 3. Add Integration

1. **Settings → Devices & Services → + Add Integration**
2. Search for **ČEZ HDO**
3. Enter your **EAN** (18-digit number from your electricity bill)
4. Enter the **CAPTCHA code** from the image
5. Select **signal** (if multiple options available)
6. Enter **prices** for NT and VT (CZK/kWh)

### 4. Add Card

In Lovelace, add the **ČEZ HDO Card** (or `custom:cez-hdo-card`).

> **Note:** After installation, you may need to press `Ctrl+F5`
> to clear the browser cache.

## 🎴 Lovelace Card

The card has a visual editor with display options:

- Tariff states (NT/VT active)
- Tariff start/end times
- Remaining time until change
- Current price
- 7-day HDO schedule

![ČEZ HDO card](img/en/entity_card.png) ![HDO schedule](img/en/graph.png)

### Price Settings

Prices are configured in the **integration**
(Settings → Devices & Services → ČEZ HDO → Configure), not in the card.

> **To change prices:** Go through all configuration steps – price settings are at the end.

### Energy Dashboard

The sensor `sensor.cez_hdo_currentprice_*` can be used as a price source in the Energy Dashboard.

## 📦 Created Entities

| Type   | Entity                          | Description                |
| ------ | ------------------------------- | -------------------------- |
| Binary | `cez_hdo_lowtariffactive_*`     | NT (low tariff) is active  |
| Binary | `cez_hdo_hightariffactive_*`    | VT (high tariff) is active |
| Binary | `cez_hdo_data_valid_*`          | Data is valid              |
| Sensor | `cez_hdo_lowtariffstart_*`      | NT start time              |
| Sensor | `cez_hdo_lowtariffend_*`        | NT end time                |
| Sensor | `cez_hdo_lowtariffremaining_*`  | NT remaining time          |
| Sensor | `cez_hdo_hightariffstart_*`     | VT start time              |
| Sensor | `cez_hdo_hightariffend_*`       | VT end time                |
| Sensor | `cez_hdo_hightariffremaining_*` | VT remaining time          |
| Sensor | `cez_hdo_currentprice_*`        | Current price (CZK/kWh)    |
| Sensor | `cez_hdo_schedule_*`            | 7-day HDO schedule         |
| Sensor | `cez_hdo_data_valid_until_*`    | Data expiration date       |
| Sensor | `cez_hdo_data_age_days_*`       | Data age (days)            |
| Sensor | `cez_hdo_days_until_expiry_*`   | Days until expiry          |

> **Note:** `*` represents your chosen suffix (e.g., `home` or `7606_a1b4dp04`).

## ⚠️ Upgrade from v2.x

Version 3.0.0 brings **major changes**:

1. **Delete YAML configuration** from `configuration.yaml`
2. **Update** via HACS
3. **Restart** Home Assistant
4. **Delete old entities** (Settings → Entities)
5. **Add integration** via GUI
6. **Delete folder** `www/cez_hdo/`

Detailed guide: [docs/en/upgrade-guide.md](docs/en/upgrade-guide.md)

## 🔧 Troubleshooting

1. **Ctrl+F5** – clear browser cache
2. **Reload integration** – Settings → Devices & Services → ČEZ HDO → Reload
3. **Check logs** – Settings → System → Logs

### Diagnostics

To report a bug, export diagnostics:

1. Settings → Devices & Services → ČEZ HDO
2. Click on device → ⋮ → **Download diagnostics**
3. Attach to [GitHub Issue](https://github.com/Cmajda/ha_cez_distribuce/issues)

## 📚 Documentation

- [User Guide (CS)](docs/cs/user-guide.md) – complete documentation (Czech)
- [User Guide (EN)](docs/en/user-guide.md) – complete documentation (English)
- [Upgrade Guide (CS)](docs/cs/upgrade-guide.md) – migration from v2.x to v3.0.0 (Czech)
- [Upgrade Guide (EN)](docs/en/upgrade-guide.md) – migration from v2.x to v3.0.0
- [Service Guide (CS)](docs/cs/service-guide.md) – available services (Czech)
- [Service Guide (EN)](docs/en/service-guide.md) – available services
- [Developer Guide (CS)](docs/cs/developer-guide.md) – for developers (Czech)
- [Developer Guide (EN)](docs/en/developer-guide.md) – for developers
- [Known Issues (CS)](docs/cs/known-issues.md) – list of known issues (Czech)
- [Known Issues (EN)](docs/en/known-issues.md) – list of known issues

## 📝 Release Notes

See [RELEASE_NOTES.md](RELEASE_NOTES.md)

## 📄 License

Apache 2.0 + Commons Clause (non-commercial use) | Support: [GitHub Issues](https://github.com/Cmajda/ha_cez_distribuce/issues)
