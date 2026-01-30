# ČEZ HDO – Upgrade Guide

Tento dokument popisuje postup pro upgrade integrace na novou verzi.

---

## Upgrade na v3.0.0 (z v2.x)

Verze 3.0.0 přináší významné změny:

- **Config Flow** – konfigurace přes GUI místo YAML
- **Device Registry** – všechny entity seskupeny pod jedno zařízení
- **Nové úložiště dat** – přesunuto z `www/cez_hdo/` do `custom_components/cez_hdo/data/`
- **Diagnostika** – export debug informací

### Postup upgradu

#### 1. Smazat YAML konfiguraci

V `configuration.yaml` smažte bloky:

```yaml
# ČEZ HDO integrace
sensor:
  - platform: cez_hdo
    ean: "Váš EAN"

binary_sensor:
  - platform: cez_hdo
    ean: "Váš EAN"
```

#### 2. Aktualizovat integraci

- **HACS:** Aktualizovat na v3.0.0
- **Manuálně:** Stáhnout a přepsat `custom_components/cez_hdo/`

#### 3. Restartovat Home Assistant

#### 4. Smazat staré entity

1. **Settings → Devices & Services → Entities**
2. Filtrovat "cez_hdo"
3. Vybrat entity bez zařízení (staré YAML entity)
4. Kliknout **Remove selected**

#### 5. Přidat integraci přes GUI

1. **Settings → Devices & Services → Add Integration**
2. Vyhledat "ČEZ HDO"
3. Zadat EAN číslo
4. Vybrat signál (pokud je více možností)

#### 6. Smazat starou složku www/cez_hdo

Po úspěšném přidání integrace smažte starou složku `www/cez_hdo/`.

Data se nyní ukládají do `custom_components/cez_hdo/data/`.

#### 7. Nastavit ceny v kartě

Ceny je potřeba nastavit znovu v kartě.

---

## Když komponenta / karta nefunguje

Postupujte takto:

1. Vynutit refresh: `Ctrl+F5`
2. Odinstalovat doplněk
3. Pokud existuje složka `www/cez_hdo`, smažte ji
4. Pokud existuje složka `custom_components/cez_hdo/data`, smažte ji
5. Znovu nainstalovat doplněk
6. Restart Home Assistant
7. Přidat integraci přes GUI

---

## Pokud se po restartu karta nezobrazuje

Po aktualizaci může být potřeba jednou udělat `Ctrl+F5`, aby prohlížeč načetl nový JavaScript.
