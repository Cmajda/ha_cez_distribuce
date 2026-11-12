# ⚡️ ČEZ HDO – User Guide

Complete guide for installation, configuration, and usage of the ČEZ HDO integration in Home Assistant.

---

## 📑 Table of Contents

- [🚀 Installation](#-installation)
- [⚙️ Integration Configuration](#️-integration-configuration)
- [🎴 Adding Card to Dashboard](#-adding-card-to-dashboard)
- [📦 Created Entities](#-created-entities)
- [💰 Price Settings](#-price-settings)
- [📊 Energy Dashboard](#-energy-dashboard)
- [📅 HDO Schedule](#-hdo-schedule)
- [🔧 Troubleshooting](#-troubleshooting)
- [🐛 Debug Logging](#-debug-logging)
- [📊 Diagnostics](#-diagnostics)

---

## 🚀 Installation

### Installation via HACS (recommended)

1. Open **HACS → Integrations**
2. Click on **⋮** → **Custom repositories**
3. Add the repository:

[![HACS Repository Badge](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

1. Install the **ČEZ HDO** integration
2. **Restart Home Assistant**

### After Installation

After restart, proceed with the integration configuration (see next section).

> **Note:** After installation/update, you may need to press
> `Ctrl+F5` to clear browser cache.

---

## ⚙️ Integration Configuration

Starting from version 3.0.0, the integration is configured exclusively through the graphical interface (GUI).

### Adding the Integration

1. Go to **Settings → Devices & Services**
2. Click the **+ Add Integration** button
3. Type **ČEZ HDO** in the search field
4. Select the integration from the list

### Step 1: Enter EAN

Enter your **EAN number** (18 digits) and click **Submit**.

![Enter EAN](../../img/en/card_add_integration_1.png)

You can find your EAN:

- On your electricity invoice / bill
- In your electricity provider's portal
- On the [ČEZ Distribuce](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo) website

### Step 2: CAPTCHA Verification

To verify access to the ČEZ Distribuce API, you need to enter the **CAPTCHA code from the image**.

![CAPTCHA Verification](../../img/en/card_add_integration_5.png)

1. An image with a code will be displayed
2. Type the displayed characters into the text field
3. Click **Submit**

> **⚠️ Important:** If you enter the wrong code, a new CAPTCHA image will be displayed.
> Data from the API is valid for **6 days**. Automatic refresh will try to renew it; you can also renew it at any time using **Manually refresh** on the ČEZ HDO card.

### Step 3: Select Signal

Select the **HDO signal** from the list of available signals for your metering point.

![Select signal](../../img/en/card_add_integration_2.png)

- **If you're unsure about your signal**, you can find it in your contract with ČEZ Distribuce
- If you don't know your signal, keep the default value (first signal in the list)
- The signal determines when switching between low (NT) and high (VT) tariff occurs
- **The same EAN can be added multiple times with different signals**

After selecting the signal, click **Submit**.

### Step 4: Entity ID Suffix

Enter a **suffix** that will be used in all entity names.

![Entity ID Suffix](../../img/en/card_add_integration_3.png)

- **Default value:** `{last 4 digits of EAN}_{signal}` (e.g., `7606_a1b4dp04`)
- **Custom suffix:** You can enter custom text for better orientation (e.g., `cottage`, `apartment`, `house`)

**Examples of resulting entity IDs:**

| Suffix          | Resulting Entity ID                           |
| --------------- | --------------------------------------------- |
| `7606_a1b4dp04` | `sensor.cez_hdo_lowtariffstart_7606_a1b4dp04` |
| `cottage`       | `sensor.cez_hdo_lowtariffstart_cottage`       |

> **Tip:** Use intuitive names for easier navigation in automations, especially if you have multiple metering points.

**Entity name language:** Home Assistant determines entity names using the Core language
when they are first created. Set it under **Settings → System → Home information → Region → Language**.
Your profile language affects the interface and card text, but does not translate existing names.
To create new entities in English, set the Core language to English before adding the integration.

Click **Submit**.

### Step 5: Price Settings

Enter electricity prices for low and high tariff.

![Price settings](../../img/en/card_add_integration_4.png)

| Field                  | Description                  |
| ---------------------- | ---------------------------- |
| **NT Price (CZK/kWh)** | Price per kWh in low tariff  |
| **VT Price (CZK/kWh)** | Price per kWh in high tariff |
| **Auto refresh data** | Enable automatic HDO data refresh |
| **OCR.space API key** | Optional key for automatic CAPTCHA solving, see [OCR API Key](#ocr-api-key) |
| **Use NT/VT price from entity** | Use the selected sensor or helper instead of the fixed price |
| **NT/VT price sensor or number helper** | Optional price source; used only when its toggle is enabled |

You can find prices on your invoice or in the price list from your electricity provider. These prices are used for cost calculations in the card and for integration with Energy Dashboard.

Click **Submit**.

### Step 6: Device Placement

Home Assistant will ask which area you want to place the device in.

![Finish configuration](../../img/en/card_add_finish.png)

- Select an area (room) for your device, or
- Click **Skip** to finish configuration

🎉 **Congratulations!** The integration is now configured and will create:

- Device "ČEZ HDO ({signal})"
- All sensors and binary sensors

---

## 🎴 Adding Card to Dashboard

### Step 1: Edit Dashboard

1. Open the dashboard where you want to add the card
2. Click **⋮** (three dots) in the top right corner
3. Select **Edit Dashboard**

### Step 2: Add Card

1. Click **+ Add Card**
2. Type **ČEZ HDO** in the search field
3. Select the **ČEZ HDO Card**

![Add card](../../img/en/add_card_1.png)

### Step 3: Configure Card

The card editor will open with configuration options.

![Card settings](../../img/en/add_card_2.png)

> **Tip:** If this is your first (or only) EAN, the card will automatically populate all entities. Prices entered during integration configuration will be automatically loaded.

#### Card Configuration Options

| Toggle                       | Description                              | Default |
| ---------------------------- | ---------------------------------------- | ------- |
| **Show title**               | Card header                              | ✅ On    |
| **Show tariff states**       | NT/VT boxes with state (active/inactive) | ✅ On    |
| **Show prices with tariffs** | Price in NT/VT box                       | ❌ Off   |
| **Show times**               | Tariff start and end times               | ✅ On    |
| **Show remaining time**      | Time until tariff change                 | ✅ On    |
| **Show current price**       | Large box with current price             | ✅ On    |
| **Show HDO schedule**        | 7-day schedule visualization             | ❌ Off   |
| **Show prices in legend**    | Prices for NT/VT in schedule legend      | ❌ Off   |
| **Compact mode**             | Reduced card size                        | ❌ Off   |

#### Entity Selection

The card automatically detects ČEZ HDO entities. If you have **multiple integration instances** (multiple EANs or multiple signals for one EAN), you need to correctly set the entities:

1. Expand the **Entities** section
2. Select the correct entities for your desired EAN/signal

After completing the settings, click **Save**.

### Result

The card will be displayed on the selected dashboard.

![Dashboard with card](../../img/en/dashboard_view.png)

---

## 📦 Created Entities

The integration creates the following entities:

### Binary Sensors

| Entity                                     | Description                      |
| ------------------------------------------ | -------------------------------- |
| `binary_sensor.cez_hdo_lowtariffactive_*`  | Low tariff is active (`on/off`)  |
| `binary_sensor.cez_hdo_hightariffactive_*` | High tariff is active (`on/off`) |
| `binary_sensor.cez_hdo_data_valid_*`       | API data is valid (`on/off`)     |

### Sensors

| Entity                                 | Description                            |
| -------------------------------------- | -------------------------------------- |
| `sensor.cez_hdo_lowtariffstart_*`      | NT start time (e.g., `01:10`)          |
| `sensor.cez_hdo_lowtariffend_*`        | NT end time (e.g., `08:30`)            |
| `sensor.cez_hdo_lowtariffduration_*`   | Remaining time until tariff change     |
| `sensor.cez_hdo_hightariffstart_*`     | VT start time                          |
| `sensor.cez_hdo_hightariffend_*`       | VT end time                            |
| `sensor.cez_hdo_hightariffduration_*`  | Remaining time until tariff change     |
| `sensor.cez_hdo_currentprice_*`        | Current price in CZK/kWh               |
| `sensor.cez_hdo_schedule_*`            | 7-day HDO schedule                     |
| `sensor.cez_hdo_raw_data_*`           | Last update timestamp                  |
| `sensor.cez_hdo_data_valid_until_*`    | Data validity expiration date and time |
| `sensor.cez_hdo_data_age_days_*`       | Data age in days                       |
| `sensor.cez_hdo_days_until_expiry_*`   | Days until data expires                |

> **Note:** `*` represents your chosen suffix from step 4 (e.g., `7606_a1b4dp04` or `cottage`).

### Multiple EANs / Signals

The integration supports:

- **Multiple different EANs** – each added as a new integration instance
- **Same EAN with different signals** – each signal as a new instance

Each instance has its own device and entities with a unique suffix.

---

## ⏰ Data Validity and Renewal

### Why Does Data Expire?

ČEZ Distribuce uses CAPTCHA protection on its API. Data is valid for **6 days**. When automatic refresh is enabled, the
integration will try to renew it automatically. You can start a manual renewal at any time with **Manually refresh** on
the card. After CAPTCHA verification, choose a signal from the alphabetically sorted list returned by ČEZ; the selection
is saved as the instance's configured signal.

### OCR API Key

Automatic refresh solves the ČEZ CAPTCHA with OCR.space. By default it uses a shared demo key that the provider rate
limits and marks as testing-only. A personal key is free and is not shared with other users:

1. Open <https://ocr.space/ocrapi/freekey> and sign up with your email address
2. Find the email from OCR.space and copy the API key it contains
3. In Home Assistant open **Settings → Devices & services → ČEZ HDO → Configure** and paste the key into
   **OCR.space API key** on the price settings step

Leave the field empty to keep using the shared demo key. The key is stored in the integration configuration entry.

### Tracking Data Validity

The integration provides sensors for tracking validity:

| Entity                               | Description                            |
| ------------------------------------ | -------------------------------------- |
| `binary_sensor.cez_hdo_data_valid_*` | `on` = data valid, `off` = expired     |
| `sensor.cez_hdo_days_until_expiry_*` | Days until expiry (negative = expired) |
| `sensor.cez_hdo_data_age_days_*`     | How many days old the data is          |
| `sensor.cez_hdo_data_valid_until_*`  | Exact expiration date and time         |

### Automatic Notifications

The integration automatically displays **persistent notifications**:

- **Day 5:** Warning that data will expire soon
- **Day 6:** Alert that data has expired

### Automation Example

For custom notifications, you can use an automation:

```yaml
automation:
  - alias: "ČEZ HDO - Data expiring soon"
    trigger:
      - platform: numeric_state
        entity_id: sensor.cez_hdo_days_until_expiry_SUFFIX
        below: 2
    action:
      - service: notify.mobile_app_phone
        data:
          title: "ČEZ HDO"
          message: "HDO data will expire in {{ states('sensor.cez_hdo_days_until_expiry_SUFFIX') }} days!"
```

> **Note:** Replace `SUFFIX` with your entity suffix (e.g., `7606_a1b4dp04`).

### Renewing Data

You can fetch new data at any time, for example before it expires:

1. Open the **ČEZ HDO** Lovelace card for the signal you want to refresh
2. Click **Manually refresh**
3. Enter the CAPTCHA and load the available signals
4. Select the desired signal and confirm with **Refresh data**

Automatic refresh remains enabled according to the integration settings. A failed manual refresh does not delete the previously stored data.

---

## 💰 Price Settings

Prices are set **in the integration**, not in the card.

### Changing Prices

1. Go to **Settings → Devices & Services**
2. Find the **ČEZ HDO** integration and click on it
3. Click **Configure**
4. Navigate through steps to **Tariff Prices Setup**
5. Change the manual prices or select NT and VT price sensors, then save

When a price sensor is selected and its **Use price from entity** toggle is enabled, its
numeric state is used as the price and updates whenever the sensor changes. The manual
price remains in use when the toggle is disabled or the sensor state is unavailable or non-numeric.

### set_prices Service

Prices can also be set programmatically via service in **Developer Tools → Services**:

```yaml
service: cez_hdo.set_prices
data:
  low_tariff_price: 2.50
  high_tariff_price: 4.50
```

> **⚠️ Limitation:** In the current version, this service sets prices for all integration instances.
> Device-specific price setting will be added in a future version.

---

## 📊 Energy Dashboard

The `sensor.cez_hdo_currentprice_{suffix}` sensor can be used in Energy Dashboard for cost tracking:

1. Go to **Settings → Dashboards → Energy**
2. In the "Electricity grid" section, click **Add consumption**
3. Select your electricity consumption meter
4. In the "Use an entity with current price" field, select `sensor.cez_hdo_currentprice_{suffix}`

![Energy Dashboard](../../img/en/integration_energy_ha.png)

---

## 📅 HDO Schedule

The card includes a 7-day HDO schedule visualization:

### Activation

1. Open the card editor
2. Enable the **Show HDO schedule** toggle
3. Optionally enable **Show prices in schedule legend**

### Schedule Description

- **Green blocks** – low tariff (NT)
- **Orange blocks** – high tariff (VT)
- **Timeline** – 0:00 to 24:00
- **Tooltip** – exact times when hovering over a block

---

## 🔧 Troubleshooting

### Card Not Displaying

1. Press `Ctrl+F5` to clear browser cache
2. Check that URL `http://HA_IP:8123/cez_hdo_card/cez-hdo-card.js?v=3.3.1` returns a response (status 200)
3. Check browser console (F12) for any errors

### Entities Not Available

1. Go to **Settings → Devices & Services → ČEZ HDO**
2. Verify the integration doesn't have an error (red icon)
3. Click **⋮** and select **Reload** for the integration

### Error "Invalid EAN" or "Failed to Load Signals"

- Verify the EAN is correct (18 digits)
- Check the [ČEZ Distribuce portal](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo) manually
- ČEZ API may be temporarily unavailable – try again later

### Complete Reset

1. Go to **Settings → Devices & Services → ČEZ HDO → Delete**
2. Restart Home Assistant and add the integration again.

Home Assistant manages the cache, prices, and auto-refresh state in `.storage`;
`custom_components/cez_hdo/data/` is no longer used. To fully clear saved data, first
create a backup, stop Home Assistant, and delete only the `cez_hdo.cache_*`,
`cez_hdo.prices_*`, and `cez_hdo.refresh_state_*` files from `/config/.storage/`.

---

## 🐛 Debug Logging

If you need to obtain detailed logs for diagnosing a problem, you can enable debug logging directly in Home Assistant.

### Step 1: Enable Debug Logging

1. Go to **Settings → Devices & Services**
2. Select the **ČEZ HDO** integration
3. Click **⋮** (three dots) in the top right corner
4. Select **Enable debug logging**

![Enable debug logging](../../img/en/enable_debug_1.png)

### Step 2: Reproduce the Problem

Perform the steps that lead to the error or incorrect behavior of the integration. The logs will record all integration operations.

### Step 3: Disable Debug Logging and Download Logs

1. Go to **Settings → Devices & Services**
2. Select the **ČEZ HDO** integration
3. Click on the info banner **“Debug logging enabled”**
4. Click **Disable**

![Disable debug logging](../../img/en/disable_debug_1.png)

### Step 4: Download the Log File

After clicking **Disable**, Home Assistant will automatically generate a file with debug information and prompt you to download it.

1. Save the downloaded file
2. Attach this file to your GitHub Issue

> **Tip:** Debug logs contain detailed information about all integration operations and are very useful for diagnosing problems.

---

## 📊 Diagnostics

To report a bug on GitHub, export diagnostic data:

### Export Diagnostics

1. Go to **Settings → Devices & Services → ČEZ HDO**
2. Click on the device
3. Click **⋮** (three dots) in the top right
4. Select **Download diagnostics**
5. Save the JSON file

### What Diagnostics Contain

- State of all sensors (values, attributes)
- Cache contents (HDO schedule)
- Integration settings (signal, prices)
- **Sensitive data is masked** (EAN, partner, vkont, vstelle, anlage)

### Attaching to Issue

1. Open [GitHub Issues](https://github.com/Cmajda/ha_cez_distribuce/issues)
2. Create a new issue
3. Attach the diagnostic JSON file
4. Describe the problem in detail

---

## 📚 Additional Documentation

- [Upgrade Guide](upgrade-guide.md) – upgrade procedure from v2.x to v3.0.0
- [Developer Guide](developer-guide.md) – for developers
- [Service Guide](service-guide.md) – description of available services
- [Known Issues](known-issues.md) – list of known issues and limitations
