# ⚡️ ČEZ HDO – Uživatelská dokumentace

Kompletní návod pro instalaci, konfiguraci a používání integrace ČEZ HDO v Home Assistantu.

---

## 📑 Obsah

- [🚀 Instalace](#-instalace)
- [⚙️ Konfigurace integrace](#️-konfigurace-integrace)
- [📦 Vytvářené entity](#-vytvářené-entity)
- [🎴 Lovelace karta](#-lovelace-karta)
- [💰 Nastavení cen](#-nastavení-cen)
- [📊 Energy Dashboard](#-energy-dashboard)
- [📅 HDO rozvrh](#-hdo-rozvrh)
- [🔧 Řešení problémů](#-řešení-problémů)
- [📊 Diagnostika](#-diagnostika)

---

## 🚀 Instalace

### Instalace přes HACS (doporučeno)

1. Otevřete **HACS → Integrations**
2. Klikněte na **⋮** → **Custom repositories**
3. Přidejte repozitář:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

4. Nainstalujte integraci **ČEZ HDO**
5. **Restartujte Home Assistant**

### Po instalaci

Po restartu pokračujte konfigurací integrace (viz další sekce).

> **Poznámka:** Po instalaci/aktualizaci může být potřeba stisknout `Ctrl+F5` pro vyčištění cache prohlížeče.

---

## ⚙️ Konfigurace integrace

Od verze 3.0.0 se integrace konfiguruje přes GUI (ne přes YAML).

### Přidání integrace

1. **Settings → Devices & Services**
2. Klikněte **+ Add Integration**
3. Vyhledejte **ČEZ HDO**

### Krok 1: EAN

Zadejte vaše **EAN číslo** (18 číslic).

EAN najdete:
- Na faktuře / vyúčtování za elektřinu
- V portálu vašeho dodavatele elektřiny
- Na stránkách [ČEZ Distribuce](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo)

![EAN na faktuře](../ean_example.png)

### Krok 2: Signál

Vyberte **signál** ze seznamu dostupných signálů pro vaše odběrné místo.

- Pokud je k dispozici pouze jeden signál, bude vybrán automaticky
- Signál určuje, kdy se přepíná mezi NT a VT

### Krok 3: Ceny

Zadejte ceny elektřiny:
- **Cena NT (Kč/kWh)** – cena za kWh v nízkém tarifu
- **Cena VT (Kč/kWh)** – cena za kWh ve vysokém tarifu

Ceny najdete na faktuře od dodavatele elektřiny.

### Dokončení

Klikněte **Finish**. Integrace vytvoří:
- Zařízení "ČEZ HDO XXXXXX" (posledních 6 číslic EAN)
- Všechny senzory a binární senzory

---

## 📦 Vytvářené entity

Integrace vytváří následující entity:

### Binary sensors

| Entita | Popis |
| ------ | ----- |
| `binary_sensor.cez_hdo_*_nizky_tarif_aktivni` | Nízký tarif je aktivní (`on/off`) |
| `binary_sensor.cez_hdo_*_vysoky_tarif_aktivni` | Vysoký tarif je aktivní (`on/off`) |

### Sensors

| Entita | Popis |
| ------ | ----- |
| `sensor.cez_hdo_*_nizky_tarif_zacatek` | Čas začátku NT (např. `01:10`) |
| `sensor.cez_hdo_*_nizky_tarif_konec` | Čas konce NT (např. `08:30`) |
| `sensor.cez_hdo_*_nizky_tarif_zbyva` | Zbývající čas do změny tarifu |
| `sensor.cez_hdo_*_vysoky_tarif_zacatek` | Čas začátku VT |
| `sensor.cez_hdo_*_vysoky_tarif_konec` | Čas konce VT |
| `sensor.cez_hdo_*_vysoky_tarif_zbyva` | Zbývající čas do změny tarifu |
| `sensor.cez_hdo_*_aktualni_cena` | Aktuální cena v Kč/kWh |
| `sensor.cez_hdo_*_rozvrh` | 7denní HDO rozvrh |
| `sensor.cez_hdo_*_surova_data` | Timestamp poslední aktualizace |

> **Poznámka:** `*` označuje suffix odvozený z EAN pro rozlišení více instancí.

---

## 🎴 Lovelace karta

### Přidání karty

1. Otevřete dashboard v edit módu
2. Přidejte kartu → vyhledejte **ČEZ HDO Card**
3. Nebo v YAML:

```yaml
type: custom:cez-hdo-card
```

### Ukázka karty

![ČEZ HDO karta](../entity_card.png)

### Nastavení karty

Karta má vizuální editor s těmito možnostmi:

| Přepínač | Popis | Výchozí |
| -------- | ----- | ------- |
| Zobrazit titulek | Nadpis karty | ✅ Zapnuto |
| Zobrazit stavy tarifů | Boxy NT/VT se stavem | ✅ Zapnuto |
| Zobrazit ceny u tarifů | Cena v boxu NT/VT | ❌ Vypnuto |
| Zobrazit časy | Začátek/konec tarifů | ✅ Zapnuto |
| Zobrazit zbývající čas | Čas do změny tarifu | ✅ Zapnuto |
| Zobrazit aktuální cenu | Velký box s cenou | ✅ Zapnuto |
| Zobrazit HDO rozvrh | 7denní vizualizace | ❌ Vypnuto |
| Zobrazit ceny v legendě | Ceny u NT/VT v legendě | ❌ Vypnuto |
| Kompaktní režim | Zmenšená velikost | ❌ Vypnuto |

### Výběr entit

Karta automaticky detekuje entity ČEZ HDO. Pokud máte více instancí integrace, vyberte správné entity v editoru.

---

## 💰 Nastavení cen

Ceny se nastavují **v integraci**, ne v kartě.

### Změna cen

1. **Settings → Devices & Services → ČEZ HDO**
2. Klikněte na **Configure**
3. Projděte kroky až ke **Krok 3: Ceny**
4. Změňte ceny a uložte

### Služba set_prices

Ceny lze nastavit i přes službu:

```yaml
service: cez_hdo.set_prices
data:
  low_tariff_price: 2.50
  high_tariff_price: 4.50
```

---

## 📊 Energy Dashboard

Senzor `sensor.cez_hdo_*_aktualni_cena` lze použít v Energy Dashboard:

1. **Settings → Dashboards → Energy**
2. V sekci "Electricity grid" klikněte na **Add consumption**
3. Vyberte měřič spotřeby
4. V poli "Use an entity with current price" vyberte `sensor.cez_hdo_*_aktualni_cena`

![Energy Dashboard](../integration_energy_ha.png)

---

## 📅 HDO rozvrh

Karta obsahuje vizualizaci 7denního HDO rozvrhu:

![HDO rozvrh](../graph.png)

### Aktivace

1. Otevřete editor karty
2. Zapněte **Zobrazit HDO rozvrh**
3. Volitelně zapněte **Zobrazit ceny v legendě rozvrhu**

### Popis

- **Zelené bloky** – nízký tarif (NT)
- **Oranžové bloky** – vysoký tarif (VT)
- **Časová osa** – 0:00 až 24:00
- **Tooltip** – přesné časy při najetí myší

---

## 🔧 Řešení problémů

### Karta se nezobrazuje

1. Stiskněte `Ctrl+F5` pro vyčištění cache
2. Zkontrolujte, že URL `http://IP_HA:8123/cez_hdo/cez-hdo-card.js` vrací 200

### Entity nejsou k dispozici

1. Zkontrolujte **Settings → Devices & Services → ČEZ HDO**
2. Ověřte, že integrace nemá chybu (červená ikona)
3. Klikněte na **Reload** u integrace

### Chyba "Neplatný EAN" nebo "Nepodařilo se načíst signály"

- Ověřte, že EAN je správný (18 číslic)
- Zkontrolujte [portál ČEZ Distribuce](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo) ručně
- API ČEZ může být dočasně nedostupné

### Kompletní reset

1. **Settings → Devices & Services → ČEZ HDO → Delete**
2. Smažte složku `custom_components/cez_hdo/data/`
3. Restart Home Assistant
4. Přidejte integraci znovu

---

## 📊 Diagnostika

Pro nahlášení chyby na GitHubu exportujte diagnostická data:

### Export diagnostiky

1. **Settings → Devices & Services → ČEZ HDO**
2. Klikněte na zařízení
3. Klikněte na **⋮** (tři tečky) vpravo nahoře
4. Vyberte **Download diagnostics**
5. Uložte JSON soubor

### Co diagnostika obsahuje

- Stav všech senzorů (hodnoty, atributy)
- Obsah cache (HDO rozvrh)
- Nastavení integrace (signál, ceny)
- **Citlivé údaje jsou maskovány** (EAN, partner, vkont, vstelle, anlage)

### Přiložení k issue

1. Otevřete [GitHub Issues](https://github.com/Cmajda/ha_cez_distribuce/issues)
2. Vytvořte nový issue
3. Přiložte diagnostický JSON soubor
4. Popište problém

---

## 📚 Další dokumentace

- [Upgrade Guide](upgrade-guide.md) – postup upgradu z v2.x na v3.0.0
- [Developer Guide](developer-guide.md) – pro vývojáře
- [Service Guide](service-guide.md) – popis dostupných služeb
