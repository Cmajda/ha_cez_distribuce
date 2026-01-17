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
    add_entities(entities, False)


class CezHdoSensor(CezHdoBaseEntity, SensorEntity):
    """Base class for CEZ HDO sensors."""

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock"

    def _get_signal(self, hdo_json: dict | None):
        """Vrátí signál pro dnešní den z již načtených dat (bez file I/O)."""
        if self.signal:
            return self.signal

        if not hdo_json:
            return None

        data_level = hdo_json.get("data")
        if isinstance(data_level, dict) and "data" in data_level:
            data_level = data_level.get("data")
        signals = []
        if isinstance(data_level, dict):
            signals = data_level.get("signals", []) or []

        from datetime import datetime

        today = datetime.now().strftime("%d.%m.%Y")
        for s in signals:
            if downloader.normalize_datum(s.get("datum")) == today and s.get("signal"):
                return s["signal"]

        if signals and signals[0].get("signal"):
            return signals[0]["signal"]
        return None


class LowTariffStart(CezHdoSensor):
    """Sensor for low tariff start time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "LowTariffStart", signal)

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        try:
            hdo_data = self._get_hdo_data()
            _LOGGER.debug("CEZ HDO: %s native_value hdo_data=%s", getattr(self, "entity_id", self.name), hdo_data)
            value = hdo_data[1]  # low_tariff_start
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error("CEZ HDO: %s LowTariffStart failed: %s", getattr(self, "entity_id", self.name), err)
            return None


class LowTariffEnd(CezHdoSensor):
    """Sensor for low tariff end time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "LowTariffEnd", signal)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        try:
            hdo_data = self._get_hdo_data()
            _LOGGER.debug("CEZ HDO: %s native_value hdo_data=%s", getattr(self, "entity_id", self.name), hdo_data)
            value = hdo_data[2]  # low_tariff_end
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error("CEZ HDO: %s LowTariffEnd failed: %s", getattr(self, "entity_id", self.name), err)
            return None


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
        try:
            hdo_data = self._get_hdo_data()
            _LOGGER.debug("CEZ HDO: %s native_value hdo_data=%s", getattr(self, "entity_id", self.name), hdo_data)
            duration = hdo_data[3]  # low_tariff_duration
            if duration is None:
                return None
            return downloader.format_duration(duration)
        except Exception as err:
            _LOGGER.error("CEZ HDO: %s LowTariffDuration failed: %s", getattr(self, "entity_id", self.name), err)
            return None


class HighTariffStart(CezHdoSensor):
    """Sensor for high tariff start time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "HighTariffStart", signal)

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        try:
            hdo_data = self._get_hdo_data()
            _LOGGER.debug("CEZ HDO: %s native_value hdo_data=%s", getattr(self, "entity_id", self.name), hdo_data)
            value = hdo_data[5]  # high_tariff_start
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error("CEZ HDO: %s HighTariffStart failed: %s", getattr(self, "entity_id", self.name), err)
            return None


class HighTariffEnd(CezHdoSensor):
    """Sensor for high tariff end time."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "HighTariffEnd", signal)

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:home-clock-outline"

    @property
    def native_value(self) -> str | None:
        """Return the state of the sensor."""
        try:
            hdo_data = self._get_hdo_data()
            _LOGGER.debug("CEZ HDO: %s native_value hdo_data=%s", getattr(self, "entity_id", self.name), hdo_data)
            value = hdo_data[6]  # high_tariff_end
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error("CEZ HDO: %s HighTariffEnd failed: %s", getattr(self, "entity_id", self.name), err)
            return None


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
        try:
            hdo_data = self._get_hdo_data()
            _LOGGER.debug("CEZ HDO: %s native_value hdo_data=%s", getattr(self, "entity_id", self.name), hdo_data)
            duration = hdo_data[7]  # high_tariff_duration
            if duration is None:
                return None
            return downloader.format_duration(duration)
        except Exception as err:
            _LOGGER.error("CEZ HDO: %s HighTariffDuration failed: %s", getattr(self, "entity_id", self.name), err)
            return None


class CezHdoRawData(CezHdoSensor):
    """Sensor for raw HDO JSON data and timestamp."""
    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "RawData", signal)
        self._attr_name = "CEZ HDO Raw Data"
        self._attr_unique_id = f"{ean}_raw_data"

    @property
    def native_value(self) -> str | None:
        """Return the timestamp from cache in format 'DD.MM.YYYY HH:mm'."""
        # Ensure data is loaded / update scheduled
        _ = self._get_hdo_data()
        if self._last_update_time:
            return self._last_update_time.strftime("%d.%m.%Y %H:%M")
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return the full JSON data as attribute."""
        _ = self._get_hdo_data()
        if self._response_data is None:
            return {}
        ts = self._last_update_time.isoformat() if self._last_update_time else None
        # Structure matches cache file format: {timestamp, data}
        return {"raw_json": {"timestamp": ts, "data": self._response_data}}
