# ČEZ HDO – Vývojářská dokumentace

Stručný přehled pro vývoj/přispívání.

## Požadavky

### Home Assistant

Pro vývojový deploy přes [dev/deploy.sh](../dev/deploy.sh) je nejjednodušší mít v HA dostupný SMB share `/config`.

- Home Assistant OS / Supervised: nainstalujte a spusťte oficiální add-on **Samba share**.
- V add-onu nastavte uživatele (username) a heslo.
- Ověřte, že z vašeho PC jde na HA připojení na SMB (typicky TCP 445) a že share `config` je dostupný jako `//IP_HA/config`.

Pokud nechcete SMB řešit, můžete deployovat i lokálně: nastavte `HA_CONFIG_DIR` na cestu k HA configu na stejném stroji (např. u Dockeru bind-mount).

### Vývojový stroj (Linux)

- `bash`, `sudo`
- CIFS klient: balíček `cifs-utils` (kvůli `mount -t cifs`)
- (volitelné) `npm` pouze pokud používáte separátní build frontendu v `dev/frontend` (v tomto repu typicky není)

## Proměnné prostředí a argumenty

Skript [dev/deploy.sh](../dev/deploy.sh) umí deployovat buď do lokálního adresáře, nebo si sám připojí SMB share z HA.

### Environment variables

- `HA_CONFIG_DIR` – mount point / cesta k HA configu (default: `/mnt/ha-config`)
- `HA_IP` – IP adresa Home Assistant (pokud není předaná jako argument)
- `HA_USERNAME` – SMB uživatel (default: aktuální uživatel v OS)
- `HA_PASSWORD` – SMB heslo (pokud není předané jako argument; jinak se skript zeptá interaktivně)
- `DEPLOY_WWW` – `1` = navíc zkopíruje kartu do `/config/www/cez_hdo` jako fallback pro `/local/...` (default: `0`)

### Argumenty

- `./deploy.sh` – deploy do `HA_CONFIG_DIR` (pokud je už přimountováno)
- `./deploy.sh IP PASSWORD` – přimountuje `//IP/config` a deployne
- `./deploy.sh clean [IP] [PASSWORD]` – odstraní integraci + volitelně i `www/cez_hdo`

## Struktura repozitáře

```text
custom_components/cez_hdo/        # integrace pro Home Assistant
  __init__.py                     # setup + registrace frontend karty
  sensor.py                       # senzory (časy, zbývá, surová data)
  binary_sensor.py                # binární senzory (aktivní tarif)
  downloader.py                   # komunikace s API
  base_entity.py                  # sdílené načítání/cache
  frontend/dist/cez-hdo-card.js   # buildnutý JS bundle karty

www/cez_hdo/cez-hdo-card.js       # kopie JS (pomocné / fallback)
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

# 3) Deploy do /config/www jako fallback pro /local
DEPLOY_WWW=1 ./dev/deploy.sh 192.168.1.50 mojeheslo

# 4) Lokální deploy (když máte HA config na disku)
HA_CONFIG_DIR=/path/to/ha-config ./dev/deploy.sh

# 5) Clean
./dev/deploy.sh clean 192.168.1.50 mojeheslo
```

Poznámka k frontendu:

- Preferovaná URL pro zdroj karty je `/cez_hdo/cez-hdo-card.js` (servírované z integrace).
- Existuje i fallback kopie do `config/www/cez_hdo`.

## Debug

Zapnutí logů:

```yaml
logger:
  logs:
    custom_components.cez_hdo: debug
```

Rychlá kontrola pro kartu:

- `http://IP_HA:8123/cez_hdo/cez-hdo-card.js` musí vracet `200`
- po update může být potřeba `Ctrl+F5`
