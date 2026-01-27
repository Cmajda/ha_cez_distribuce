"""Platform for sensor integration."""
from __future__ import annotations
import logging
from typing import Any
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
        CurrentPrice(ean, signal),
        CezHdoRawData(ean, signal),  # Nová entita
    ]
    add_entities(entities, False)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the CEZ HDO sensor platform (async).

    This integration is configured via YAML. When EAN changes, old entries in the
    entity registry can keep occupying the previous entity_ids and HA will create
    new ones with suffixes like "_2". We proactively remove stale entries.
    """

    ean = config[CONF_EAN]
    signal = config.get(CONF_SIGNAL)

    from .registry_cleanup import async_cleanup_entity_registry_if_ean_changed

    await async_cleanup_entity_registry_if_ean_changed(hass, ean)

    entities = [
        LowTariffStart(ean, signal),
        LowTariffEnd(ean, signal),
        LowTariffDuration(ean, signal),
        HighTariffStart(ean, signal),
        HighTariffEnd(ean, signal),
        HighTariffDuration(ean, signal),
        CurrentPrice(ean, signal),
        CezHdoRawData(ean, signal),
    ]
    async_add_entities(entities, False)


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
        signals: list[dict[str, Any]] = []
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
            value = hdo_data[1]  # low_tariff_start
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s LowTariffStart failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
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
            value = hdo_data[2]  # low_tariff_end
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s LowTariffEnd failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
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
            duration = hdo_data[3]  # low_tariff_duration
            if duration is None:
                return None
            return downloader.format_duration(duration)
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s LowTariffDuration failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
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
            value = hdo_data[5]  # high_tariff_start
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s HighTariffStart failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
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
            value = hdo_data[6]  # high_tariff_end
            if value is None:
                return None
            return value.strftime("%H:%M")
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s HighTariffEnd failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
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
            duration = hdo_data[7]  # high_tariff_duration
            if duration is None:
                return None
            return downloader.format_duration(duration)
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s HighTariffDuration failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
            return None


class CurrentPrice(CezHdoSensor):
    """Sensor for current electricity price based on active tariff."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "CurrentPrice", signal)

    @property
    def _low_tariff_price(self) -> float:
        """Get low tariff price from hass.data."""
        if self.hass and "cez_hdo" in self.hass.data:
            return self.hass.data["cez_hdo"].get("low_tariff_price", 0.0)
        return 0.0

    @property
    def _high_tariff_price(self) -> float:
        """Get high tariff price from hass.data."""
        if self.hass and "cez_hdo" in self.hass.data:
            return self.hass.data["cez_hdo"].get("high_tariff_price", 0.0)
        return 0.0

    @property
    def icon(self) -> str:
        """Return the icon of the sensor."""
        return "mdi:currency-usd"

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement."""
        return "Kč/kWh"

    @property
    def device_class(self) -> str:
        """Return the device class."""
        return "monetary"

    @property
    def native_value(self) -> float | None:
        """Return the current price based on active tariff."""
        try:
            hdo_data = self._get_hdo_data()
            is_low_tariff = hdo_data[0]  # low_tariff_active
            is_high_tariff = hdo_data[4]  # high_tariff_active

            if is_low_tariff:
                return self._low_tariff_price
            elif is_high_tariff:
                return self._high_tariff_price
            else:
                # Pokud není aktivní ani jeden tarif, vrátíme vysoký tarif jako výchozí
                return self._high_tariff_price
        except Exception as err:
            _LOGGER.error(
                "CEZ HDO: %s CurrentPrice failed: %s",
                getattr(self, "entity_id", self.name),
                err,
            )
            return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return additional attributes."""
        hdo_data = self._get_hdo_data()
        is_low_tariff = hdo_data[0] if hdo_data else False
        return {
            "low_tariff_price": self._low_tariff_price,
            "high_tariff_price": self._high_tariff_price,
            "active_tariff": "low" if is_low_tariff else "high",
        }


class CezHdoRawData(CezHdoSensor):
    """Sensor for raw HDO JSON data and timestamp."""

    def __init__(self, ean: str, signal: str | None = None) -> None:
        super().__init__(ean, "RawData", signal)
        # Keep a stable unique_id (historical behavior), but let base_entity
        # provide friendly name + suggested object_id.
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
