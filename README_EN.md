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

## ⚙️ What the integration does

For a configured metering point (EAN) and HDO signal, the integration fetches
the switching schedule for low and high tariffs. It provides:

- sensors for the active tariff, tariff start/end times, and time until change;
- the current price from a fixed value or a selected price sensor;
- a seven-day HDO schedule and data-validity sensors;
- entities that can be used in automations, for example to switch appliances
   based on the active tariff;
- automatic and manual HDO data refresh.

Add the current-price sensor to the Energy Dashboard for cost tracking; an
electricity consumption sensor is also required.

## 📚 Wiki

The Wiki is the main source of detailed documentation. It covers installation
and setup, entities, automation examples, prices and the Energy Dashboard,
troubleshooting, services, upgrades, and development.

[Open the English Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki/English-Home) ·
[Česká Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki)

## 🤝 Collaborators and Contributors

### 👥 Collaborators

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

### 🌱 Contributors

- [@jandado](https://github.com/jandado) – proposed limiting OCR retries on HTTP 429
   and honoring `retryAfter` in [PR #86](https://github.com/Cmajda/ha_cez_distribuce/pull/86).

## 🍺 Support Development

If you find the integration useful, you can support its continued development:

[![Buy me a beer](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20beer&emoji=%F0%9F%8D%BA&slug=cmajda&button_colour=FF813F&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00)](https://www.buymeacoffee.com/cmajda)

## 🚀 Installation

1. In HACS, open **Integrations → Custom repositories** and add
   `Cmajda/ha_cez_distribuce` as an integration.
2. Install **ČEZ HDO** and restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration**, search for
   **ČEZ HDO**, and enter your EAN, CAPTCHA, signal, and tariff prices.

[![Open the ČEZ HDO repository in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&owner=Cmajda&repository=ha_cez_distribuce)

[Detailed installation and setup guide](https://github.com/Cmajda/ha_cez_distribuce/wiki/User-Guide-EN)

## 🎴 Add the card

1. Open a dashboard and select **Edit dashboard → Add card**.
2. Search for **ČEZ HDO Card**, configure it, and save.

![Add ČEZ HDO card](img/en/add_card_1.png)

The editor lets you choose entities, prices, displayed times, remaining time,
and compact mode. Enable the schedule and its price legend as needed.

![Configure ČEZ HDO card](img/en/add_card_2.png)

## 🏠 Lovelace card

The card can show low/high tariff status, start and end times, remaining time,
the current price, and an optional seven-day HDO schedule. Data can also be
refreshed manually from the card.

![ČEZ HDO card](img/en/entity_card.png) ![HDO schedule](img/en/graph.png)

## 📚 Documentation and support

- [English Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki/English-Home)
- [Česká Wiki](https://github.com/Cmajda/ha_cez_distribuce/wiki)
- [Releases and pre-releases](https://github.com/Cmajda/ha_cez_distribuce/releases)
- [Report an issue](https://github.com/Cmajda/ha_cez_distribuce/issues)
- [License](LICENSE)
