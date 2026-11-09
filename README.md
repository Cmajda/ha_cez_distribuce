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

## Spolupracovníci

Děkuji všem, kteří se podílejí na vývoji integrace:

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

> **Neoficiální komunitní integrace.** Nejde o produkt společnosti ČEZ Distribuce.

Integrace načítá HDO rozvrhy ČEZ Distribuce do Home Assistantu a nabízí senzory
tarifů i Lovelace kartu.

## Rychlý start

1. V HACS otevřete **Integrations → Custom repositories** a přidejte
   `Cmajda/ha_cez_distribuce` jako integraci.
2. Nainstalujte **ČEZ HDO** a restartujte Home Assistant.
3. V **Nastavení → Zařízení a služby → Přidat integraci** vyhledejte
   **ČEZ HDO** a projděte nastavením EANu, CAPTCHA, signálu a cen.

[![Otevřít repozitář ČEZ HDO v HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

[Podrobný návod k instalaci a konfiguraci](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-CS)

## Přidání karty

1. Otevřete dashboard a zvolte **Upravit dashboard → Přidat kartu**.
2. Vyhledejte **ČEZ HDO Card**, nastavte kartu a uložte ji.

![Přidání karty ČEZ HDO](img/cs/add_card_1_cz.png)

Editor umožňuje zvolit zobrazené entity, ceny, časy, zbývající čas i kompaktní
režim. Rozvrh a ceny v jeho legendě lze zapnout podle potřeby.

![Nastavení karty ČEZ HDO](img/cs/add_card_2_cz.png)

## Lovelace karta

Karta zobrazuje stav nízkého a vysokého tarifu, začátky a konce tarifů,
zbývající čas, aktuální cenu a volitelný sedmidenní HDO rozvrh. Data lze obnovit
ručně přímo z karty.

![ČEZ HDO karta](img/cs/entity_card_cz.png) ![HDO rozvrh](img/cs/graph_cz.png)

## Dokumentace a podpora

- [Česká Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki)
- [Anglická Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki/English-Home)
- [Vydání a testovací verze](https://github.com/Cmajda/ha_cez_distribuce/releases)
- [Nahlásit problém](https://github.com/Cmajda/ha_cez_distribuce/issues)
- [Licence](LICENSE)
