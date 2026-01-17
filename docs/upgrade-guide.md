# ČEZ HDO – Upgrade a čistá reinstalace

Tento dokument je praktický postup pro upgrade nebo situaci, kdy po instalaci něco nefunguje (karta se nenačítá, nejsou entity, chyby v konzoli).

## Když komponenta / karta nefunguje

Postupujte takto:

1. Vynutit refresh: `Ctrl+F5`
1. Odinstalovat doplněk
1. Pokud existuje složka `www/cez_hdo`, smažte ji
1. Znovu nainstalovat doplněk
1. Restart Home Assistant

## Upgrade konfigurace (zjednodušeně)

Integrace používá EAN.

Zkontrolujte, že máte v `configuration.yaml` alespoň:

```yaml
sensor:
  - platform: cez_hdo
    ean: "Váš EAN"

binary_sensor:
  - platform: cez_hdo
    ean: "Váš EAN"
```

Pak restartujte Home Assistant.

## Pokud se po restartu karta nezobrazuje v seznamu karet

Po aktualizaci může být potřeba jednou udělat `Ctrl+F5`, aby prohlížeč načetl nový JavaScript.
