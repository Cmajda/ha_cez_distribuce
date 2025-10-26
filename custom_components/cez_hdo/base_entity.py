"""Base entity for CEZ HDO sensors."""
from __future__ import annotations
import logging
from datetime import timedelta
from typing import Any

import requests
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

from . import downloader

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=3600)
_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"


class CezHdoBaseEntity(Entity):
    """Base class for CEZ HDO entities."""

    def __init__(self, region: str, code: str, name: str) -> None:
        """Initialize the sensor."""
        self.region = region
        self.code = code
        self._name = name
        self._response_data: dict[str, Any] | None = None
        self._last_update_success = False
        self.update()

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"{DOMAIN}_{self._name}"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return f"{DOMAIN}_{self._name}"

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state."""
        return True

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        attributes = {}
        if self._response_data is not None:
            attributes["response_json"] = self._response_data
        return attributes

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self) -> None:
        """Fetch new state data for the sensor."""
        try:
            response = requests.get(
                downloader.get_request_url(self.region, self.code),
                timeout=30
            )
            response.raise_for_status()
            self._response_data = response.json()
            self._last_update_success = True
            _LOGGER.debug("Successfully updated CEZ HDO data")
        except requests.exceptions.RequestException as err:
            _LOGGER.error("Error fetching CEZ HDO data: %s", err)
            self._last_update_success = False
        except ValueError as err:
            _LOGGER.error("Error parsing CEZ HDO JSON response: %s", err)
            self._last_update_success = False

    def _get_hdo_data(self) -> tuple[bool, Any, Any, Any, bool, Any, Any, Any]:
        """Get HDO data from response."""
        if self._response_data is None:
            return False, None, None, None, False, None, None, None
        
        try:
            return downloader.isHdo(self._response_data["data"])
        except (KeyError, TypeError) as err:
            _LOGGER.error("Error processing HDO data: %s", err)
            return False, None, None, None, False, None, None, None