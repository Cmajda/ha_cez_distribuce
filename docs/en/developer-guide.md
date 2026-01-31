# ČEZ HDO – Developer Documentation

A brief overview for development/contribution.

## Requirements

### Home Assistant

For development deployment via [dev/deploy.sh](../dev/deploy.sh),
the easiest approach is to have an SMB share `/config` available in HA.

- Home Assistant OS / Supervised: install and start
  the official **Samba share** add-on.
- Configure username and password in the add-on.
- Verify that your PC can connect to HA via SMB (typically TCP 445)
  and that the `config` share is available as `//IP_HA/config`.

If you don't want to set up SMB, you can deploy locally:
set `HA_CONFIG_DIR` to the path of HA config on the same machine
(e.g., with Docker bind-mount).

### Development Machine (Linux)

- `bash`, `sudo`
- CIFS client: `cifs-utils` package (for `mount -t cifs`)
- (optional) `npm` only if using separate frontend build
  in `dev/frontend` (typically not used in this repo)

## Environment Variables and Arguments

The [dev/deploy.sh](../dev/deploy.sh) script can deploy either to a local
directory or mount an SMB share from HA.

### Environment Variables

- `HA_CONFIG_DIR` – mount point / path to HA config
  (default: `/mnt/ha-config`)
- `HA_IP` – Home Assistant IP address (if not passed as argument)
- `HA_USERNAME` – SMB username (default: current OS user)
- `HA_PASSWORD` – SMB password (if not passed as argument;
  otherwise the script will prompt interactively)
- `DEPLOY_WWW` – `1` = also copy the card to `/config/www/cez_hdo`
  as fallback for `/local/...` (default: `0`)

### Arguments

- `./deploy.sh` – deploy to `HA_CONFIG_DIR` (if already mounted)
- `./deploy.sh IP PASSWORD` – mount `//IP/config` and deploy
- `./deploy.sh clean [IP] [PASSWORD]` – remove integration + optionally `www/cez_hdo`

## Repository Structure

```text
custom_components/cez_hdo/        # Home Assistant integration
  __init__.py                     # setup + frontend card registration
  sensor.py                       # sensors (times, remaining, raw data)
  binary_sensor.py                # binary sensors (active tariff)
  downloader.py                   # API communication
  base_entity.py                  # shared loading/cache
  frontend/dist/cez-hdo-card.js   # built JS bundle for card

www/cez_hdo/cez-hdo-card.js       # JS copy (helper / fallback)
dev/deploy.sh                     # development deploy to HA
docs/                             # documentation
```

## Deploy to HA

Use the [dev/deploy.sh](../dev/deploy.sh) script.

Examples:

```bash
# 1) Deploy via Samba share add-on (SMB)
./dev/deploy.sh 192.168.1.50 mypassword

# 2) Deploy with different SMB user
HA_USERNAME=homeassistant ./dev/deploy.sh 192.168.1.50 mypassword

# 3) Deploy to /config/www as fallback for /local
DEPLOY_WWW=1 ./dev/deploy.sh 192.168.1.50 mypassword

# 4) Local deploy (when you have HA config on disk)
HA_CONFIG_DIR=/path/to/ha-config ./dev/deploy.sh

# 5) Clean
./dev/deploy.sh clean 192.168.1.50 mypassword
```

Note on frontend:

- Preferred URL for card source is `/cez_hdo/cez-hdo-card.js` (served from integration).
- There's also a fallback copy to `config/www/cez_hdo`.

## Debug

Enable logs:

```yaml
logger:
  logs:
    custom_components.cez_hdo: debug
```

Quick check for card:

- `http://HA_IP:8123/cez_hdo/cez-hdo-card.js` should return `200`
- After update, you may need to press `Ctrl+F5`
