# Release notes – ČEZ HDO (Home Assistant + Lovelace karta)

## Hlavní změny

- Opraveno spolehlivé načítání Lovelace karty po čisté instalaci i po hard refresh (řešení 404 na `/local/...` a „Custom element doesn’t exist“) – karta je primárně servírovaná z integrace a zároveň existuje fallback kopie do `www`.
- Zlepšena kompatibilita napříč verzemi Home Assistant (registrace statické cesty bez spoléhání na neexistující `register_static_path`).
- Opraven pád editoru karty způsobený `ha-entity-picker` (`Cannot read properties of undefined (reading 'localize')`) – editor je nově stabilní bez této závislosti.
- Přidán „zero-config“ režim: když uživatel nevyplní entity v konfiguraci karty, použijí se výchozí entity.
- Výchozí entity jsou nastavené na reálné české `entity_id` (např. `sensor.cez_hdo_nizky_tarif_*`); anglická kompatibilita defaultů byla odstraněna.

## Backend / integrace

- Stabilní servírování frontend bundle pro kartu z integrace + fallback kopie do `www` pro `/local/...`.
- Cache/úložiště: vytvoření parent adresáře před zápisem cache, aby čisté instalace nepadaly.

Dotčené soubory:

- `custom_components/cez_hdo/__init__.py`
- `custom_components/cez_hdo/base_entity.py`

## Frontend / karta

- Editor karty přepracován: místo `ha-entity-picker` používá stabilní `input + datalist` (našeptávání z `hass.states`) + volitelný upgrade přes `ha-selector`, když je dostupný.
- `getStubConfig()` vrací předvyplněné výchozí entity pro rychlé přidání karty.
- Zachováno inteligentní dohledání variant `entity_id` se suffixy `_2`, `_3` (např. po úpravách v Entity Registry).

Dotčené soubory:

- `custom_components/cez_hdo/frontend/dist/cez-hdo-card.js`
- `www/cez_hdo/cez-hdo-card.js`

## Dokumentace

- Kompletní přepsání uživatelské dokumentace + troubleshooting (včetně doporučeného postupu `Ctrl+F5`, reinstalace, smazání `www/cez_hdo`, restart HA).
- Doplněno, že jde o HACS (Custom repository) + odkaz na instalaci HACS.
- Přidány obrázky karty a editoru do README.
- Vývojářská dokumentace rozšířena o požadavky (Samba share), env proměnné a příklady deploy.

Dotčené soubory:

- `README.md`
- `docs/user-guide.md`
- `docs/service-guide.md`
- `docs/upgrade-guide.md`
- `docs/developer-guide.md`

## Poznámky k upgradu

- Po instalaci/aktualizaci karty může být jednorázově potřeba `Ctrl+F5` kvůli cache/service workeru – je popsané v dokumentaci.
- Pokud uživatel nic nevyplní v konfiguraci karty, použijí se výchozí české entity (pokud existují v systému).
