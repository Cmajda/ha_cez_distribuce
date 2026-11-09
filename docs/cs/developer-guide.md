# ČEZ HDO – Vývojářská dokumentace

Stručný přehled pro vývoj/přispívání.

## Požadavky

### Lokální Python vývoj

Projekt vyžaduje Python **3.14.2 až 3.15.0** a používá `uv` pro vytvoření
virtuálního prostředí `.venv` a instalaci nástrojů z `pyproject.toml`.

```bash
uv sync --group dev
uv run pre-commit install
uv run pre-commit run --all-files
```

VS Code používá `${workspaceFolder}/.venv/bin/python`; po `uv sync` se prostředí
vytvoří na této cestě. Před commitem ověřte, že `uv.lock` odpovídá projektu:

```bash
uv lock --check
```

### Home Assistant

Pro vývojový deploy přes [dev/deploy.sh](../dev/deploy.sh) je nejjednodušší
mít v HA dostupný SMB share `/config`.

- Home Assistant OS / Supervised: nainstalujte a spusťte
  oficiální add-on **Samba share**.
- V add-onu nastavte uživatele (username) a heslo.
- Ověřte, že z vašeho PC jde na HA připojení na SMB (typicky TCP 445)
  a že share `config` je dostupný jako `//IP_HA/config`.

Pokud nechcete SMB řešit, můžete deployovat i lokálně:
nastavte `HA_CONFIG_DIR` na cestu k HA configu na stejném stroji
(např. u Dockeru bind-mount).

### Vývojový stroj (Linux)

- `bash`, `sudo`
- CIFS klient: balíček `cifs-utils` (kvůli `mount -t cifs`)
- (volitelné) `npm` pouze pokud používáte separátní build frontendu
  v `dev/frontend` (v tomto repu typicky není)

## Proměnné prostředí a argumenty

Skript [dev/deploy.sh](../dev/deploy.sh) umí deployovat buď do lokálního
adresáře, nebo si sám připojí SMB share z HA.

### Environment variables

- `HA_CONFIG_DIR` – mount point / cesta k HA configu
  (default: `/mnt/ha-config`)
- `HA_IP` – IP adresa Home Assistant (pokud není předaná jako argument)
- `HA_USERNAME` – SMB uživatel (default: aktuální uživatel v OS)
- `HA_PASSWORD` – SMB heslo (pokud není předané jako argument;
  jinak se skript zeptá interaktivně)

### Argumenty

- `./deploy.sh` – deploy do `HA_CONFIG_DIR` (pokud je už přimountováno)
- `./deploy.sh IP PASSWORD` – přimountuje `//IP/config` a deployne
- `./deploy.sh clean [IP] [PASSWORD]` – odstraní integraci

## Struktura repozitáře

```text
custom_components/cez_hdo/        # integrace pro Home Assistant
  __init__.py                     # setup + registrace frontend karty
  sensor.py                       # senzory (časy, zbývá, surová data)
  binary_sensor.py                # binární senzory (aktivní tarif)
  downloader.py                   # komunikace s API
  base_entity.py                  # sdílené načítání/cache
  frontend/dist/cez-hdo-card.js   # buildnutý JS bundle karty

dev/deploy.sh                     # vývojový deploy do HA
docs/                             # dokumentace
```

## Deploy do HA

Použijte skript [dev/deploy.sh](../dev/deploy.sh).

Příklady:

```bash
# 1) Deploy přes Samba share add-on (SMB)
./dev/deploy.sh 192.168.1.50 mojeheslo

# 2) Deploy s jiným SMB uživatelem
HA_USERNAME=homeassistant ./dev/deploy.sh 192.168.1.50 mojeheslo

# 3) Lokální deploy (když máte HA config na disku)
HA_CONFIG_DIR=/path/to/ha-config ./dev/deploy.sh

# 4) Clean
./dev/deploy.sh clean 192.168.1.50 mojeheslo
```

Poznámka k frontendu:

- Integrace servíruje kartu z `/cez_hdo_card/cez-hdo-card.js`.

## Debug

Zapnutí logů:

```yaml
logger:
  logs:
    custom_components.cez_hdo: debug
```

Rychlá kontrola pro kartu:

- `http://IP_HA:8123/cez_hdo_card/cez-hdo-card.js?v=3.3.1` musí vracet `200`
- po update může být potřeba `Ctrl+F5`
