# ČEZ HDO – Services

Tento dokument popisuje služby (Developer Tools → Services), které integrace nabízí.

## `cez_hdo.list_signals`

Vypíše dostupné HDO signály pro zadaný EAN do logů Home Assistant.

Použití:

```yaml
action: cez_hdo.list_signals
data:
  ean: "Váš EAN"
```

Kde to uvidíte:

- Nastavení → Systém → Protokoly (Logs)

## `cez_hdo.set_prices`

Nastaví ceny pro nízký a vysoký tarif.
Ceny se uloží perzistentně a přežijí restart Home Assistantu.

Použití:

```yaml
action: cez_hdo.set_prices
data:
  low_tariff_price: 2.50
  high_tariff_price: 4.50
```

Parametry:

- `low_tariff_price` – cena za kWh v nízkém tarifu (NT) v Kč
- `high_tariff_price` – cena za kWh ve vysokém tarifu (VT) v Kč

Po nastavení se automaticky aktualizuje senzor `sensor.cez_hdo_aktualni_cena`.

## `cez_hdo.reload_frontend_card`

Znovu nasadí/obnoví frontend soubor karty.
Užitečné při vývoji nebo když se karta nenačítá.

Použití:

```yaml
action: cez_hdo.reload_frontend_card
data: {}
```

Poznámka: po použití služby může být v prohlížeči potřeba `Ctrl+F5`.
