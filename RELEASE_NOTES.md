# Release Notes – ČEZ HDO

---

## v3.1.0 (2026-02-04)

### 🚀 Hlavní změny

Verze 3.1.0 přináší **podporu CAPTCHA ověření** a nové senzory pro sledování platnosti dat.

#### CAPTCHA ochrana API

- ČEZ Distribuce zavedl CAPTCHA ochranu na svém API
- **Nový krok v konfiguraci** – zobrazí se obrázek CAPTCHA a uživatel zadá kód
- Data jsou načtena jednorázově a uložena do cache
- **Platnost dat 6 dní** – poté je nutné překonfigurovat integraci

#### Nové entity pro sledování platnosti dat

| Typ    | Entita                        | Popis                     |
| ------ | ----------------------------- | ------------------------- |
| Binary | `cez_hdo_data_valid_*`        | Data jsou platná (on/off) |
| Sensor | `cez_hdo_data_valid_until_*`  | Datum vypršení platnosti  |
| Sensor | `cez_hdo_data_age_days_*`     | Stáří dat ve dnech        |
| Sensor | `cez_hdo_days_until_expiry_*` | Dnů do vypršení           |

#### Automatická upozornění

- **Den 5:** Persistent notification s varováním
- **Den 6:** Persistent notification o vypršení dat

### ✨ Vylepšení

- Lepší error handling při validaci CAPTCHA
- Options Flow také podporuje CAPTCHA pro obnovení dat
- Aktualizovaná dokumentace s příklady automatizací

### 📚 Dokumentace

- Přidána sekce "Platnost dat a obnovení" do user-guide
- Aktualizován known-issues s informací o vyřešeném CAPTCHA problému
- Přidány příklady automatizací pro upozornění na vypršení dat

---

## v3.0.1 (2026-02-03)

### 📚 Dokumentace

- Přidáno upozornění o CAPTCHA problému do README

---

## v3.0.0 (2026-02-02)

### 🚀 Hlavní změny

Verze 3.0.0 přináší **kompletní přepracování** integrace
s důrazem na moderní architekturu Home Assistantu.

#### Config Flow – GUI konfigurace

- **Žádný YAML** – integrace se konfiguruje přes Settings → Devices & Services
- **4-krokový průvodce:**
  1. Zadání EAN
  2. Výběr signálu
  3. Přípona entit (uživatelsky konfigurovatelná)
  4. Nastavení cen NT/VT
- **Options Flow** – možnost změnit nastavení kdykoli po instalaci
- **Více signálů pro EAN** – stejné EAN lze přidat vícekrát s různými signály

#### Device Registry

- Všechny entity jsou seskupeny pod **hub** (posledních 6 číslic EAN)
- Každý signál vytváří vlastní **zařízení** s kódem signálu
- Lepší přehled v UI Home Assistantu

#### Nové úložiště dat

- Data přesunuta z `www/cez_hdo/` do `custom_components/cez_hdo/data/`
- **Per-EAN cache** – každé EAN má vlastní soubory
- Podpora více instancí integrace

#### Diagnostika

- Export diagnostických dat přes UI
- Settings → Devices → ČEZ HDO → ⋮ → Download diagnostics
- Automatické maskování citlivých údajů

#### Lokalizace

- **Lokalizace názvů entit** – podpora `translation_key` pro automatický překlad friendly_name entit podle systémového jazyka HA
- **Dvojjazyčná dokumentace** – kompletní CS a EN verze všech dokumentů

### ✨ Vylepšení

- **Ceny v integraci** – ceny se nastavují v Options Flow, ne v kartě
- **API update interval** – změněn na 1 hodinu
- **State update interval** – aktualizace stavu každých 5 sekund
- **Lepší chybové hlášky při zadávání EAN** – s odkazy na portál ČEZ
- **Dynamické texty** – pro počet signálů
- **Maskování EAN v logu** – zobrazeny pouze poslední číslice
- **Bez emoji v logu** – nahrazeny textovými značkami `[NT]`/`[VT]`

### 🐛 Opravy

- **Lovelace karta** – opraveny výchozí entity ID v `DEFAULT_ENTITIES`
- **Entity discovery** – karta správně detekuje entity podle anglických prefixů
- Opraveny odkazy na obrázky v dokumentaci
- Opraveno číslování seznamů v user-guide

### 🔧 Technické změny

- DataUpdateCoordinator pro centralizovanou správu dat
- Refaktoring podle Home Assistant Style Guidelines
- Vylepšené logování

### 📚 Dokumentace

- **README_EN.md** – přidána anglická verze hlavního README
- **Dvojjazyčná dokumentace:**
  - `docs/cs/` – česká dokumentace
  - `docs/en/` – anglická dokumentace
- **Obrázky** – reorganizovány do `img/cs/` a `img/en/`

### ⚠️ Breaking Changes

1. **YAML konfigurace již nefunguje** – nutno přidat přes GUI
2. **Nové cesty k datům** – smazat starou složku `www/cez_hdo/`
3. **Ceny v kartě** – pole odebrána, nastavují se v integraci

