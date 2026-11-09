# ⚡️ČEZ HDO pro Home Assistant ⚡️

[English](README_EN.md) · [Kompletní dokumentace ve Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![Release](https://img.shields.io/github/v/release/Cmajda/ha_cez_distribuce?label=stable&logo=github)](https://github.com/Cmajda/ha_cez_distribuce/releases/latest)
[![Pre-release](https://img.shields.io/github/v/release/Cmajda/ha_cez_distribuce?include_prereleases&label=pre-release&logo=github)](https://github.com/Cmajda/ha_cez_distribuce/releases)
[![Validate](https://github.com/Cmajda/ha_cez_distribuce/actions/workflows/hacs.yaml/badge.svg?branch=main)](https://github.com/Cmajda/ha_cez_distribuce/actions/workflows/hacs.yaml)
[![License](https://img.shields.io/badge/License-Apache%202.0%20%2B%20Commons%20Clause-blue)](./LICENSE)

[![Downloads](https://img.shields.io/github/downloads/Cmajda/ha_cez_distribuce/total)](https://github.com/Cmajda/ha_cez_distribuce/releases)
![Unique Views](https://raw.githubusercontent.com/Cmajda/ha_cez_distribuce/traffic/views_unique.svg)
![Unique Clones](https://raw.githubusercontent.com/Cmajda/ha_cez_distribuce/traffic/clones_unique.svg)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/Cmajda/ha_cez_distribuce)](https://github.com/Cmajda/ha_cez_distribuce/commits/main)

> **Neoficiální komunitní integrace.** Nejde o produkt společnosti ČEZ Distribuce.

Integrace načítá HDO rozvrhy ČEZ Distribuce do Home Assistantu a nabízí senzory
tarifů i Lovelace kartu.

## 📑 Obsah

- [⚙️ Co integrace dělá](#co-integrace-dela)
- [📚 Wiki](#-wiki)
- [🐛 Nahlášení chyby nebo vylepšení](#-nahlášení-chyby-nebo-vylepšení)
  - [🐛 Nahlásit chybu](#-nahlásit-chybu)
  - [💡 Navrhnout vylepšení](#-navrhnout-vylepšení)
  - [❓ Položit dotaz](#-položit-dotaz)
- [🤝 Spolupracovníci a přispěvatelé](#-spolupracovníci-a-přispěvatelé)
  - [👥 Spolupracovníci](#-spolupracovníci)
  - [🌱 Přispěvatelé](#-přispěvatelé)
- [🍺 Podpořit vývoj](#-podpořit-vývoj)
- [🚀 Rychlý start](#-rychlý-start)
- [🎴 Přidání karty](#-přidání-karty)
- [🏠 Lovelace karta](#-lovelace-karta)
- [📡 Vytvářené entity](#-vytvářené-entity)
- [📚 Dokumentace a podpora](#-dokumentace-a-podpora)

<a id="co-integrace-dela"></a>

## ⚙️ Co integrace dělá

Pro zadané odběrné místo (EAN) a HDO signál načítá časy spínání nízkého a
vysokého tarifu. V Home Assistantu poskytuje:

- senzory aktuálního tarifu, začátků a konců tarifů a času do další změny;
- aktuální cenu z pevného nastavení nebo vybraného cenového senzoru;
- sedmidenní HDO rozvrh a senzory platnosti načtených dat;
- entity použitelné v automatizacích, například pro spínání spotřebičů podle tarifu;
- automatické a ruční obnovení HDO dat.

Senzor aktuální ceny lze přidat do Energy Dashboard pro přehled nákladů;
pro výpočet je potřeba také senzor spotřeby elektřiny.

## 📚 Wiki

Wiki je hlavním zdrojem podrobné dokumentace. Obsahuje návody k instalaci a
nastavení, přehled entit, příklady automatizací, práci s cenami a Energy
Dashboardem, řešení problémů i vývojářské informace.

[Otevřít českou Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki) ·
[English Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki/English-Home)

[Příklady automatizací podle tarifu](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-CS#-automatizace-podle-tarifu)

## 🐛 Nahlášení chyby nebo vylepšení

### 🐛 Nahlásit chybu

[Vytvořit bug report](https://github.com/Cmajda/ha_cez_distribuce/issues/new?template=bug_report.yml) ·
[Postup včetně debug logů a diagnostiky](https://github.com/Cmajda/ha_cez_distribuce/wiki/Known-Issues-CS#jak-nahlásit-problém)

### 💡 Navrhnout vylepšení

[Vytvořit návrh vylepšení](https://github.com/Cmajda/ha_cez_distribuce/issues/new?template=feature_request.yml)

### ❓ Položit dotaz

[Vytvořit dotaz](https://github.com/Cmajda/ha_cez_distribuce/issues/new?template=question.yml) ·
[GitHub Discussions](https://github.com/Cmajda/ha_cez_distribuce/discussions)

## 🤝 Spolupracovníci a přispěvatelé

### 👥 Spolupracovníci

Děkuji všem, kteří se dlouhodobě podílejí na vývoji integrace:

<!-- readme: collaborators -start -->
<table>
   <tbody>
      <tr>
         <td align="center">
            <a href="https://github.com/pokornyIt">
               <img src="https://github.com/pokornyIt.png" width="96;" alt="pokornyIt"/>
               <br />
               <sub><b>pokornyIt</b></sub>
            </a>
         </td>
         <td align="center">
            <a href="https://github.com/VojtechJurcik">
               <img src="https://github.com/VojtechJurcik.png" width="96;" alt="VojtechJurcik"/>
               <br />
               <sub><b>VojtechJurcik</b></sub>
            </a>
         </td>
      </tr>
   </tbody>
</table>
<!-- readme: collaborators -end -->

### 🌱 Přispěvatelé

- [@jandado](https://github.com/jandado) – návrh omezení opakování OCR při HTTP 429
   a respektování `retryAfter` v [PR #86](https://github.com/Cmajda/ha_cez_distribuce/pull/86).

## 🍺 Podpořit vývoj

Pokud vám integrace pomáhá, můžete podpořit její další vývoj:

[![Buy me a beer](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20beer&emoji=%F0%9F%8D%BA&slug=cmajda&button_colour=FF813F&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/cmajda)

## 🚀 Rychlý start

1. V HACS otevřete **Integrations → Custom repositories** a přidejte
   `Cmajda/ha_cez_distribuce` jako integraci.
2. Nainstalujte **ČEZ HDO** a restartujte Home Assistant.
3. V **Nastavení → Zařízení a služby → Přidat integraci** vyhledejte
   **ČEZ HDO** a projděte nastavením EANu, CAPTCHA, signálu a cen.

[![Otevřít repozitář ČEZ HDO v HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

[Podrobný návod k instalaci a konfiguraci](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-CS)

## 🎴 Přidání karty

1. Otevřete dashboard a zvolte **Upravit dashboard → Přidat kartu**.
2. Vyhledejte **ČEZ HDO Card**, nastavte kartu a uložte ji.

[![Přidání karty ČEZ HDO](img/cs/add_card_1_cz.png)](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-CS#krok-2-p%C5%99id%C3%A1n%C3%AD-karty)

Editor umožňuje zvolit zobrazené entity, ceny, časy, zbývající čas i kompaktní
režim. Rozvrh a ceny v jeho legendě lze zapnout podle potřeby.

[![Nastavení karty ČEZ HDO](img/cs/add_card_2_cz.png)](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-CS#krok-3-nastaven%C3%AD-karty)

## 🏠 Lovelace karta

Karta zobrazuje stav nízkého a vysokého tarifu, začátky a konce tarifů,
zbývající čas, aktuální cenu a volitelný sedmidenní HDO rozvrh. Data lze obnovit
ručně přímo z karty.

[![ČEZ HDO karta](img/cs/entity_card_cz.png)](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-CS#v%C3%BDsledek) [![HDO rozvrh](img/cs/graph_cz.png)](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-CS#v%C3%BDsledek)

## 📡 Vytvářené entity

Každá instance vytváří entity pro své EAN a HDO signál. `*` označuje příponu
zvolenou při konfiguraci. Ikony odpovídají Material Design Icons použitým v kódu;
u platnosti dat se mění podle stavu.

| Ikona | Typ | Entita | Popis |
| --- | --- | --- | --- |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/power.svg" width="18" height="18" alt="mdi:power"> | Binary sensor | [`binary_sensor.cez_hdo_lowtariffactive_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#lowtariffactive) | Nízký tarif je aktivní |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/power.svg" width="18" height="18" alt="mdi:power"> | Binary sensor | [`binary_sensor.cez_hdo_hightariffactive_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#hightariffactive) | Vysoký tarif je aktivní |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/check-circle.svg" width="18" height="18" alt="mdi:check-circle"> / <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/alert-circle.svg" width="18" height="18" alt="mdi:alert-circle"> | Binary sensor | [`binary_sensor.cez_hdo_data_valid_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#datavalid) | Data jsou platná |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/home-clock.svg" width="18" height="18" alt="mdi:home-clock"> | Sensor | [`sensor.cez_hdo_lowtariffstart_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#lowtariffstart) | Začátek NT |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/home-clock-outline.svg" width="18" height="18" alt="mdi:home-clock-outline"> | Sensor | [`sensor.cez_hdo_lowtariffend_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#lowtariffend) | Konec NT |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/timer.svg" width="18" height="18" alt="mdi:timer"> | Sensor | [`sensor.cez_hdo_lowtariffduration_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#lowtariffduration) | Zbývající čas NT |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/home-clock.svg" width="18" height="18" alt="mdi:home-clock"> | Sensor | [`sensor.cez_hdo_hightariffstart_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#hightariffstart) | Začátek VT |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/home-clock-outline.svg" width="18" height="18" alt="mdi:home-clock-outline"> | Sensor | [`sensor.cez_hdo_hightariffend_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#hightariffend) | Konec VT |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/timer.svg" width="18" height="18" alt="mdi:timer"> | Sensor | [`sensor.cez_hdo_hightariffduration_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#hightariffduration) | Zbývající čas VT |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/currency-usd.svg" width="18" height="18" alt="mdi:currency-usd"> | Sensor | [`sensor.cez_hdo_currentprice_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#currentprice) | Aktuální cena (Kč/kWh) |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/chart-timeline-variant.svg" width="18" height="18" alt="mdi:chart-timeline-variant"> | Sensor | [`sensor.cez_hdo_schedule_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#schedule) | 7denní HDO rozvrh |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/home-clock.svg" width="18" height="18" alt="mdi:home-clock"> | Sensor | [`sensor.cez_hdo_raw_data_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#rawdata) | Čas poslední aktualizace a surová data |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/calendar-clock.svg" width="18" height="18" alt="mdi:calendar-clock"> | Sensor | [`sensor.cez_hdo_data_valid_until_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#datavaliduntil) | Platnost dat do |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/calendar-question.svg" width="18" height="18" alt="mdi:calendar-question"> | Sensor | [`sensor.cez_hdo_data_age_days_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#dataagedays) | Stáří dat ve dnech |
| <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/calendar-check.svg" width="18" height="18" alt="mdi:calendar-check"> / <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/calendar-alert.svg" width="18" height="18" alt="mdi:calendar-alert"> / <img src="https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/calendar-remove.svg" width="18" height="18" alt="mdi:calendar-remove"> | Sensor | [`sensor.cez_hdo_days_until_expiry_*`](https://github.com/Cmajda/ha_cez_distribuce/wiki/Entities-CS#daysuntilexpiry) | Dní do vypršení platnosti |

Například přípona `doma` vytvoří ID `sensor.cez_hdo_lowtariffstart_doma`.

## 📚 Dokumentace a podpora

- [Česká Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki)
- [Anglická Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki/English-Home)
- [Vydání a testovací verze](https://github.com/Cmajda/ha_cez_distribuce/releases)
- [Licence](LICENSE)
