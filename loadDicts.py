import os
import errno
import json
from unicodedata import normalize

DICT_FOLDER = "dicts/"
route_codes = {}
timetable_remarks = {}

def get_route_code(origin: str, destination: str):
  for route in route_codes:
    if route["origin"].lower() == origin.lower() and route["destination"].lower() == destination.lower():
      return route["route_code"]
  return ""

def get_remarks(route_code: str):
  for remarks in timetable_remarks:
    if route_code.upper() in remarks["route_codes"]:
      return remarks["remarks"]
  return []

if not os.path.isdir(DICT_FOLDER):
  raise FileNotFoundError(
    errno.ENOENT, os.strerror(errno.ENOENT), DICT_FOLDER)
else:
  with open(DICT_FOLDER + "routeCodes.json", 'r') as f:
    json_file = json.load(f)
    route_codes = json_file["route_codes"]
  with open(DICT_FOLDER + "timetableRemarks.json", 'r') as f:
    json_file = json.load(f)
    timetable_remarks = json_file["timetable_remarks"]
