# Release Notes – ČEZ HDO

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
