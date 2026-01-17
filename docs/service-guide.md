# ČEZ HDO – Services

Tento dokument popisuje služby (Developer Tools → Services), které integrace nabízí.

## `cez_hdo.list_signals`

Vypíše dostupné HDO signály pro zadaný EAN do logů Home Assistant.

Použití:

```yaml
action: cez_hdo.list_signals
data:
  ean: "Váš EAN"
```

Kde to uvidíte:

- Nastavení → Systém → Protokoly (Logs)

## `cez_hdo.reload_frontend_card`

Znovu nasadí/obnoví frontend soubor karty (užitečné při vývoji nebo když se karta nenačítá).

Použití:

```yaml
action: cez_hdo.reload_frontend_card
data: {}
```

Poznámka: po použití služby může být v prohlížeči potřeba `Ctrl+F5`.
