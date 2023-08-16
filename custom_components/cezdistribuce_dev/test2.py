import datetime
from datetime import timedelta
import json

try:
    # python 3.9+
    from zoneinfo import ZoneInfo
except ImportError:
    # python 3.6-3.8
    from backports.zoneinfo import ZoneInfo

calendar = '{"data" : [ {"primaryKey" : 5234,"ID" : 5234,"VALID_FROM" : 1679868000000,"VALID_TO" : 4070905200000,"DUMP_ID" : 45,"POVEL" : "A3B4DP2","KOD" : null,"KOD_POVELU" : "406","SAZBA" : "D57d","INFO" : "ET","PLATNOST" : "Po - Pá","DOBA" : "20","CAS_ZAP_1" : "0:00","CAS_VYP_1" : "5:35","CAS_ZAP_2" : "6:30","CAS_VYP_2" : "8:55","CAS_ZAP_3" : "9:55","CAS_VYP_3" : "15:35","CAS_ZAP_4" : "16:35","CAS_VYP_4" : "20:15","CAS_ZAP_5" : "21:15","CAS_VYP_5" : "23:59","CAS_ZAP_6" : null,"CAS_VYP_6" : null,"CAS_ZAP_7" : null,"CAS_VYP_7" : null,"CAS_ZAP_8" : null,"CAS_VYP_8" : null,"CAS_ZAP_9" : null,"CAS_VYP_9" : null,"CAS_ZAP_10" : null,"CAS_VYP_10" : null,"DATE_OF_ENTRY" : 1678866747000,"DESCRIPTION" : "2023_jaro_stred"},{"primaryKey" : 5235,"ID" : 5235,"VALID_FROM" : 1679868000000,"VALID_TO" : 4070905200000,"DUMP_ID" : 45,"POVEL" : "A3B4DP2","KOD" : null,"KOD_POVELU" : "406","SAZBA" : "D57d","INFO" : "ET","PLATNOST" : "So - Ne","DOBA" : "20","CAS_ZAP_1" : "0:00","CAS_VYP_1" : "9:10","CAS_ZAP_2" : "10:10","CAS_VYP_2" : "12:30","CAS_ZAP_3" : "13:30","CAS_VYP_3" : "18:55","CAS_ZAP_4" : "19:55","CAS_VYP_4" : "21:55","CAS_ZAP_5" : "22:55","CAS_VYP_5" : "23:59","CAS_ZAP_6" : null,"CAS_VYP_6" : null,"CAS_ZAP_7" : null,"CAS_VYP_7" : null,"CAS_ZAP_8" : null,"CAS_VYP_8" : null,"CAS_ZAP_9" : null,"CAS_VYP_9" : null,"CAS_ZAP_10" : null,"CAS_VYP_10" : null,"DATE_OF_ENTRY" : 1678866747000,"DESCRIPTION" : "2023_jaro_stred"} ],  "pageSize" : 20,  "pageNumber" : 1,  "pageOffset" : 0,  "pageBarItems" : 5,  "totalNumberOfRecords" : 2,  "pagingModel" : { },  "onePage" : true,  "firstRecordNumberForPage" : 0,  "lastPageNumber" : 1,  "lastRecordNumber" : 2,  "pageNumbersNavigation" : [ 1 ],  "defaultPageNumbersAround" : [ 1 ],  "fullyInitialized" : true,  "last" : true,  "first" : true}'


CEZ_TIMEZONE = ZoneInfo("Europe/Prague")


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


def duration(time1, time2):
    if time1 <= time2:
        datetime1 = datetime.datetime.combine(datetime.datetime.today(), time1)
        datetime2 = datetime.datetime.combine(datetime.datetime.today(), time2)
    else:
        datetime1 = datetime.datetime.combine(datetime.datetime.today(), time1)
        datetime2 = datetime.datetime.combine(
            datetime.datetime.today() + timedelta(days=1), time2)

    time_difference = datetime2 - datetime1
    return time_difference


def isLowTariff(jsonCalendar):
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


data = json.loads(calendar)

result = isLowTariff(data["data"])

low_tariff, closest_start_timeL, closest_end_timeL, duration_time_L, high_tariff, closest_start_timeH, closest_end_timeH, duration_time_H = result

if low_tariff:
    print("Nízký tarif od:", closest_start_timeL.strftime("%H:%M"), "do",
          closest_end_timeL.strftime("%H:%M"), "trvání:", duration_time_L)
if high_tariff:
    print("Vysoký tarif od:", closest_start_timeH.strftime("%H:%M"), "do",
          closest_end_timeH.strftime("%H:%M"), "trvání:", duration_time_H)
