# Release Notes – ČEZ HDO v2.1.0

## 🚀 Nové funkce

### Senzor aktuální ceny elektřiny

Přidán nový senzor **aktuální cena** (`sensor.cez_hdo_aktualni_cena`), který zobrazuje cenu elektřiny podle aktivního tarifu.

- **sensor.cez_hdo_aktualni_cena** – zobrazuje aktuální cenu v Kč/kWh
- Automaticky přepíná mezi cenou NT a VT podle aktivního HDO tarifu
- Atributy: `low_tariff_price`, `high_tariff_price`, `active_tariff`
- Ikona: 💵 (mdi:currency-usd)
- **Perzistentní ceny** – ceny přežijí restart Home Assistantu

### Služba `cez_hdo.set_prices`

Nová služba pro nastavení cen tarifů:

```yaml
service: cez_hdo.set_prices
data:
  low_tariff_price: 2.50
  high_tariff_price: 4.50
```

## ✨ Vylepšená Lovelace karta

### Nové přepínače v editoru

- **Zobrazit aktuální cenu** – zobrazí sekci s aktuální cenou
- **Zobrazit ceny u tarifů** – zobrazí cenu přímo v boxu tarifu (NT/VT)

### Cenová pole

- Pole pro zadání ceny NT a VT v editoru karty
- Plynulé psaní bez překreslování
- Automatická synchronizace se senzorem při opuštění pole

### Zobrazení cen

- **Aktuální cena** – velký box s aktuální cenou a barevným pozadím
- **Ceny u tarifů** – malý text pod stavem tarifu (volitelné)

## 🔧 Technické změny

### Perzistentní úložiště cen

- Ceny se ukládají do `/config/www/cez_hdo/cez_hdo_prices.json`
- Automatické načtení při startu Home Assistantu
- Automatické uložení při změně cen

### Dotčené soubory

- `custom_components/cez_hdo/__init__.py` – perzistence cen, služba set_prices
- `custom_components/cez_hdo/sensor.py` – nový CurrentPrice senzor
- `custom_components/cez_hdo/base_entity.py` – metadata pro CurrentPrice
- `custom_components/cez_hdo/services.yaml` – definice služby
- `custom_components/cez_hdo/frontend/dist/cez-hdo-card.js` – vylepšená karta

## 📋 Poznámky k upgradu

1. Po aktualizaci restartujte Home Assistant
2. Nastavte ceny v editoru karty nebo přes službu `cez_hdo.set_prices`
3. Ceny zůstanou zachovány i po restartu

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
