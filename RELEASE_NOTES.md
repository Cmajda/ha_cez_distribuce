# Release Notes – ČEZ HDO v2.0.9

## 🚀 Nová funkce: Automatická registrace Lovelace karty

Kompletně přepracovaný systém registrace frontend karty. Karta se nyní automaticky registruje do Lovelace resources bez nutnosti ruční konfigurace.

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
