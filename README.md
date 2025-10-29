# ČEZ HDO - Senzor pro Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

Tento senzor stahuje data z webu https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html.
Integrace vyžaduje **region** a **kód**. Tyto informace lze získat ze smlouvy s ČEZ CZ nebo z https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html.

Pro otestování zda je správně použit region a kod, lze otevřít odkaz v prohlížeči ve tvaru:

`https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/`REGION`?code=`kód

Příklad:

```Text
https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/stred?code=405
```

## ✨ Funkce integrace

- ✅ **Aktuální stav HDO** - zobrazuje zda je aktivní nízký nebo vysoký tarif
- ✅ **Časy začátku a konce** nízkého/vysokého tarifu
- ✅ **Zbývající čas** aktivního tarifu
- ✅ **Podpora státních svátků** - automaticky aplikuje víkendový tarif
- ✅ **Custom Lovelace karta** pro přehledné zobrazení

## 🚀 Instalace

### Krok 1: Instalace přes HACS

Klikněte na tlačítko níže pro automatické otevření HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

**Nebo manuálně:**

1. Otevřete HACS v Home Assistant
2. Jděte na **Integrations**
3. Klikněte na **⋮** → **Custom repositories**
4. Přidejte URL: `https://github.com/Cmajda/ha_cez_distribuce`
5. Kategorie: **Integration**
6. Klikněte **Add**
7. Najděte **"ČEZ HDO"** a nainstalujte

### Krok 2: Konfigurace

Přidejte do `configuration.yaml`:

```yaml
# ČEZ HDO integrace
sensor:
  - platform: cez_hdo
    kod_distribuce: "CZE"  # Váš distribuční kód
    name: "ČEZ HDO"
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)

binary_sensor:
  - platform: cez_hdo
    kod_distribuce: "CZE"  # Váš distribuční kód
    name: "ČEZ HDO Binary"
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)
```

#### Podporované distribuční kódy

- **CZE** - ČEZ Distribuce (celá ČR)
- Další kódy budou přidány dle potřeby

### Krok 3: Přidání Lovelace karty

Karta se automaticky nainstaluje při prvním spuštění integrace. Pro ruční konfiguraci přidejte do dashboardu:

```yaml
type: custom:cez-hdo-card
entities:
  nt_binary: binary_sensor.cez_hdo_nt_active
  vt_binary: binary_sensor.cez_hdo_vt_active
  nt_start: sensor.cez_hdo_nt_start
  nt_end: sensor.cez_hdo_nt_end
  vt_start: sensor.cez_hdo_vt_start
  vt_end: sensor.cez_hdo_vt_end
  nt_remaining: sensor.cez_hdo_nt_remaining
  vt_remaining: sensor.cez_hdo_vt_remaining
title: "ČEZ HDO Status"
show_times: true
show_duration: true
compact_mode: false
```

### Krok 4: Restartování Home Assistant

Po přidání konfigurace restartujte Home Assistant.

## 🎨 Custom Lovelace Card

Integrace obsahuje vlastní Lovelace kartu pro lepší zobrazení HDO informací:

![ČEZ HDO Card](entity_card.png)

## 📊 Entity

Integrace vytváří následující entity:

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

### Atributy

Každý senzor obsahuje v atributech kompletní API odpověď s detailními informacemi o HDO rozpisech.

## � Debug logování

Pro detailní logování a troubleshooting přidejte do `configuration.yaml`:

```yaml
logger:
  default: error
  logs:
    custom_components.cez_hdo.downloader: debug
```

**Debug logy obsahují:**

- 🗓️ Výběr kalendáře (pracovní dny vs víkendy/svátky)
- 🔍 Seznam všech HDO období pro aktuální den
- ✅ Aktuální stav (nízký/vysoký tarif) se zbývajícím časem

**Zobrazení debug logů:**

1. **Developer Tools** → **Logs**
2. **Klikněte na "Zobrazit nezpracované logy"**
3. **Filtrujte:** `custom_components.cez_hdo`

## �🔧 Řešení problémů

Pokud máte problémy s integrací:

1. **Zkontrolujte region a kód** - otestujte URL v prohlížeči
2. **Zkontrolujte logy** - Developer Tools → Logs
3. **Restartujte HA** po změnách konfigurace
4. **Vyčistěte cache** prohlížeče (Ctrl+F5) pro Lovelace kartu
