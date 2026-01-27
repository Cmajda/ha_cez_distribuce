# Release Notes – ČEZ HDO v2.1.0

## 🚀 Nová funkce: Aktuální cena elektřiny

Přidán nový senzor **aktuální cena** (`sensor.cez_hdo_aktualni_cena`), který zobrazuje cenu elektřiny podle aktivního tarifu.

## ✨ Hlavní změny

### Nový senzor aktuální ceny

- **sensor.cez_hdo_aktualni_cena** – zobrazuje aktuální cenu v Kč/kWh
- Automaticky přepíná mezi cenou nízkého a vysokého tarifu podle aktivního HDO
- Atributy: `low_tariff_price`, `high_tariff_price`, `active_tariff`
- Ikona: 💵 (mdi:currency-usd)

### Nová služba `cez_hdo.set_prices`

- Nastaví ceny pro nízký a vysoký tarif
- Parametry:
  - `low_tariff_price` – cena za kWh v nízkém tarifu (NT)
  - `high_tariff_price` – cena za kWh ve vysokém tarifu (VT)

### Aktualizovaná Lovelace karta

- **Nové pole v editoru**: Cena NT a Cena VT
- **Zobrazení aktuální ceny**: Karta nyní zobrazuje aktuální cenu s barevným pozadím
- Nový přepínač "Zobrazit aktuální cenu" v editoru karty

## 📋 Použití

### Nastavení cen přes službu

```yaml
service: cez_hdo.set_prices
data:
  low_tariff_price: 2.50
  high_tariff_price: 4.50
```

### Konfigurace karty

V editoru karty zadejte:
- **Cena NT (Kč/kWh)**: např. 2.50
- **Cena VT (Kč/kWh)**: např. 4.50
- Zaškrtněte **Zobrazit aktuální cenu**

## 🔧 Dotčené soubory

- `custom_components/cez_hdo/sensor.py` – nový CurrentPrice senzor
- `custom_components/cez_hdo/base_entity.py` – metadata pro CurrentPrice
- `custom_components/cez_hdo/__init__.py` – služba set_prices
- `custom_components/cez_hdo/services.yaml` – definice služby
- `custom_components/cez_hdo/frontend/dist/cez-hdo-card.js` – aktualizovaná karta

---

# Release Notes – ČEZ HDO v2.0.9

## 🚀 Nová funkce: Automatická registrace Lovelace karty

Kompletně přepracovaný systém registrace frontend karty. Karta se nyní automaticky registruje do Lovelace resources bez nutnosti ruční konfigurace. Ve zdrojích se zobrazí jako ***/cez_hdo_card/cez-hdo-card.js?v=x.x.x*** kde x.x.x je verze doplnku

## ✨ Hlavní změny

### Nový registrační systém frontend karty

- **Automatická registrace** – karta se zaregistruje automaticky při startu Home Assistant
- **Storage mód** – plná podpora Lovelace v režimu storage (UI mód)
- **Verzování** – automatická aktualizace verze karty při upgrade integrace
- **Čistá odregistrace** – při odebrání integrace se karta automaticky odstraní z resources

### Backend / integrace

- Nová třída `CezHdoCardRegistration` pro správu registrace karty
- Registrace statické cesty pomocí `StaticPathConfig` (modernější API)
- Přidána závislost na `lovelace` v `after_dependencies`
- Přidána závislost `packaging` pro správné parsování verze Home Assistant

### Dotčené soubory

- `custom_components/cez_hdo/__init__.py` – přepracovaná inicializace
- `custom_components/cez_hdo/frontend/__init__.py` – **nový soubor** s registrační třídou
- `custom_components/cez_hdo/manifest.json` – aktualizované závislosti

## 📋 Poznámky k upgradu

1. Po aktualizaci restartujte Home Assistant
2. Karta se automaticky zaregistruje do Lovelace resources
3. Po restartu může být potřeba `Ctrl+F5` pro vyčištění cache prohlížeče

## 🔧 Technické detaily

Karta je dostupná na URL: `/cez_hdo_card/cez-hdo-card.js`

Lovelace resource je automaticky přidán ve formátu:

```yaml
/cez_hdo_card/cez-hdo-card.js?v=1.0.0
```