### 📋 Postup upgradu z v2.x

1. **Smazat YAML konfiguraci** z `configuration.yaml`
2. **Aktualizovat** přes HACS
3. **Restart** Home Assistant
4. **Smazat staré entity** (Nastavení → Entity → smazat vše obsahující `cez_hdo`)
5. **Přidat integraci** přes GUI
6. **Smazat složku** `www/cez_hdo/`

Detailní postup: [Upgrade Guide (CS)](docs/cs/upgrade-guide.md) | [Upgrade Guide (EN)](docs/en/upgrade-guide.md)

---

## v3.0.0-RC.3 (2026-02-01)

### 🐛 Opravy

- **Lovelace karta** – opraveny výchozí entity ID v `DEFAULT_ENTITIES`
  (odstraněny staré české názvy jako `cez_hdo_nizky_tarif_aktivni`)
- **Entity discovery** – karta nyní správně detekuje entity
  podle anglických prefixů (`cez_hdo_lowtariffactive_*`)

### ✨ Vylepšení

- **Lokalizace názvů entit** – přidána podpora `translation_key`
  pro automatický překlad friendly_name entit podle systémového jazyka HA
- **Dvojjazyčná dokumentace** – kompletní CS a EN verze všech dokumentů:
  - `docs/cs/` – česká dokumentace
  - `docs/en/` – anglická dokumentace
- **README_EN.md** – přidána anglická verze hlavního README
- **Obrázky** – reorganizovány do `img/cs/` a `img/en/`

### 📝 Dokumentace

- Opraveny odkazy na obrázky v README_EN.md
- Aktualizována konfigurace markdownlint
- Opraveno číslování seznamů v user-guide

---

## v3.0.0-RC.2 (2026-01-30)

### 🚀 Hlavní změny

Verze 3.0.0 přináší **kompletní přepracování** integrace
s důrazem na moderní architekturu Home Assistantu.

#### Config Flow – GUI konfigurace

- **Žádný YAML** – integrace se konfiguruje přes Settings → Devices & Services
- **4-krokový průvodce:**
  1. Zadání EAN
  2. Výběr signálu
  3. Přípona entit (uživatelsky konfigurovatelná)
  4. Nastavení cen NT/VT
- **Options Flow** – možnost změnit nastavení kdykoli po instalaci
- **Více signálů pro EAN** – stejné EAN lze přidat vícekrát
  s různými signály

#### Device Registry

- Všechny entity jsou seskupeny pod jedno **zařízení**
- Název zařízení: "ČEZ HDO XXXXXX" (posledních 6 číslic EAN)
- Lepší přehled v UI Home Assistantu

#### Nové úložiště dat

- Data přesunuta z `www/cez_hdo/` do `custom_components/cez_hdo/data/`
- **Per-EAN cache** – každé EAN má vlastní soubory
- Podpora více instancí integrace

#### Diagnostika

- Export diagnostických dat přes UI
- Settings → Devices → ČEZ HDO → ⋮ → Download diagnostics
- Automatické maskování citlivých údajů

### ✨ Vylepšení

- **Ceny v integraci** – ceny se nastavují v Options Flow, ne v kartě
- **API update interval** – změněn na 1 hodinu
- **State update interval** – aktualizace stavu každých 5 sekund
- **Lepší chybové hlášky při zadávání EAN** – s odkazy na portál ČEZ
- **Dynamické texty** – pro počet signálů
- **Maskování EAN v logu** – zobrazeny pouze poslední číslice
- **Bez emoji v logu** – nahrazeny textovými značkami `[NT]`/`[VT]`

### 🔧 Technické změny

- DataUpdateCoordinator pro centralizovanou správu dat
- Refaktoring podle Home Assistant Style Guidelines
- Vylepšené logování

### ⚠️ Breaking Changes

1. **YAML konfigurace již nefunguje** – nutno přidat přes GUI
2. **Nové cesty k datům** – smazat starou složku `www/cez_hdo/`
3. **Ceny v kartě** – pole odebrána, nastavují se v integraci

### 📋 Postup upgradu

Viz [Upgrade Guide](docs/cs/upgrade-guide.md) pro detailní postup.

---

## v2.2.0

### 🚀 Nové funkce

#### HDO Rozvrh – senzor a vizualizace

- Nový senzor `sensor.cez_hdo_rozvrh` s 7denním rozvrhem
- Vizuální timeline v kartě
- Barevné bloky pro NT (zelená) a VT (oranžová)

#### Nové přepínače v editoru karty

- Zobrazit titulek
- Zobrazit stavy tarifů
- Zobrazit HDO rozvrh
- Zobrazit ceny v legendě rozvrhu

### ✨ Vylepšení (v2.2.0)

- Správné zpracování času 24:00 (půlnoc)
- Opravena duplicita aktuálního dne
- Opraveno psaní titulku bez scrollování
