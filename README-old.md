# ČEZ HDO - Senzor pro Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

## 📑 Obsah

- [� Obsah](#-obsah)
- [📋 O integraci](#-o-integraci)
- [✨ Funkce integrace](#-funkce-integrace)
- [🚀 Instalace](#-instalace)
  - [Krok 1: Instalace přes HACS](#krok-1-instalace-přes-hacs)
  - [Krok 2: Konfigurace](#krok-2-konfigurace)
    - [Podporované distribuční kódy](#podporované-distribuční-kódy)
      - [**Region STŘED**](#region-střed)
      - [**Region MORAVA**](#region-morava)
      - [**Region ZÁPAD**](#region-západ)
      - [**Region VÝCHOD**](#region-východ)
      - [**Region SEVER**](#region-sever)
  - [Krok 3: Přidání Lovelace karty](#krok-3-přidání-lovelace-karty)
    - [Automatická instalace (doporučeno)](#automatická-instalace-doporučeno)
    - [Ruční instalace (pokud automatická nefunguje)](#ruční-instalace-pokud-automatická-nefunguje)
  - [Krok 4: Restartování Home Assistant](#krok-4-restartování-home-assistant)
- [🎨 Custom Lovelace Card](#-custom-lovelace-card)
- [📊 Entity](#-entity)
  - [Binary Sensors](#binary-sensors)
  - [Sensors](#sensors)
  - [Atributy](#atributy)
- [� Debug logování](#-debug-logování)
- [🔧 Řešení problémů](#-řešení-problémů)
- [🤖 GitHub Copilot - Pracovní instrukce](#-github-copilot---pracovní-instrukce)

## 📋 O integraci

Tento senzor stahuje data z webu [ČEZ Distribuce HDO](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html).
Integrace vyžaduje **region** a **kód**. Tyto informace lze získat ze smlouvy s ČEZ CZ nebo z [webových stránek ČEZ Distribuce](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html).

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
    code: "405"  # Váš distribuční kód
    region: stred # Váš region
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)

binary_sensor:
  - platform: cez_hdo
    code: "405"  # Váš distribuční kód
    region: stred # Váš region
    scan_interval: 300  # Aktualizace každých 5 minut (volitelné)
```

#### Podporované distribuční kódy

Integrace podporuje všechny HDO kódy ČEZ Distribuce podle regionů:

##### **Region STŘED**

| Kód | Popis povelu | Platnost | Poznámka |
|-----|-------------|----------|----------|
| 153 | A1B4DP5 | po - pá | Blokování/odblokování spotřebičů v určených časech dle HDO |
| 201 | A1B7DP5 | po - pá | Podobně, odlišné časy HDO |
| 219 | A1B8DP7 | po - pá | Individuální rozvrh pro odběratele |
| **405** | **A3B4DP1** | **po - pá/so - ne** | **Modelové nízké/vysoké tarify, nejčastěji v domácnostech** |
| 406 | A3B4DP2 | po - pá/so - ne | Stejný typ jako 405, jiné časy nebo bloky |
| 410 | A3B4DP6 | po - pá/so - ne | Specifické pro některé oblasti, jiné rozvrhy |
| 437 | A3B6DP1 | po - pá | Rozšířený řetězec blokování |
| 438 | A3B6DP2 | po - pá | Téměř stejně jako 437, jiná oblast nebo časy |
| 442 | A3B6DP6 | po - pá | Alternativní rozvrhy odběru |
| 458 | A3B7DP6 | so - ne | Odběrové období pro specifické zákazníky |

##### **Region MORAVA**

| Kód | Popis povelu | Platnost | Poznámka |
|-----|-------------|----------|----------|
| 149 | A1B4DP1 | po - pá | Detailní časy blokování/odblokování |
| **154** | **A1B4DP6** | **po - pá/so-ne** | **Typické domácnosti** |
| 184 | A1B6DP4 | po - pá | Jednotlivé oblasti s různými spotřebiči |
| 185 | A1B6DP5 | so - ne | Víkendové režimy odběru |
| 187 | A1B6DP7 | po - pá | Konkrétní oblast |
| 218 | A1B8DP6 | so - ne | Časy pro spotřebiče |

##### **Region ZÁPAD**

| Kód | Popis povelu | Platnost | Poznámka |
|-----|-------------|----------|----------|
| **153** | **A1B4DP5** | **po - pá** | **Typické domovní HDO časy** |
| **154** | **A1B4DP6** | **po - pá/so-ne** | **Častý kód odběrných míst** |
| 169 | A1B5DP5 | po - pá | Odlišené časy proti 153 |
| 170 | A1B5DP6 | po - pá/so-ne | Další obdobné využití |
| 201 | A1B7DP5 | po - pá/so-ne | Varianta pro domácnosti |
| 213 | A1B8DP1 | po - pá | Komplexnější rozvrh spotřeby |
| 217 | A1B8DP5 | po - pá | Ostatní řetězce domácností |
| 218 | A1B8DP6 | po - pá | Ojediněle používané |
| 410 | A3B4DP6 | po - pá/so-ne | Podobně jako střed, rozdílný časový rozvrh |

##### **Region VÝCHOD**

| Kód | Popis povelu | Platnost | Poznámka |
|-----|-------------|----------|----------|
| 153 | A1B4DP5 | po - pá | Detailní rozvrh |
| 185 | A1B6DP5 | po - pá | Podrobnosti blokování spotřebičů |
| 201 | A1B7DP5 | po - pá | Standardní domácnosti |
| 453 | A3B7DP1 | po - pá | Odlišná oblast ve východě |
| 454 | A3B7DP2 | po - pá | Víkendové časy |
| 458 | A3B7DP6 | po - pá | Specifické pro vybrané oblasti |

##### **Region SEVER**

| Kód | Popis povelu | Platnost | Poznámka |
|-----|-------------|----------|----------|
| 12 | A1B4DP1 | po - pá | Typické HDO v severních Čechách |
| 13 | A1B6DP3 | po - pá | Blokování spotřebičů |
| 14 | A1B8DP3 | po - pá | Alternativní rozvrhy |
| 82 | A1B8DP5 | po - pá | Standardní domácnosti |
| 83 | A1B5DP6 | so - ne | Specifický víkendový odběr |
| 410 | A3B4DP6 | po - pá/so-ne | Univerzální časy domácnosti |

**💡 Tip:** Nejčastěji používané kódy pro domácnosti jsou **405** (střed), **154** (morava/západ) a **410** (univerzální).

### Krok 3: Přidání Lovelace karty

Karta se automaticky nainstaluje při prvním spuštění integrace.

#### Automatická instalace (doporučeno)

Po restartu Home Assistant se karta automaticky přidá do zdrojů.

#### Ruční instalace (pokud automatická nefunguje)

1. **Přidejte zdroj do Lovelace:**
   - Jděte na **Nastavení** → **Dashboardy** → **Zdroje**
   - Klikněte **Přidat zdroj**
   - URL: `/local/cez-hdo-card.js`
   - Typ zdroje: **JavaScript Module**
   - Klikněte **Vytvořit**

2. **Přidejte kartu do dashboardu:**

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

## 🔧 Řešení problémů

Pokud máte problémy s integrací:

1. **Zkontrolujte region a kód** - otestujte URL v prohlížeči
2. **Zkontrolujte logy** - Developer Tools → Logs
3. **Restartujte HA** po změnách konfigurace
4. **Vyčistěte cache** prohlížeče (Ctrl+F5) pro Lovelace kartu

## 🤖 GitHub Copilot - Pracovní instrukce

Pro vývojáře pracující s GitHub Copilot na tomto projektu:

**Template pro začátek práce:**

```text
@GitHub Copilot - pracovní instrukce:
- Používej isBackground: true pro všechny terminálové příkazy
- Dev struktura: /dev/, Production: /custom_components/
- Build: ./dev/deploy-dev.sh, Clean: ./dev/deploy-dev.sh clean
Řiď se těmito pravidly.
```
