# ČEZ HDO – Upgrade Guide

Tento dokument popisuje postup pro upgrade integrace na novou verzi.

---

## ⚠️ Upgrade na v3.x (z v2.x) – DŮLEŽITÉ ZMĚNY

Verze 3.x přináší **zásadní změny** v architektuře integrace.
Přečtěte si pozorně celý postup.

### Změny oproti v2.x

| Funkce | v2.x | v3.x |
|--------|------|--------|
| **Konfigurace** | YAML (`configuration.yaml`) | GUI (Settings → Integrations) |
| **Správa entit** | Jednotlivé entity | Device Registry (seskupeno pod zařízení) |
| **Úložiště dat** | `www/cez_hdo/` | Home Assistant `.storage` |
| **Nastavení cen** | Editor karty | Options Flow integrace |
| **Cache** | Sdílený soubor | Soubory pro každé EAN v `.storage` |
| **Diagnostika** | Manuální logy | Export přes UI |
| **Více EAN** | Komplikované | Plně podporováno |
| **Více signálů/EAN** | Nepodporováno | Plně podporováno |
| **Entity ID** | Automatické | Uživatelsky konfigurovatelná přípona |

### Postup upgradu

#### Krok 1: Záloha (doporučeno)

Před upgradem vytvořte zálohu Home Assistantu (Settings → System → Backups).

#### Krok 2: Smazat YAML konfiguraci

V `configuration.yaml` **smažte** všechny bloky ČEZ HDO:

```yaml
# SMAZAT tyto bloky:
sensor:
  - platform: cez_hdo
    ean: "Váš EAN"

binary_sensor:
  - platform: cez_hdo
    ean: "Váš EAN"
```

#### Krok 3: Aktualizovat integraci

- **HACS:** Otevřete HACS → ČEZ HDO → Aktualizovat na nejnovější verzi 3.x
- **Manuálně:** Stáhněte a přepište `custom_components/cez_hdo/`

#### Krok 4: Restartovat Home Assistant

Po aktualizaci proveďte **plný restart** Home Assistantu (ne jen reload).

#### Krok 5: Smazat staré entity

1. **Settings → Devices & Services → Entities**
2. Do vyhledávání napište `cez_hdo`
3. Vyberte všechny staré entity (budou bez přiřazeného zařízení)
4. Klikněte **Remove selected**

#### Krok 6: Přidat integraci přes GUI

1. **Settings → Devices & Services**
2. Klikněte **+ Add Integration**
3. Vyhledejte **ČEZ HDO**
4. Projděte aktuální kroky konfigurace: EAN, CAPTCHA, signál, přípona a ceny.
5. V nastavení cen můžete ponechat pevné ceny nebo volitelně vybrat cenové entity.
6. Dokončete konfiguraci podle [uživatelského návodu](user-guide.md).

#### Krok 7: Odstranit případnou starou složku

Pokud zůstala po verzi 2.x, smažte starou složku `www/cez_hdo/`; aktuální verze ji nepoužívá:

```bash
# Přes SSH nebo File Editor addon
rm -rf /config/www/cez_hdo
```

Aktuální verze ukládá cache do Home Assistantem spravované složky `.storage`.

#### Krok 8: Aktualizovat kartu

1. Otevřete Lovelace dashboard
2. Stiskněte `Ctrl+F5` pro vyčištění cache
3. Upravte kartu `custom:cez-hdo-card`
4. **Ceny se nyní nastavují v integraci**, ne v kartě

### ✅ Ověření upgradu

Po upgradu byste měli vidět:

1. **Settings → Devices & Services → ČEZ HDO**
   - Zařízení „ČEZ HDO ({signál})“
   - Všechny entity seskupené pod tímto zařízením

2. **Entity s novými názvy:**
   - `sensor.cez_hdo_lowtariffstart_{pripona}`
   - `binary_sensor.cez_hdo_lowtariffactive_{pripona}`
   - atd. (kde `{pripona}` je vaše zvolená přípona)

3. **Diagnostika dostupná:**
   - Settings → Devices → ČEZ HDO → ⋮ → Download diagnostics

---

## 🔄 Změna nastavení po instalaci

### Změna EAN, signálu nebo cen

1. **Settings → Devices & Services → ČEZ HDO**
2. Klikněte na **Configure**
3. Projděte kroky EAN → CAPTCHA → Signál → Přípona → Ceny
4. Uložte změny

### Více EAN (více odběrných míst)

Pro každé EAN přidejte integraci znovu:

1. Settings → Devices & Services → + Add Integration → ČEZ HDO
2. Zadejte další EAN

Každé EAN bude mít:

- Vlastní zařízení v Device Registry
- Vlastní entity (s unikátní příponou)
- Vlastní cache soubory

### Stejné EAN s různými signály

Pokud máte jedno EAN s více signály (např. pro různé okruhy):

1. Přidejte integraci pro každý signál zvlášť
2. Každá instance bude mít jinou příponu

---

## 🔧 Když něco nefunguje

### Karta se nezobrazuje

1. Stiskněte `Ctrl+F5`
2. Zkontrolujte, že URL `/cez_hdo_card/cez-hdo-card.js?v=3.3.1` vrací 200

### Entity nejsou k dispozici

1. Zkontrolujte Settings → Devices & Services → ČEZ HDO
2. Ověřte, že integrace nemá chybu
3. Klikněte na "Reload" u integrace

### Kompletní reset

Pokud nic nepomáhá:

1. Settings → Devices & Services → ČEZ HDO → Delete
2. Soubory cache, cen a stavu obnovování jsou v Home Assistantem spravované složce `.storage`; běžně je není nutné mazat ručně.
3. Restart Home Assistant
4. Přidejte integraci znovu

---

## 📊 Export diagnostických dat

Pro nahlášení chyby:

1. **Settings → Devices & Services → ČEZ HDO**
2. Klikněte na zařízení
3. Klikněte na **⋮** (tři tečky) → **Download diagnostics**
4. Přiložte JSON soubor k issue na GitHubu

Diagnostika obsahuje:

- Stav senzorů (hodnoty, atributy)
- Obsah cache (rozvrh, ceny)
- Nastavení integrace
- **Bez citlivých dat** (EAN je maskován)
