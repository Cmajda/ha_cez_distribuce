# ČEZ HDO - Senzor pro Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

## 📑 Obsah

- [📋 O doplňku](#-o-doplňku)
- [🚀 Instalace](#-instalace)
- [⚙️ Konfigurace](#️-konfigurace)
- [🎨 Frontend karta](#-frontend-karta)
- [🖼️ Ukázka karty](#️-ukázka-karty)
- [👥 Pro vývojáře](#-pro-vývojáře)

## 📋 O doplňku

Tento doplněk pro Home Assistant stahuje data o HDO (hromadné dálkové ovládání) z [ČEZ Distribuce](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html) a poskytuje:

- ✅ **Aktuální stav HDO** - zobrazuje zda je aktivní nízký nebo vysoký tarif
- ✅ **Časy začátku a konce** nízkého/vysokého tarifu
- ✅ **Zbývající čas** aktivního tarifu
- ✅ **Podpora státních svátků** - automaticky aplikuje víkendový tarif
- ✅ **Custom Lovelace karta** pro přehledné zobrazení

## 🚀 Instalace

Klikněte na tlačítko níže pro automatické otevření HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

> 📖 **Podrobné instrukce instalace** včetně manuální instalace najdete v [uživatelské dokumentaci](docs/user-guide.md).

## ⚙️ Konfigurace

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

**Zjištění vašeho kódu a regionu:**

Informace najdete ve smlouvě s ČEZ nebo na [webových stránkách ČEZ Distribuce](https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html).

Pro ověření správnosti použijte URL ve tvaru:
```
https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/REGION?code=KÓD
```

> 📖 **Kompletní seznam kódů** pro všechny regiony najdete v [uživatelské dokumentaci](docs/user-guide.md#podporované-distribuční-kódy).

## 🎨 Frontend karta

### Automatická instalace

Karta se automaticky nainstaluje při prvním spuštění integrace po restartu Home Assistant.

### Ruční přidání (pokud automatická nefunguje)

1. **Přidejte zdroj do Lovelace:**
   - Nastavení → Dashboardy → Zdroje
   - URL: `/local/cez-hdo-card.js`
   - Typ: JavaScript Module

2. **Restartujte Home Assistant**

> 📖 **Podrobná konfigurace karty** včetně YAML nastavení je v [uživatelské dokumentaci](docs/user-guide.md#lovelace-karta).

## 🖼️ Ukázka karty

![ČEZ HDO Card](entity_card.png)

Karta zobrazuje:
- 🟢/🔴 Aktuální stav HDO (nízký/vysoký tarif)
- ⏰ Časy začátku a konce tarifů
- ⏳ Zbývající čas do změny tarifu
- 📅 Rozlišení pracovních dnů a víkendů

## 👥 Pro vývojáře

Chcete přispět k vývoji nebo si nastavit development prostředí?

📚 **Přečtěte si [vývojářskou dokumentaci](docs/developer-guide.md)** která obsahuje:

- 🏗️ Strukturu projektu a development workflow
- 🔧 Build a deployment skripty
- 🎨 Frontend a backend development
- ✅ Testování a release proces
- 🤖 Instrukce pro práci s GitHub Copilot

---

**Licence:** MIT | **Podpora:** [GitHub Issues](https://github.com/Cmajda/ha_cez_distribuce/issues)