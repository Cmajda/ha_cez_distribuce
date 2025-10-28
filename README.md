# ČEZ HDO - Senzor pro Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)  

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

Tento senzor stahuje data z webu https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html.  
Integrace vyžaduje **region** a **kód**. Tyto informace lze získat ze smlouvy s ČEZ CZ nebo z https://www.cezdistribuce.cz/cs/pro-zakazniky/spinani-hdo.html.  

Pro otestování zda je správně použit region a kod, lze otevřít odkaz v prohlížeči ve tvaru:

`https://www.cezdistribuce.cz/webpublic/distHdo/adam/containers/`REGION`?code=`kód  

Příklad:  
```
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
binary_sensor:
  - platform: cez_hdo
    region: stred  # váš region: zapad/sever/stred/vychod/morava
    code: 405      # váš HDO kód

sensor:
  - platform: cez_hdo
    region: stred
    code: 405
```

#### Podporované regiony

- západ
- sever  
- střed
- východ
- morava

### Krok 3: Přidání frontend resource

- Jděte do **Nastavení** → **Dashboards** → **Resources**
- Klikněte **"Add Resource"**
- URL: `/local/cez-hdo-card.js`
- Resource type: **JavaScript Module**
- Klikněte **"Create"**

### Krok 4: Restartování HA

Po přidání konfigurace restartujte Home Assistant.

## 🎨 Custom Lovelace Card

Integrace obsahuje vlastní Lovelace kartu pro lepší zobrazení HDO informací:

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

## 🔧 Řešení problémů

Pokud máte problémy s integrací:

1. **Zkontrolujte region a kód** - otestujte URL v prohlížeči
2. **Zkontrolujte logy** - Developer Tools → Logs
3. **Restartujte HA** po změnách konfigurace
4. **Vyčistěte cache** prohlížeče (Ctrl+F5) pro Lovelace kartu
