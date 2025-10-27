# ČEZ HDO Integration

Integrace pro sledování HDO (High/Low tariff) tarifů ČEZ Distribuce.

## 🎨 Custom Lovelace Card

Integrace obsahuje vlastní Lovelace kartu pro přehledné zobrazení HDO informací.

### ⚠️ DŮLEŽITÉ: Registrace frontend resource

**Před použitím custom karty musíte přidat frontend resource:**

1. **Jděte do Home Assistant** → **Nastavení** → **Dashboards** → **Resources**
2. **Klikněte "Add Resource"**
3. **Zadejte URL:** `/local/cez-hdo-card.js`
4. **Resource type:** `JavaScript Module`
5. **Klikněte "Create"**
6. **Obnovte stránku** (Ctrl+F5)

### Použití karty

Po registraci resource můžete přidat kartu v Lovelace editoru:

```yaml
type: custom:cez-hdo-card
entities:
  low_tariff: binary_sensor.cez_hdo_lowtariffactive
  high_tariff: binary_sensor.cez_hdo_hightariffactive
  low_start: sensor.cez_hdo_lowtariffstart
  low_end: sensor.cez_hdo_lowtariffend
  low_duration: sensor.cez_hdo_lowtariffduration
  high_start: sensor.cez_hdo_hightariffstart
  high_end: sensor.cez_hdo_hightariffend
  high_duration: sensor.cez_hdo_hightariffduration
title: "ČEZ HDO Status"
show_times: true
show_duration: true
compact_mode: false
```

Karta se automaticky zobrazí v "Add Card" dialogu jako "ČEZ HDO Card".

## Konfigurace

Přidejte do `configuration.yaml`:

```yaml
# ČEZ HDO integrace
binary_sensor:
  - platform: cez_hdo
    region: stred  # váš region: zapad/sever/stred/vychod/morava
    code: 405      # váš HDO kód

sensor:
  - platform: cez_hdo
    region: stred
    code: 405
```
