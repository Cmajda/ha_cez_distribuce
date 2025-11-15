# ČEZ HDO - Senzor pro Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)

## 📑 Obsah

- [📑 Obsah](#-obsah)
- [📋 O doplňku](#-o-doplňku)
- [🚀 Instalace](#-instalace)
- [⚙️ Konfigurace](#️-konfigurace)
- [🎨 Frontend karta](#-frontend-karta)
  - [✨ Automatická instalace](#-automatická-instalace)
  - [📋 Použití karty](#-použití-karty)
  - [🔧 Ruční registrace (pouze pokud automatická selže)](#-ruční-registrace-pouze-pokud-automatická-selže)
- [🖼️ Ukázka karty](#️-ukázka-karty)
- [📚 Dokumentace](#-dokumentace)
- [👥 Pro vývojáře](#-pro-vývojáře)

## 📋 O doplňku

Tento doplněk pro Home Assistant stahuje data o HDO (hromadné dálkové ovládání) z nového API [ČEZ Distribuce](https://dip.cezdistribuce.cz/) a poskytuje:

- ✅ **EAN-based konfigurace** - používá EAN číslo odběrného místa místo starých kódů
- ✅ **Aktuální stav HDO** - zobrazuje zda je aktivní nízký nebo vysoký tarif
- ✅ **Automatický výběr signálu** - nebo možnost specifikace konkrétního signálu
- ✅ **Časy začátku a konce** nízkého/vysokého tarifu
- ✅ **Zbývající čas** aktivního tarifu
- ✅ **Service pro zjištění signálů** - `cez_hdo.list_signals`
- ✅ **Custom Lovelace karta** s automatickou instalací a registrací
- ✅ **Plug & play** - žádná manuální konfigurace frontend karty není potřeba

## 🚀 Instalace

Klikněte na tlačítko níže pro automatické otevření HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

> 📖 **Podrobné instrukce instalace** včetně manuální instalace najdete v [uživatelské dokumentaci](docs/user-guide.md).

> ⚙️ **Pokročilá konfigurace** a seznam všech možností je v [uživatelské dokumentaci](docs/user-guide.md).

> 🛠️ **Průvodce services** včetně `list_signals` najdete v [service dokumentaci](docs/service-guide.md).

## ⚙️ Konfigurace

Přidejte do `configuration.yaml`:

```yaml
# ČEZ HDO integrace - nové EAN API
sensor:
  - platform: cez_hdo
    ean: "VAŠE_EAN_ČÍSLO"  # EAN odběrného místa z faktury
    signal: "a3b4dp01"     # Volitelný - konkrétní signál (zjistíte přes service)
    scan_interval: 300      # Aktualizace každých 5 minut (volitelné)

binary_sensor:
  - platform: cez_hdo
    ean: "VAŠE_EAN_ČÍSLO"  # Stejné EAN jako u sensoru
    signal: "a3b4dp01"     # Volitelný - stejný signál jako u sensoru
```

**Zjištění dostupných signálů:**

Použijte service k zjištění dostupných HDO signálů:
```yaml
# V Developer Tools → Services
action: cez_hdo.list_signals
data:
  ean: "VAŠE_EAN_ČÍSLO"
```

**EAN číslo najdete:**
- Na vaší faktuře za elektřinu
- V zákaznickém portálu ČEZ
- Má formát dlouhého číselného kódu (např. "859182400609846929")

## 🎨 Frontend karta

### ✨ Automatická instalace

🎯 **Karta se instaluje a registruje úplně automaticky!**

Po instalaci integrace a restartu Home Assistant se karta:
- ✅ **Automaticky zkopíruje** do `/config/www/cez_hdo/`
- ✅ **Automaticky zaregistruje** v systému bez manuální konfigurace
- ✅ **Ihned k použití** - žádné další kroky nejsou potřeba

### 📋 Použití karty

Jednoduše přidejte do vašeho Lovelace dashboardu:

```yaml
type: custom:cez-hdo-card
# Automaticky použije výchozí entity pokud nejsou specifikovány
```

### 🔧 Ruční registrace (pouze pokud automatická selže)

Pokud by se karta z nějakého důvodu nezaregistrovala automaticky:

1. **Přidejte zdroj do Lovelace:**
   - Nastavení → Dashboardy → Zdroje
   - URL: `/local/cez_hdo/cez-hdo-card.js`
   - Typ: JavaScript Module

2. **Restartujte Home Assistant**

> 💡 **Tip:** Karta automaticky najde správné entity pokud nejsou zadány explicitně a instaluje se zcela automaticky bez potřeby manuální konfigurace.

> 📖 **Podrobná konfigurace karty** včetně YAML nastavení je v [uživatelské dokumentaci](docs/user-guide.md#lovelace-karta).

## 🖼️ Ukázka karty

![ČEZ HDO Card](entity_card.png)

Karta zobrazuje:
- 🟢/🔴 Aktuální stav HDO (nízký/vysoký tarif)
- ⏰ Časy začátku a konce tarifů
- ⏳ Zbývající čas do změny tarifu
- 📅 Rozlišení pracovních dnů a víkendů

## 📚 Dokumentace

- 📖 **[Uživatelská dokumentace](docs/user-guide.md)** - kompletní návod k instalaci a konfiguraci
- 🛠️ **[Průvodce services](docs/service-guide.md)** - jak použít `list_signals` service a signal selection
- 🔄 **[Upgrade Guide](docs/upgrade-guide.md)** - migrace ze staré verze (code/region → EAN)
- 🏗️ **[Vývojářská dokumentace](docs/developer-guide.md)** - pro vývojáře a přispěvatele

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
