# ČEZ HDO - Uživatelská dokumentace

## 📑 Obsah

- [📑 Obsah](#-obsah)
- [🚀 Instalace](#-instalace)
  - [Automatická instalace přes HACS](#automatická-instalace-přes-hacs)
  - [Manuální instalace](#manuální-instalace)
- [⚙️ Konfigurace](#️-konfigurace)
  - [Základní konfigurace](#základní-konfigurace)
  - [EAN číslo - jak ho najít](#ean-číslo---jak-ho-najít)
  - [Zjištění dostupných signálů](#zjištění-dostupných-signálů)
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
    ean: "VAŠE_EAN_ČÍSLO"  # Váš EAN kód odběrného místa
    signal: "HDO1"  # Volitelně - konkrétní signál (jinak se vybere automaticky)
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)

binary_sensor:
  - platform: cez_hdo
    ean: "VAŠE_EAN_ČÍSLO"  # Váš EAN kód odběrného místa
    signal: "HDO1"  # Volitelně - konkrétní signál (jinak se vybere automaticky)
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)
```

**Chování bez specifikace signálu:**

- Integrace automaticky použije **nejpravděpodobnější signál** z dostupných pro daný EAN
- Pro většinu uživatelů je automatický výběr dostatečný
- Můžete použít službu `cez_hdo.list_signals` pro zjištění dostupných signálů

### EAN číslo - jak ho najít

EAN číslo (13 nebo 18 číslic) najdete na:

- **Faktuře od ČEZ Distribuce** - obvykle v záhlaví nebo v detailech odběrného místa
- **Smlouvě o připojení** - jako identifikace odběrného místa
- **Aplikaci ČEZ** - v detailech odběrného místa
- **Zákaznickém portálu ČEZ** - v sekci odběrná místa

**Formát EAN:** `123456789101112113` (18 číslic) nebo `1234567891456` (13 číslic)

### Zjištění dostupných signálů

Pro zjištění všech dostupných HDO signálů pro váš EAN použijte službu:

```yaml
service: cez_hdo.list_signals
data:
  ean: "VAŠE_EAN_ČÍSLO"
```

Služba vrátí seznam všech dostupných signálů s jejich názvy a časovými rozpisy.

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

Kartu jde konfigurovat buď ručně v YAML, nebo ve vizuálním editoru Lovelace (UI) – tam si můžete pohodlně vybrat entity přes entity picker.

Přidejte do dashboardu:

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

1. **Zkontrolujte EAN číslo** - musí být ve formátu 13 nebo 18 číslic
2. **Otestujte dostupné signály** - použijte službu `cez_hdo.list_signals`
3. **Zkontrolujte logy** - Developer Tools → Logs
4. **Restartujte HA** po změnách konfigurace
5. **Vyčistěte cache** prohlížeče (Ctrl+F5) pro Lovelace kartu

### Debug logy obsahují

- 📡 Volání ČEZ API s EAN parametrem
- 🔍 Seznam všech dostupných signálů pro EAN
- 🎯 Automatický výběr nejvhodnějšího signálu
- 🗓️ Zpracování časových období HDO
- ✅ Aktuální stav (nízký/vysoký tarif) se zbývajícím časem

**Zobrazení debug logů:**

1. **Developer Tools** → **Logs**
2. **Klikněte na "Zobrazit nezpracované logy"**
3. **Filtrujte:** `custom_components.cez_hdo`
