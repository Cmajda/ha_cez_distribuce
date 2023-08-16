"""Platform for sensor integration."""
from __future__ import annotations
import logging
from . import downloader
import voluptuous as vol
from datetime import timedelta, datetime, date
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA
)
import homeassistant.helpers.config_validation as cv
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util import Throttle

import requests
from lxml import html, etree

MIN_TIME_BETWEEN_SCANS = timedelta(seconds=3600)
_LOGGER = logging.getLogger(__name__)

DOMAIN = "cez_hdo"
CONF_REGION = "region"
CONF_CODE = "code"


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_REGION): cv.string,
        vol.Required(CONF_CODE): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    region = config.get(CONF_REGION)
    code = config.get(CONF_CODE)

    ents = []
    ents.append(CezHdo(region, code))
    add_entities(ents)


class CezHdo(BinarySensorEntity):
    def __init__(self, region, code):
        """Initialize the sensor."""
        self._name = "LowTariffActive"
        self.region = region
        self.code = code
        self.responseJson = "[]"
        self.update()

    @property
    def name(self):
        return DOMAIN + "_" + self._name

    @property
    def icon(self):
        return "mdi:power"

    @property
    def is_on(self):
        result = downloader.isHdo(self.responseJson["data"])
        low_tariff, closest_start_timeL, closest_end_timeL, duration_time_L, high_tariff, closest_start_timeH, closest_end_timeH, duration_time_H = result
        return low_tariff

    @property
    def extra_state_attributes(self):
        attributes = {}
        attributes["response_json"] = self.responseJson
        return attributes

    @property
    def should_poll(self):
        return True

    @property
    def available(self):
        return self.last_update_success

    @property
    def device_class(self):
        return ""

    @property
    def unique_id(self):
        return DOMAIN + "_" + self._name

    @Throttle(MIN_TIME_BETWEEN_SCANS)
    def update(self):

        response = requests.get(
            downloader.getRequestUrl(self.region, self.code))
        if response.status_code == 200:
            self.responseJson = response.json()
            self.last_update_success = True
        else:
            self.last_update_success = False
