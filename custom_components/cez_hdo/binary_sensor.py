"""Platform for binary sensor integration."""
from __future__ import annotations
import logging
import voluptuous as vol

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
)
from homeassistant.components.sensor import PLATFORM_SCHEMA as BASE_PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .base_entity import CezHdoBaseEntity
from . import downloader

_LOGGER = logging.getLogger(__name__)

CONF_EAN = "ean"
CONF_SIGNAL = "signal"

PLATFORM_SCHEMA = BASE_PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EAN): cv.string,
        vol.Optional(CONF_SIGNAL): cv.string,
    }
)


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO binary sensor platform."""
    ean = config[CONF_EAN]
    signal = config.get(CONF_SIGNAL)

    entities = [
        LowTariffActive(ean, signal),
        HighTariffActive(ean, signal),
    ]
    add_entities(entities, True)


class CezHdoBinarySensor(CezHdoBaseEntity, BinarySensorEntity):
    """Base class for CEZ HDO binary sensors."""

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:power"

    @property
    def device_class(self) -> str | None:
        """Return the device class of the sensor."""
        return None

    def _get_signal(self, hdo_data):
        """Vrátí signál: pokud není zadaný, vezme první dostupný z JSON."""
        if self.signal:
            _LOGGER.info(f"CEZ HDO: Používám signál z konfigurace: {self.signal}")
            return self.signal
        try:
            cache_file = self.cache_file
            import json
            from pathlib import Path
            from datetime import datetime
            if Path(cache_file).exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_content = json.load(f)
                signals = cache_content.get("data", {}).get("data", {}).get("signals", [])
                today = datetime.now().strftime("%d.%m.%Y")
                for s in signals:
                    if downloader.normalize_datum(s.get("datum")) == today and s.get("signal"):
                        _LOGGER.info(f"CEZ HDO: První signál pro dnešní den v cache: {s['signal']}")
                        return s["signal"]
                # fallback: první signál v poli
                if signals and signals[0].get("signal"):
                    _LOGGER.info(f"CEZ HDO: Fallback - první dostupný signál v cache: {signals[0]['signal']}")
                    return signals[0]["signal"]
                else:
                    _LOGGER.warning(f"CEZ HDO: Pole 'signals' je prázdné nebo neobsahuje klíč 'signal'.")
            else:
                _LOGGER.warning(f"CEZ HDO: Cache file {cache_file} neexistuje.")
        except Exception as e:
            _LOGGER.warning(f"CEZ HDO: Chyba při získávání signálu z cache: {e}")
        return None


class LowTariffActive(CezHdoBinarySensor):
    """Binary sensor for low tariff active state."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "LowTariffActive", signal)

    @property
    def is_on(self) -> bool | None:
        """Return True if low tariff is active."""
        hdo_data = self._get_hdo_data()
        return hdo_data[0]  # low_tariff_active


class HighTariffActive(CezHdoBinarySensor):
    """Binary sensor for high tariff active state."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "HighTariffActive", signal)

    @property
    def is_on(self) -> bool | None:
        """Return True if high tariff is active."""
        hdo_data = self._get_hdo_data()
        return hdo_data[4]  # high_tariff_active
