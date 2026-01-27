"""Frontend for CEZ HDO Cards."""

import logging
import os
import pathlib

from packaging.version import parse

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_call_later
from homeassistant.components.http import StaticPathConfig
from homeassistant.const import __version__

_LOGGER = logging.getLogger(__name__)

# Konstanty pro frontend kartu
DOMAIN = "cez_hdo"
URL_BASE = "/cez_hdo_card"
CEZ_HDO_CARDS = [
    {
        'name': 'CEZ HDO Card',
        'filename': 'cez-hdo-card.js',
        'version': '1.0.0'
    }
]


class CezHdoCardRegistration:
    """Class for managing CEZ HDO Lovelace card registration."""

    def __init__(self, hass: HomeAssistant):
        """Initialize the card registration."""
        self.hass = hass

    @property
    def lovelace_mode(self):
        """Get the current Lovelace mode."""
        ha_version = parse(__version__)
        if (ha_version.major >= 2026) or ((ha_version.major == 2025) and (ha_version.minor >= 2)):
            return self.hass.data["lovelace"].mode
        else:
            return self.hass.data["lovelace"]["mode"]

    @property
    def lovelace_resources(self):
        """Get Lovelace resources."""
        ha_version = parse(__version__)
        if (ha_version.major >= 2026) or ((ha_version.major == 2025) and (ha_version.minor >= 2)):
            return self.hass.data["lovelace"].resources
        else:
            return self.hass.data["lovelace"]["resources"]

    async def async_register(self):
        """Register the CEZ HDO card."""
        await self.async_register_cez_hdo_path()
        if self.lovelace_mode == "storage":
            await self.async_wait_for_lovelace_resources()

    async def async_register_cez_hdo_path(self):
        """Register custom cards path if not already registered."""
        try:
            # Složka dist obsahuje zkompilovaný JS soubor
            dist_path = pathlib.Path(__file__).parent / "dist"
            await self.hass.http.async_register_static_paths(
                [StaticPathConfig(URL_BASE, dist_path, False)]
            )
            _LOGGER.debug("Registered CEZ HDO path from %s", dist_path)
        except RuntimeError:
            _LOGGER.debug("CEZ HDO static path already registered")

    async def async_wait_for_lovelace_resources(self) -> None:
        """Wait for Lovelace resources to be loaded before registering cards."""
        async def check_lovelace_resources_loaded(now):
            if self.lovelace_resources.loaded:
                await self.async_register_cez_hdo_cards()
            else:
                _LOGGER.debug(
                    "Unable to install CEZ HDO Cards because Lovelace resources not yet loaded. "
                    "Trying again in 5 seconds"
                )
                async_call_later(self.hass, 5, check_lovelace_resources_loaded)

        await check_lovelace_resources_loaded(0)

    async def async_register_cez_hdo_cards(self):
        """Register CEZ HDO cards as Lovelace resources."""
        _LOGGER.debug("Installing Lovelace resource for CEZ HDO Cards")

        # Get resources already registered
        cez_hdo_resources = [
            resource
            for resource in self.lovelace_resources.async_items()
            if resource["url"].startswith(URL_BASE)
        ]

        for card in CEZ_HDO_CARDS:
            url = f"{URL_BASE}/{card.get('filename')}"

            card_registered = False

            for res in cez_hdo_resources:
                if self.get_resource_path(res["url"]) == url:
                    card_registered = True
                    # Check version
                    if self.get_resource_version(res["url"]) != card.get("version"):
                        # Update card version
                        _LOGGER.debug(
                            "Updating %s to version %s",
                            card.get("name"),
                            card.get("version")
                        )
                        await self.lovelace_resources.async_update_item(
                            res.get("id"),
                            {
                                "res_type": "module",
                                "url": url + "?v=" + card.get("version")
                            }
                        )
                        # Remove old gzipped files
                        await self.async_remove_gzip_files()
                    else:
                        _LOGGER.debug(
                            "%s already registered as version %s",
                            card.get("name"),
                            card.get("version")
                        )

            if not card_registered:
                _LOGGER.debug(
                    "Registering %s as version %s",
                    card.get("name"),
                    card.get("version")
                )
                await self.lovelace_resources.async_create_item({
                    "res_type": "module",
                    "url": url + "?v=" + card.get("version")
                })

    def get_resource_path(self, url: str):
        """Extract resource path from URL."""
        return url.split("?")[0]

    def get_resource_version(self, url: str):
        """Extract version from URL."""
        try:
            return url.split("?")[1].replace("v=", "")
        except Exception:
            return "0"

    async def async_unregister(self):
        """Unregister CEZ HDO cards from Lovelace resources."""
        if self.lovelace_mode == "storage":
            for card in CEZ_HDO_CARDS:
                url = f"{URL_BASE}/{card.get('filename')}"
                cez_hdo_resources = [
                    resource
                    for resource in self.lovelace_resources.async_items()
                    if str(resource["url"]).startswith(url)
                ]

                for resource in cez_hdo_resources:
                    await self.lovelace_resources.async_delete_item(resource.get("id"))

    async def async_remove_gzip_files(self):
        """Remove old gzip files asynchronously."""
        await self.hass.async_add_executor_job(self.remove_gzip_files)

    def remove_gzip_files(self):
        """Remove outdated gzip files."""
        _LOGGER.debug("remove_gzip_files")
        path = pathlib.Path(__file__).parent / "dist"

        if not path.exists():
            return

        gzip_files = [
            filename for filename in os.listdir(path) if filename.endswith(".gz")
        ]

        _LOGGER.debug("Found gzip files: %s", gzip_files)
        for file in gzip_files:
            try:
                gz_path = path / file
                original_path = path / file.replace('.gz', '')
                if original_path.exists() and gz_path.stat().st_mtime < original_path.stat().st_mtime:
                    _LOGGER.debug("Removing older gzip file - %s", file)
                    gz_path.unlink()
            except Exception:
                pass
