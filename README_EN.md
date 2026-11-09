# ČEZ HDO for Home Assistant

[Čeština](README.md) · [Full documentation on the Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki/English-Home)

[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![Stable release](https://img.shields.io/github/v/release/Cmajda/ha_cez_distribuce?label=stable)](https://github.com/Cmajda/ha_cez_distribuce/releases/latest)
[![Pre-release](https://img.shields.io/github/v/release/Cmajda/ha_cez_distribuce?include_prereleases&label=pre-release)](https://github.com/Cmajda/ha_cez_distribuce/releases)
[![Validate](https://github.com/Cmajda/ha_cez_distribuce/actions/workflows/hacs.yaml/badge.svg?branch=main)](https://github.com/Cmajda/ha_cez_distribuce/actions/workflows/hacs.yaml)
[![License](https://img.shields.io/badge/License-Apache%202.0%20%2B%20Commons%20Clause-blue)](./LICENSE)

> **Unofficial community integration.** This is not a ČEZ Distribuce product.

The integration brings ČEZ Distribuce HDO schedules into Home Assistant with
tariff sensors and a Lovelace card.

## Contributors

Thanks to everyone who contributes to the integration:

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

## Installation

1. In HACS, open **Integrations → Custom repositories** and add
   `Cmajda/ha_cez_distribuce` as an integration.
2. Install **ČEZ HDO** and restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration**, search for
   **ČEZ HDO**, and enter your EAN, CAPTCHA, signal, and tariff prices.

[![Open the ČEZ HDO repository in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

[Detailed installation and setup guide](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-EN)

## Add the card

1. Open a dashboard and select **Edit dashboard → Add card**.
2. Search for **ČEZ HDO Card**, configure it, and save.

![Add ČEZ HDO card](img/en/add_card_1.png)

The editor lets you choose entities, prices, displayed times, remaining time,
and compact mode. Enable the schedule and its price legend as needed.

![Configure ČEZ HDO card](img/en/add_card_2.png)

## Lovelace card

The card can show low/high tariff status, start and end times, remaining time,
the current price, and an optional seven-day HDO schedule. Data can also be
refreshed manually from the card.

![ČEZ HDO card](img/en/entity_card.png) ![HDO schedule](img/en/graph.png)

## Documentation and support

- [English Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki/English-Home)
- [Česká Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki)
- [Releases and pre-releases](https://github.com/Cmajda/ha_cez_distribuce/releases)
- [Report an issue](https://github.com/Cmajda/ha_cez_distribuce/issues)
- [License](LICENSE)
