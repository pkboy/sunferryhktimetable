from pathlib import Path 
from datetime import *
import csv
import json
import os
import loadDicts
import interpretServiceDates

DATA_FOLDER = "sunferry_timetables"

# remarks aren't found in the CSVs but in Sunferry's dataspec document
# https://www.sunferry.com.hk/eta/SunFerry_time_table_and_fare_table_dataspec_eng.pdf


language_key = {
  "to" : {
    "eng" : "to",
    "cht" : "至",
    "chs" : "至"
  }
}

def parseCsv(csvfile):
  print("Parsing {filename}".format(filename=str(csvfile.resolve())))
  source_file = open(str(csvfile.resolve()))
  source_reader = csv.DictReader(source_file)
  source_reader.fieldnames

  timetable = {
    "routes" : [],
    "remarks": []
  }

  # Direction,Service Date,Service Hour,Remark
  for row in source_reader:
    # Direction,Service Date,Service Hour,Remark
    # Central to Cheung Chau,Mondays to Saturdays except public holidays,12:30 a.m.,
    origin = str.strip(row["Direction"].split(language_key["to"]["eng"])[0])
    dest = str.strip(row["Direction"].split(language_key["to"]["eng"])[1])

    serviceDaysString = str.strip(row["Service Date"])
    departureTime = str.strip(row["Service Hour"])
    departureTime = departureTime.replace("a.m.", "AM")
    departureTime = departureTime.replace("p.m.", "PM")
    departureTime = departureTime.replace("noon", "PM")
    departureTime = str(datetime.strptime(departureTime, "%I:%M %p").strftime("%H:%M"))
    departureRemark = str.strip(row["Remark"])

    route_code = loadDicts.get_route_code(origin, dest)
    if route_code and len(timetable["remarks"]) == 0:
      timetable["remarks"] = loadDicts.get_remarks(route_code)

    serviceDays = interpretServiceDates.get_service_days(serviceDaysString)
    
    departures = { 
      "dayStart": serviceDays["dayStart"],
      "dayEnd": serviceDays["dayEnd"],
      "runOnPublicHoliday": serviceDays["runOnPublicHoliday"],
      "serviceDaysString" : serviceDaysString,
      "serviceTimes" : [
        {
          "time" : departureTime, 
          "remark" : departureRemark
        }
      ]
    }
    
    current_row = {
      "routeCode": route_code,
      "origin": origin,
      "destination": dest,
      "departures": [ departures ]
    }

    row_exists = False
    for i in range(len(timetable["routes"])):
      trow = timetable["routes"][i]
      if trow["routeCode"] == current_row["routeCode"]:
        row_exists = True
        svc_day_exists = False
        for j in range(len(trow["departures"])):
          trow_svc_day = trow["departures"][j]["serviceDaysString"]
          if trow_svc_day.lower() == departures["serviceDaysString"].lower():
            svc_day_exists = True
            timetable["routes"][i]["departures"][j]["serviceTimes"].extend(departures["serviceTimes"])
            break
        if not svc_day_exists:
          timetable["routes"][i]["departures"].append(departures)
          break

    if not row_exists:
      timetable["routes"].append(current_row)

  json_timetable = json.dumps(timetable, indent=4)
  basename = os.path.basename(str(csvfile.resolve()))
  filename = os.path.splitext(basename)[0]
  with open("json/" + filename + '.json', 'w') as f:
    f.write(json_timetable)
  

p = Path(DATA_FOLDER).glob('**/*')
files = [x for x in p if x.is_file()]
for file in files:
  if os.path.splitext(str(file.resolve()))[0].endswith("_eng"):
    parseCsv(file)
