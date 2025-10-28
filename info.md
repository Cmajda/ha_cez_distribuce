# ČEZ HDO Integration v1.1.0

Integrace pro sledování HDO (High/Low tariff) tarifů ČEZ Distribuce s automatickou instalací a custom Lovelace kartou.

## ✨ Nové ve verzi 1.1.0

- 🎨 **Custom Lovelace Card** - TypeScript karta pro lepší zobrazení HDO
- 🔧 **Automatická instalace** frontend resources
- ♻️ **Refaktorovaný Python kód** - 60% méně duplikace kódu
- 🏛️ **Podpora státních svátků** - automaticky aplikuje víkendový tarif
- ⏰ **Vylepšený formát času** - bez milisekund pro lepší čitelnost
- ✅ **HACS kompatibilita** - plně připraveno pro HACS store

## 🚀 Jednoduchá instalace

### 1. Konfigurace senzorů

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

### 2. Přidání frontend resource

**Pro použití custom karty:**

- Jděte do **Nastavení** → **Dashboards** → **Resources**
- Přidejte URL: `/local/cez-hdo-card.js`
- Type: **JavaScript Module**

### 3. Restart Home Assistant

Po restartu budou k dispozici entity a custom karta.

## 🎨 Custom Lovelace Card

### Automatické přidání karty:

1. Otevřete Lovelace editor
2. Klikněte **"Přidat kartu"**
3. Najděte **"ČEZ HDO Card"** v seznamu
4. Karta se automaticky nakonfiguruje!

### Ruční konfigurace:

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

## 📊 Vytvořené entity

### Binary Sensors

- `binary_sensor.cez_hdo_lowtariffactive` - Je aktivní nízký tarif?
- `binary_sensor.cez_hdo_hightariffactive` - Je aktivní vysoký tarif?

### Sensors

- `sensor.cez_hdo_lowtariffstart` - Začátek nízkého tarifu
- `sensor.cez_hdo_lowtariffend` - Konec nízkého tarifu
- `sensor.cez_hdo_lowtariffduration` - Zbývající čas nízkého tarifu
- `sensor.cez_hdo_hightariffstart` - Začátek vysokého tarifu
- `sensor.cez_hdo_hightariffend` - Konec vysokého tarifu
- `sensor.cez_hdo_hightariffduration` - Zbývající čas vysokého tarifu

## 🔧 Podporované funkce

- ✅ **Pracovní dny** (Po-Pá) a **víkendy** (So-Ne)
- ✅ **Státní svátky** - automaticky aplikuje víkendový tarif
- ✅ **Všechny regiony ČEZ** - západ, sever, střed, východ, morava
- ✅ **Realtime aktualizace** - každou hodinu
- ✅ **Detailní atributy** s kompletní API odpovědí

Integrace automaticky detekuje české státní svátky a aplikuje správný víkendový tarif.
