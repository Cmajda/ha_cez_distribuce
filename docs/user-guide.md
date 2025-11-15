# ČEZ HDO - Uživatelská dokumentace

## 📑 Obsah

- [📑 Obsah](#-obsah)
- [🚀 Instalace](#-instalace)
  - [Automatická instalace přes HACS](#automatická-instalace-přes-hacs)
  - [Manuální instalace](#manuální-instalace)
- [⚙️ Konfigurace](#️-konfigurace)
  - [Základní konfigurace](#základní-konfigurace)
  - [EAN číslo - jak ho najít](#ean-číslo---jak-ho-najít)
  - [Dostupné signály a jejich výběr](#dostupné-signály-a-jejich-výběr)
- [🎨 Lovelace karta](#-lovelace-karta)
  - [✨ Automatická instalace karty](#-automatická-instalace-karty)
  - [🔧 Ruční přidání karty (pouze pokud automatická selže)](#-ruční-přidání-karty-pouze-pokud-automatická-selže)
  - [Konfigurace karty](#konfigurace-karty)
- [📊 Entity a senzory](#-entity-a-senzory)
  - [Binary Sensors](#binary-sensors)
  - [Sensors](#sensors)
  - [Atributy](#atributy)
- [🔍 Debug a řešení problémů](#-debug-a-řešení-problémů)
  - [Debug logování](#debug-logování)
  - [Řešení problémů](#řešení-problémů)
  - [Debug logy obsahují](#debug-logy-obsahují)

## 🚀 Instalace

### Automatická instalace přes HACS

Klikněte na tlačítko níže pro automatické otevření HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

### Manuální instalace

1. Otevřete HACS v Home Assistant
2. Jděte na **Integrations**
3. Klikněte na **⋮** → **Custom repositories**
4. Přidejte URL: `https://github.com/Cmajda/ha_cez_distribuce`
5. Kategorie: **Integration**
6. Klikněte **Add**
7. Najděte **"ČEZ HDO"** a nainstalujte

## ⚙️ Konfigurace

### Základní konfigurace

Přidejte do `configuration.yaml`:

```yaml
# ČEZ HDO integrace
sensor:
  - platform: cez_hdo
    code: "405"  # Váš distribuční kód
    region: stred # Váš region
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)

binary_sensor:
  - platform: cez_hdo
    code: "405"  # Váš distribuční kód
    region: stred # Váš region
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)
```

**Chování bez specifikace signálu:**
- Integrace automaticky použije **první nalezený signál** pro daný den
- Pro většinu uživatelů je toto dostatečné

## 🎨 Lovelace karta

### ✨ Automatická instalace karty

🎯 **Karta se instaluje a registruje úplně automaticky!**

Po instalaci integrace a restartu Home Assistant se karta:
- ✅ **Automaticky zkopíruje** do `/config/www/cez_hdo/`
- ✅ **Automaticky zaregistruje** v systému bez manuální konfigurace
- ✅ **Ihned k použití** - žádné další kroky nejsou potřeba

### 🔧 Ruční přidání karty (pouze pokud automatická selže)

Pokud by se karta z nějakého důvodu nezaregistrovala automaticky:

1. **Přidejte zdroj do Lovelace:**
   - Jděte na **Nastavení** → **Dashboardy** → **Zdroje**
   - Klikněte **Přidat zdroj**
   - URL: `/local/cez_hdo/cez-hdo-card.js`
   - Typ zdroje: **JavaScript Module**
   - Klikněte **Vytvořit**

2. **Restartujte Home Assistant**

### Konfigurace karty

Přidejte do dashboardu:

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

## 📊 Entity a senzory

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

## 🔍 Debug a řešení problémů

### Debug logování

Pro detailní logování přidejte do `configuration.yaml`:

```yaml
logger:
  default: error
  logs:
    custom_components.cez_hdo.downloader: debug
```

### Řešení problémů

1. **Zkontrolujte region a kód** - otestujte URL v prohlížeči:
   ```
   https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/REGION?code=KÓD
   ```
2. **Zkontrolujte logy** - Developer Tools → Logs
3. **Restartujte HA** po změnách konfigurace
4. **Vyčistěte cache** prohlížeče (Ctrl+F5) pro Lovelace kartu

### Debug logy obsahují

- 🗓️ Výběr kalendáře (pracovní dny vs víkendy/svátky)
- 🔍 Seznam všech HDO období pro aktuální den
- ✅ Aktuální stav (nízký/vysoký tarif) se zbývajícím časem

**Zobrazení debug logů:**

1. **Developer Tools** → **Logs**
2. **Klikněte na "Zobrazit nezpracované logy"**
3. **Filtrujte:** `custom_components.cez_hdo`
