# Release Notes – ČEZ HDO

---

## v3.2.3 (2026-02-28)

### 🐛 Opravy

#### Opraveno denní automatické obnovení dat

- **Auto-refresh nyní běží denně** – předchozí verze plánovala auto-refresh pouze když byla data 5+ dnů stará
- **Opraveno:** Data se nyní automaticky obnovují každý den (ne jen před expirací)
- Metoda `_async_schedule_auto_refresh` již obsahuje logiku pro reset čítačů pro nový den

---

## v3.2.2 (2026-02-26)

### 🚀 Hlavní změny

#### Migrace na Home Assistant Store API

- **Nový systém ukládání dat** – integrace nyní používá nativní Home Assistant Store helper
- **Atomické zápisy** – data jsou ukládána bezpečně bez rizika poškození při výpadku
- **Automatická správa** – HA se stará o umístění souborů v `.storage/`

#### Vylepšené logování

- **Detailnější logy API** – každý krok procesu je nyní logován s číslem pokusu
- **Strukturované zprávy** – jasné informace o tom, co se děje (API volání, výsledky)
- **Odstraněn zavádějící log** – "Manually updated" se již nezobrazuje každých 5 sekund

### 🐛 Opravy

- **Opravena diagnostika** – funguje správně s novým Store API
- **Odstraněn nepoužívaný kód** – vyčištěny legacy soubory a funkce

### 🌐 Lokalizace

- **Služby přeloženy do angličtiny** – `services.yaml` nyní v angličtině dle HA best practices
- **Lokalizace služeb** – české překlady služeb přesunuty do `translations/cs.json`
- **Komentáře v angličtině** – veškeré komentáře v kódu jsou nyní anglicky

### 📁 Změny v ukládání dat

Nová umístění souborů (spravuje Home Assistant automaticky):

| Soubor       | Nové umístění                           |
| ------------ | --------------------------------------- |
| Cache dat    | `.storage/cez_hdo.cache_XXXXXX`         |
| Ceny         | `.storage/cez_hdo.prices_XXXXXX`        |
| Stav refresh | `.storage/cez_hdo.refresh_state_XXXXXX` |

> **Poznámka:** `XXXXXX` = posledních 6 číslic EAN

---

## v3.2.1 (2026-02-26)

### 🚨 Breaking Changes

- **Změna umístění cache** z `custom_components/cez_hdo/data/` na `.storage/cez_hdo/`
- Po aktualizaci je nutné:

> - **Znovu nakonfigurovat integraci**, nebo
> - **Ručně zkopírovat data:** z /config/custom_components/cez_hdo/data/*.json do /config/.storage/cez_hdo
>
>   ```bash
>   mkdir -p /config/.storage/cez_hdo
>   cp /config/custom_components/cez_hdo/data/*.json /config/.storage/cez_hdo/
>   ```

### 🐛 Opravy

#### Data přežijí aktualizaci integrace

- **Přesun cache do `.storage/cez_hdo/`** – data (HDO rozvrh, ceny, stav auto-refresh) jsou nyní uložena v bezpečném umístění
- **Opraveno:** Budoucí aktualizace přes HACS již nesmažou uložená data

### ⚠️ Důležité pro uživatele přecházející z 3.2.0

**HACS smaže celou složku integrace při aktualizaci**, takže data z verze 3.2.0 byla ztracena.

**Řešení:**

- Znovu nakonfigurujte integraci, nebo
- Ručně zkopírujte data:

  ```bash
  mkdir -p /config/.storage/cez_hdo
  cp /config/custom_components/cez_hdo/data/*.json /config/.storage/cez_hdo/
  ```

---

## v3.2.0 (2026-02-25)

### 🚀 Hlavní změny

#### Vylepšené automatické obnovování dat

- **Spolehlivější získávání dat** – vylepšená logika pro automatické obnovení HDO dat
- **Retry mechanismus** – při selhání se systém pokusí znovu získat data (až 3 pokusy)
- **Lepší error handling** – robustnější zpracování chyb při komunikaci s API
- **Detailnější logování** – přehlednější informace o průběhu aktualizace dat v logu

### ✨ Vylepšení

- Optimalizovaná komunikace s ČEZ Distribuce API
- Vylepšené zprávy v logu pro snazší diagnostiku
- Zvýšená spolehlivost při nestabilním připojení

---

## v3.1.1 (2026-02-05)

### 🐛 Opravy

#### Kompatibilita s Home Assistant 2026.02+

- **Opravena chyba** `'LovelaceData' object has no attribute 'mode'`
- V HA 2026.02+ byla změněna struktura `LovelaceData` – objekt již nemá atribut `mode`
- Nová detekce storage režimu pomocí kontroly typu resources kolekce

**Fixes:** [#62](https://github.com/Cmajda/ha_cez_distribuce/issues/62)

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
