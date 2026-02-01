# ČEZ HDO – Services

This document describes the services (Developer Tools → Services) offered by the integration.

## `cez_hdo.list_signals`

Lists available HDO signals for a given EAN in the Home Assistant logs.

Usage:

```yaml
action: cez_hdo.list_signals
data:
  ean: "Your EAN"
```

Where to see it:

- Settings → System → Logs

## `cez_hdo.set_prices`

Sets prices for low and high tariffs.
Prices are stored persistently and survive Home Assistant restarts.

Usage:

```yaml
action: cez_hdo.set_prices
data:
  low_tariff_price: 2.50
  high_tariff_price: 4.50
```

Parameters:

- `low_tariff_price` – price per kWh in low tariff (NT) in CZK
- `high_tariff_price` – price per kWh in high tariff (VT) in CZK

After setting, the `sensor.cez_hdo_currentprice` sensor is automatically updated.

## `cez_hdo.reload_frontend_card`

Redeploys/refreshes the frontend card file.
Useful during development or when the card doesn't load.

Usage:

```yaml
action: cez_hdo.reload_frontend_card
data: {}
```

Note: After using this service, you may need to press `Ctrl+F5` in your browser.
