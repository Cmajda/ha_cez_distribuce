# ČEZ HDO – Developer Documentation

A brief overview for development/contribution.

## Requirements

### Local Python Development

The project requires Python **3.14.2 through 3.15.0** and uses `uv` to create
the `.venv` virtual environment and install tools declared in `pyproject.toml`.

```bash
uv sync --group dev
uv run pre-commit install
uv run pre-commit run --all-files
```

VS Code uses `${workspaceFolder}/.venv/bin/python`; `uv sync` creates the
environment at that path. Before committing, verify that `uv.lock` matches the
project:

```bash
uv lock --check
```

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

### Arguments

- `./deploy.sh` – deploy to `HA_CONFIG_DIR` (if already mounted)
- `./deploy.sh IP PASSWORD` – mount `//IP/config` and deploy
- `./deploy.sh clean [IP] [PASSWORD]` – remove the integration

## Repository Structure

```text
custom_components/cez_hdo/        # Home Assistant integration
  __init__.py                     # setup + frontend card registration
  sensor.py                       # sensors (times, remaining, raw data)
  binary_sensor.py                # binary sensors (active tariff)
  downloader.py                   # API communication
  base_entity.py                  # shared loading/cache
  frontend/dist/cez-hdo-card.js   # built JS bundle for card

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

# 3) Local deploy (when you have HA config on disk)
HA_CONFIG_DIR=/path/to/ha-config ./dev/deploy.sh

# 4) Clean
./dev/deploy.sh clean 192.168.1.50 mypassword
```

Note on frontend:

- The integration serves the card from `/cez_hdo_card/cez-hdo-card.js`.

## Debug

Enable logs:

```yaml
logger:
  logs:
    custom_components.cez_hdo: debug
```

Quick check for card:

- `http://HA_IP:8123/cez_hdo_card/cez-hdo-card.js?v=3.3.1` should return `200`
- After update, you may need to press `Ctrl+F5`
