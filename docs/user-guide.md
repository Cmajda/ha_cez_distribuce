# ⚡️ ČEZ HDO – Uživatelská dokumentace

Tato stránka je kompletní návod pro běžného uživatele: instalace, konfigurace, vytvořené entity, Lovelace karta a řešení problémů.

## 📑 Obsah

- [📑 Obsah](#-obsah)
- [🚀 Instalace](#-instalace)
  - [Instalace přes HACS (doporučeno)](#instalace-přes-hacs-doporučeno)
- [⚙️ Konfigurace (`configuration.yaml`)](#️-konfigurace-configurationyaml)
  - [Kde najít EAN](#kde-najít-ean)
- [📦 Vytvářené entity a jejich význam](#-vytvářené-entity-a-jejich-význam)
  - [Binary sensors](#binary-sensors)
  - [Sensors](#sensors)
- [🎴 Lovelace karta](#-lovelace-karta)
  - [Přidání karty](#přidání-karty)
  - [Ukázka karty](#ukázka-karty)
  - [Nastavení entit v UI](#nastavení-entit-v-ui)
  - [Kompletní konfigurace karty](#kompletní-konfigurace-karty)
    - [Titulek](#titulek)
    - [Výběr entit](#výběr-entit)
    - [Přepínače zobrazení](#přepínače-zobrazení)
    - [Cenová pole](#cenová-pole)
  - [Příklad kompletní YAML konfigurace](#příklad-kompletní-yaml-konfigurace)
  - [Ruční registrace zdroje (jen pokud se karta nenačítá)](#ruční-registrace-zdroje-jen-pokud-se-karta-nenačítá)
- [💰 Nastavení cen tarifů](#-nastavení-cen-tarifů)
  - [Nastavení v Lovelace kartě](#nastavení-v-lovelace-kartě)
  - [Nastavení přes službu](#nastavení-přes-službu)
  - [Zobrazení cen v kartě](#zobrazení-cen-v-kartě)
- [📊 Použití v Energy Dashboard](#-použití-v-energy-dashboard)
- [📅 HDO rozvrh – vizualizace v kartě](#-hdo-rozvrh--vizualizace-v-kartě)
  - [Aktivace rozvrhu](#aktivace-rozvrhu)
  - [Popis vizualizace](#popis-vizualizace)
  - [Formát dat senzoru](#formát-dat-senzoru)
- [🎛️ Přehled přepínačů v editoru karty](#️-přehled-přepínačů-v-editoru-karty)
- [🔧 Co dělat, když komponenta nefunguje](#-co-dělat-když-komponenta-nefunguje)
- [🔍 Diagnostika (když chcete poslat logy)](#-diagnostika-když-chcete-poslat-logy)

## 🚀 Instalace

### Instalace přes HACS (doporučeno)

1. Otevřete HACS → Integrations
1. Přidejte repozitář jako Custom repository (Integration):

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

1. Nainstalujte integraci „ČEZ HDO"
1. Restart Home Assistant

Poznámka: po instalaci/aktualizaci a restartu HA může být potřeba jednou udělat `Ctrl+F5`, aby se Lovelace karta objevila v seznamu karet.

## ⚙️ Konfigurace (`configuration.yaml`)

Přidejte do `configuration.yaml` přesně tento blok (EAN je povinný):

```yaml
sensor:
  - platform: cez_hdo
    ean: "Váš EAN"

binary_sensor:
  - platform: cez_hdo
    ean: "Váš EAN"
```

Pak restartujte Home Assistant.

### Kde najít EAN

EAN je identifikátor odběrného místa a najdete ho typicky:

- na faktuře / vyúčtování
- v portálu dodavatele/distributora

## 📦 Vytvářené entity a jejich význam

Integrace vytváří tyto entity (výchozí názvy):

### Binary sensors

- `binary_sensor.cez_hdo_nizky_tarif_aktivni` – nízký tarif je aktivní (`on/off`)
- `binary_sensor.cez_hdo_vysoky_tarif_aktivni` – vysoký tarif je aktivní (`on/off`)

### Sensors

- `sensor.cez_hdo_nizky_tarif_zacatek` – čas začátku nízkého tarifu (např. `01:10`)
- `sensor.cez_hdo_nizky_tarif_konec` – čas konce nízkého tarifu (např. `08:30`)
- `sensor.cez_hdo_nizky_tarif_zbyva` – zbývající čas do změny tarifu
- `sensor.cez_hdo_vysoky_tarif_zacatek` – čas začátku vysokého tarifu
- `sensor.cez_hdo_vysoky_tarif_konec` – čas konce vysokého tarifu
- `sensor.cez_hdo_vysoky_tarif_zbyva` – zbývající čas do změny tarifu
- `sensor.cez_hdo_aktualni_cena` – aktuální cena elektřiny v Kč/kWh (podle aktivního tarifu)
- `sensor.cez_hdo_rozvrh` – 7denní rozvrh HDO pro vizualizaci v kartě
- `sensor.cez_hdo_surova_data` – surová data / timestamp (diagnostika)

## 🎴 Lovelace karta

### Přidání karty

V Lovelace přidejte kartu typu:

```yaml
type: custom:cez-hdo-card
```

### Ukázka karty

![ČEZ HDO karta](../entity_card.png)

### Nastavení entit v UI

- Karta má UI editor a nabízí výběr entit.
- Tip: když necháte nějaké pole prázdné, karta použije výchozí entity (pokud existují).

### Kompletní konfigurace karty

![Editor karty](../entity_card_edit.png)

Editor karty obsahuje následující nastavení:

#### Titulek

Textové pole pro zadání názvu karty. Výchozí hodnota je "ČEZ HDO". Můžete změnit na libovolný text nebo nechat prázdné.

#### Výběr entit

Karta automaticky detekuje entity ČEZ HDO, ale můžete je ručně změnit:

| Entity picker            | Popis                           | Výchozí entita                              |
| ------------------------ | ------------------------------- | ------------------------------------------- |
| Nízký tarif (binary)     | Binární senzor pro stav NT      | `binary_sensor.cez_hdo_nizky_tarif_aktivni` |
| Vysoký tarif (binary)    | Binární senzor pro stav VT      | `binary_sensor.cez_hdo_vysoky_tarif_aktivni`|
| NT začátek               | Čas začátku nízkého tarifu      | `sensor.cez_hdo_nizky_tarif_zacatek`        |
| NT konec                 | Čas konce nízkého tarifu        | `sensor.cez_hdo_nizky_tarif_konec`          |
| NT zbývá                 | Zbývající čas do změny z NT     | `sensor.cez_hdo_nizky_tarif_zbyva`          |
| VT začátek               | Čas začátku vysokého tarifu     | `sensor.cez_hdo_vysoky_tarif_zacatek`       |
| VT konec                 | Čas konce vysokého tarifu       | `sensor.cez_hdo_vysoky_tarif_konec`         |
| VT zbývá                 | Zbývající čas do změny z VT     | `sensor.cez_hdo_vysoky_tarif_zbyva`         |
| Rozvrh HDO               | Senzor s 7denním rozvrhem       | `sensor.cez_hdo_rozvrh`                     |

#### Přepínače zobrazení

> **Poznámka:** Pořadí přepínačů v editoru odpovídá pořadí zobrazení prvků na kartě – od shora dolů.

| # | Přepínač | Popis | Výchozí |
| - | -------- | ----- | ------- |
| 1 | **Zobrazit titulek** | Zobrazí/skryje nadpis karty úplně nahoře. Když je vypnutý, karta nemá žádný hlavní nadpis. | ✅ Zapnuto |
| 2 | **Zobrazit stavy tarifů** | Zobrazí dva boxy vedle sebe – "Nízký tarif" a "Vysoký tarif" s textem "Aktivní" nebo "Neaktivní". Aktivní tarif je zvýrazněn barvou (zelená pro NT, oranžová pro VT). | ✅ Zapnuto |
| 3 | **Zobrazit ceny u tarifů** | Pod textem "Aktivní/Neaktivní" v boxech tarifů zobrazí nastavenou cenu (např. "2.50 Kč/kWh"). Vyžaduje nastavené ceny v polích níže. | ❌ Vypnuto |
| 4 | **Zobrazit časy (začátek/konec)** | Zobrazí sekci s časy: NT začátek, NT konec, VT začátek, VT konec. Užitečné pro plánování spotřeby. | ✅ Zapnuto |
| 5 | **Zobrazit zbývající čas** | Zobrazí sekci "NT zbývá" a "VT zbývá" – kolik času zbývá do konce aktuálního tarifu nebo do začátku dalšího. | ✅ Zapnuto |
| 6 | **Zobrazit aktuální cenu** | Zobrazí velký zvýrazněný box s aktuální cenou elektřiny. Barva pozadí odpovídá aktivnímu tarifu (zelená = NT, oranžová = VT). Pod cenou je text "Nízký tarif" nebo "Vysoký tarif". | ✅ Zapnuto |
| 7 | **Zobrazit HDO rozvrh** | Zobrazí vizuální timeline s 7denním rozvrhem HDO. Každý den má pruh s barevnými bloky: zelená = NT, oranžová = VT. Časová osa 0:00–24:00. | ❌ Vypnuto |
| 8 | **Zobrazit ceny v legendě rozvrhu** | V legendě rozvrhu (nad grafem) přidá k textu "NT" a "VT" také ceny (např. "NT 2.50 Kč"). Vyžaduje nastavené ceny a zapnutý rozvrh. | ❌ Vypnuto |
| 9 | **Kompaktní režim** | Zmenší velikost karty – menší fonty, menší odsazení. Vhodné pro menší displeje nebo když chcete více karet vedle sebe. | ❌ Vypnuto |

#### Cenová pole

| Pole | Popis |
| ---- | ----- |
| **Cena NT (Kč/kWh)** | Cena za kWh v nízkém tarifu (např. 2.50) |
| **Cena VT (Kč/kWh)** | Cena za kWh ve vysokém tarifu (např. 4.50) |

Ceny se:

- Ukládají perzistentně (přežijí restart HA)
- Synchronizují se senzorem `sensor.cez_hdo_aktualni_cena`
- Zobrazují v kartě podle nastavení přepínačů

### Příklad kompletní YAML konfigurace

```yaml
type: custom:cez-hdo-card
title: Můj HDO
entities:
  low_tariff: binary_sensor.cez_hdo_nizky_tarif_aktivni
  high_tariff: binary_sensor.cez_hdo_vysoky_tarif_aktivni
  low_start: sensor.cez_hdo_nizky_tarif_zacatek
  low_end: sensor.cez_hdo_nizky_tarif_konec
  low_duration: sensor.cez_hdo_nizky_tarif_zbyva
  high_start: sensor.cez_hdo_vysoky_tarif_zacatek
  high_end: sensor.cez_hdo_vysoky_tarif_konec
  high_duration: sensor.cez_hdo_vysoky_tarif_zbyva
  schedule: sensor.cez_hdo_rozvrh
show_title: true
show_tariff_status: true
show_tariff_prices: true
show_times: true
show_duration: true
show_price: true
show_schedule: true
show_schedule_prices: true
compact_mode: false
low_tariff_price: 2.50
high_tariff_price: 4.50
```

### Ruční registrace zdroje (jen pokud se karta nenačítá)

Pokud se karta v seznamu karet nezobrazuje ani po `Ctrl+F5`:

1. Nastavení → Dashboardy → Zdroje
1. Přidat zdroj
1. URL: `/cez_hdo/cez-hdo-card.js`
1. Typ: JavaScript Module
1. Restart Home Assistant

## 💰 Nastavení cen tarifů

### Nastavení v Lovelace kartě

V editoru karty najdete pole pro zadání cen:

- **Cena NT (Kč/kWh)** – cena za kWh v nízkém tarifu
- **Cena VT (Kč/kWh)** – cena za kWh ve vysokém tarifu

Po zadání cen a uložení karty se automaticky aktualizuje senzor `sensor.cez_hdo_aktualni_cena`.

### Nastavení přes službu

Ceny lze nastavit i přes službu:

```yaml
service: cez_hdo.set_prices
data:
  low_tariff_price: 2.50
  high_tariff_price: 4.50
```

### Zobrazení cen v kartě

V editoru karty jsou dva přepínače:

- **Zobrazit aktuální cenu** – zobrazí velký box s aktuální cenou
- **Zobrazit ceny u tarifů** – zobrazí cenu přímo v boxu NT/VT

## 📊 Použití v Energy Dashboard

1. Nastavení → Dashboardy → Energy
2. V sekci "Electricity grid" klikněte na "Add consumption"
3. Vyberte měřič spotřeby
4. V poli "Use an entity tracking the total costs" nebo "Use an entity with current price" vyberte `sensor.cez_hdo_aktualni_cena`

Senzor automaticky přepíná mezi cenou NT a VT podle aktivního tarifu.
Senzor `sensor.cez_hdo_aktualni_cena` lze použít jako zdroj ceny elektřiny v Energy kartě Home Assistantu.

![Nastavení Energy Dashboard](../integration_energy_ha.png)

## 📅 HDO rozvrh – vizualizace v kartě

Lovelace karta obsahuje integrovanou vizualizaci 7denního HDO rozvrhu:

![HDO rozvrh](../graph.png)

### Aktivace rozvrhu

1. Otevřete editor karty
2. Zapněte přepínač "Zobrazit HDO rozvrh"
3. Volitelně zapněte "Zobrazit ceny v legendě rozvrhu" pro zobrazení cen NT/VT

### Popis vizualizace

- **Zelené bloky** – nízký tarif (NT)
- **Oranžové bloky** – vysoký tarif (VT)
- **Časová osa** – 0:00 až 24:00 pro každý den
- **Legenda** – s volitelným zobrazením cen
- **Tooltip** – při najetí myší zobrazí přesné časy intervalu

### Formát dat senzoru

Senzor `sensor.cez_hdo_rozvrh` poskytuje v atributu `schedule` seznam intervalů:

```json
[
  {"start": "2026-01-27T00:00:00", "end": "2026-01-27T07:15:00", "tariff": "NT", "value": 1},
  {"start": "2026-01-27T07:15:00", "end": "2026-01-27T08:15:00", "tariff": "VT", "value": 0}
]
```

- `tariff`: "NT" (nízký tarif) nebo "VT" (vysoký tarif)
- `value`: 1 pro NT, 0 pro VT

## 🎛️ Přehled přepínačů v editoru karty

| Přepínač                        | Popis                                 |
| ------------------------------- | ------------------------------------- |
| Zobrazit titulek                | Zobrazí/skryje nadpis karty           |
| Zobrazit stavy tarifů           | Zobrazí/skryje boxy s NT/VT stavem    |
| Zobrazit ceny u tarifů          | Zobrazí cenu přímo v boxu NT/VT       |
| Zobrazit časy (začátek/konec)   | Zobrazí časy začátku a konce tarifů   |
| Zobrazit zbývající čas          | Zobrazí zbývající čas do změny tarifu |
| Zobrazit aktuální cenu          | Zobrazí velký box s aktuální cenou    |
| Zobrazit HDO rozvrh             | Zobrazí 7denní vizualizaci rozvrhu    |
| Zobrazit ceny v legendě rozvrhu | Přidá ceny NT/VT k legendě grafu      |
| Kompaktní režim                 | Zmenší kartu                          |

## 🔧 Co dělat, když komponenta nefunguje

Pokud se po instalaci/aktualizaci něco rozbije (karta nejde přidat, nejde načíst JS, nebo jsou chyby v konzoli), postupujte takto:

1. Vynutit refresh: `Ctrl+F5`
1. Odinstalovat doplněk
1. Pokud existuje složka `www/cez_hdo`, smažte ji
1. Znovu nainstalovat doplněk
1. Restart Home Assistant

## 🔍 Diagnostika (když chcete poslat logy)

Nejrychlejší kontrola pro kartu:

- Otevřete v prohlížeči `http://IP_HA:8123/cez_hdo/cez-hdo-card.js`
  - pokud vrací `200`, zdroj existuje
  - pokud vrací `404`, karta se nenačte

Pro integraci:

- Nastavení → Systém → Protokoly (Logs)
- hledejte záznamy `custom_components.cez_hdo`
