"""Platform for sensor integration."""
from __future__ import annotations
import logging
from datetime import time
import voluptuous as vol

from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorEntity,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .base_entity import CezHdoBaseEntity
from . import downloader

_LOGGER = logging.getLogger(__name__)

CONF_EAN = "ean"
CONF_SIGNAL = "signal"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
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
    """Set up the CEZ HDO sensor platform."""
    ean = config[CONF_EAN]
    signal = config.get(CONF_SIGNAL)

    entities = [
        LowTariffStart(ean, signal),
        LowTariffEnd(ean, signal),
        LowTariffDuration(ean, signal),
        HighTariffStart(ean, signal),
        HighTariffEnd(ean, signal),
        HighTariffDuration(ean, signal),
        CezHdoRawData(ean, signal),  # Nová entita
    ]
    add_entities(entities, True)


class CezHdoSensor(CezHdoBaseEntity, SensorEntity):
    """Base class for CEZ HDO sensors."""

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock"


class LowTariffStart(CezHdoSensor):
    """Sensor for low tariff start time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "LowTariffStart", signal)

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[1]  # low_tariff_start


class LowTariffEnd(CezHdoSensor):
    """Sensor for low tariff end time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "LowTariffEnd", signal)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[2]  # low_tariff_end


class LowTariffDuration(CezHdoSensor):
    """Sensor for low tariff duration."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "LowTariffDuration", signal)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        duration = hdo_data[3]  # low_tariff_duration
        if duration is None:
            return None
        return downloader.format_duration(duration)


class HighTariffStart(CezHdoSensor):
    """Sensor for high tariff start time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "HighTariffStart", signal)

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[5]  # high_tariff_start


class HighTariffEnd(CezHdoSensor):
    """Sensor for high tariff end time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "HighTariffEnd", signal)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> time | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        return hdo_data[6]  # high_tariff_end


class HighTariffDuration(CezHdoSensor):
    """Sensor for high tariff duration."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "HighTariffDuration", signal)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:timer"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        hdo_data = self._get_hdo_data()
        duration = hdo_data[7]  # high_tariff_duration
        if duration is None:
            return None
        return downloader.format_duration(duration)


class CezHdoRawData(CezHdoSensor):
    """Sensor for raw HDO JSON data and timestamp."""
    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "RawData", signal)
        self._attr_name = "CEZ HDO Raw Data"
        self._attr_unique_id = f"{ean}_raw_data"

    @property
    def native_value(self) -> str | None:
        """Return the timestamp from cache in format 'DD.MM.YYYY HH:mm'."""
        hdo_data = self._get_hdo_data()
        # Získat timestamp z cache
        try:
            cache_file = self.cache_file
            import json
            from pathlib import Path
            if Path(cache_file).exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_content = json.load(f)
                timestamp = cache_content.get("timestamp")
                if timestamp:
                    from datetime import datetime
                    dt = datetime.fromisoformat(timestamp)
                    return dt.strftime("%d.%m.%Y %H:%M")
        except Exception as e:
            _LOGGER.warning("CEZ HDO RAW: Failed to get timestamp: %s", e)
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return the full JSON data as attribute."""
        try:
            cache_file = self.cache_file
            import json
            from pathlib import Path
            if Path(cache_file).exists():
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_content = json.load(f)
                return {"raw_json": cache_content}
        except Exception as e:
            _LOGGER.warning("CEZ HDO RAW: Failed to get raw json: %s", e)
        return {}
