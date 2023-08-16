import requests
import datetime
from datetime import timedelta
import json

try:
    # python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:
    # python 3.6-3.8
    from backports.zoneinfo import ZoneInfo


BASE_URL = "https://www.cezdistribuce.cz/distHdo/adam/containers/"
CEZ_TIMEZONE = ZoneInfo("Europe/Prague")


def getCorrectRegionName(region):
    region = region.lower()
    for x in ["zapad", "sever", "stred", "vychod", "morava"]:
        if x in region:
            return x


def getRequestUrl(region, code):
    region = getCorrectRegionName(region)
    return BASE_URL + region + "?&code=" + code.upper()


def timeInRange(start, end, x):
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def parseTime(date_time_str):
    if not date_time_str:
        return datetime.time(0, 0)
    else:
        return datetime.datetime.strptime(date_time_str, "%H:%M").time()


def isHdo(jsonCalendar):
    """
    Find out if the HDO is enabled for the current timestamp

    :param jsonCalendar: JSON with calendar schedule from CEZ
    :param daytime: relevant time in "Europe/Prague" timezone to check if HDO is on or not
    :return: bool
    """
    daytime = datetime.datetime.now(tz=CEZ_TIMEZONE)
    if daytime.weekday() < 5:
        dayCalendar = jsonCalendar[0]
    else:
        dayCalendar = jsonCalendar[1]

    checkedTime = daytime.time()
    # checkedTime=datetime.time(21,0,00,000000)
    low_tariff = False
    closest_start_timeL = None
    closest_end_timeL = None
    duration_time_L = None
    high_tariff = False
    closest_start_timeH = None
    closest_end_timeH = None
    duration_time_H = None
    a = 1

    for i in range(1, 11):
        if i == 10:
            a = 0
        startTimeL = parseTime(dayCalendar["CAS_ZAP_" + str(i)])
        endTimeL = parseTime(dayCalendar["CAS_VYP_" + str(i)])
        startTimeH = parseTime(dayCalendar["CAS_VYP_" + str(i)])
        endTimeH = parseTime(dayCalendar["CAS_ZAP_" + str(i+a)])
        low_tariff = low_tariff or timeInRange(
            start=startTimeL, end=endTimeL, x=checkedTime)
        high_tariff = high_tariff or timeInRange(
            start=startTimeH, end=endTimeH, x=checkedTime)
        if low_tariff and startTimeL != endTimeL and timeInRange(start=startTimeL, end=endTimeL, x=checkedTime):
            closest_start_timeL = startTimeL
            closest_end_timeL = endTimeL
            duration_time_L = duration(checkedTime, endTimeL)
            # print("Nízký tarif od: " + startTimeL.strftime("%H:%M") + " do " + endTimeL.strftime("%H:%M") + "trvání: " , duration_time_L)
        if high_tariff and startTimeH != endTimeH and timeInRange(start=startTimeH, end=endTimeH, x=checkedTime):
            closest_start_timeH = startTimeH
            closest_end_timeH = endTimeH
            duration_time_H = duration(checkedTime, endTimeH)
            # print("Vysoký tarif od: " + startTimeH.strftime("%H:%M") + " do " + endTimeH.strftime("%H:%M") + "trvání: " , duration_time_H)

    return low_tariff, closest_start_timeL, closest_end_timeL, duration_time_L, high_tariff, closest_start_timeH, closest_end_timeH, duration_time_H
