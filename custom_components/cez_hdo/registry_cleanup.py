"""Helpers for keeping entity ids stable when EAN changes.

This integration is configured via YAML (setup_platform), so there is no config entry
we can use for HA's built-in migrations. When the configured EAN changes, the
integration creates entities with different unique_id values, but the old entity
registry entries remain and keep occupying the original entity_ids. That leads to
new entities being created with suffixes like "_2".

We store the last used EAN and remove old registry entries when the EAN changes.
"""

from __future__ import annotations

import asyncio
import logging

from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.storage import Store

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

_STORE_VERSION = 1
_STORE_KEY = f"{DOMAIN}_meta"

_LOCK_KEY = "ean_cleanup_lock"
_DONE_FOR_KEY = "ean_cleanup_done_for"


async def async_cleanup_entity_registry_if_ean_changed(hass, current_ean: str) -> None:
    """Remove stale entity registry entries when configured EAN changes.

    Assumption: this integration is intended to be configured with a single EAN.
    If multiple EANs are configured simultaneously, they would naturally collide
    on entity_ids (names are the same), so we treat an EAN change as a replacement.
    """

    domain_data = hass.data.setdefault(DOMAIN, {})
    lock: asyncio.Lock = domain_data.setdefault(_LOCK_KEY, asyncio.Lock())

    async with lock:
        if domain_data.get(_DONE_FOR_KEY) == current_ean:
            return

        store = Store(hass, _STORE_VERSION, _STORE_KEY)
        stored = await store.async_load() or {}
        last_ean = stored.get("last_ean")

        if last_ean and last_ean != current_ean:
            registry = er.async_get(hass)
            prefix = f"{last_ean}_"

            to_remove: list[str] = []
            for entry in registry.entities.values():
                if entry.platform != DOMAIN:
                    continue
                unique_id = entry.unique_id or ""
                if unique_id.startswith(prefix):
                    to_remove.append(entry.entity_id)

            for entity_id in to_remove:
                registry.async_remove(entity_id)

            _LOGGER.info(
                "CEZ HDO: EAN changed %s -> %s; removed %d old registry entries",
                last_ean,
                current_ean,
                len(to_remove),
            )

        await store.async_save({"last_ean": current_ean})
        domain_data[_DONE_FOR_KEY] = current_ean
