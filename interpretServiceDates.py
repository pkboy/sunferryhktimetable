# Not the best practice but we know that they use 5 strings of text for the Service Date field
#
# Sundays and public holidays
# Mondays to Saturdays except public holidays
# Mondays to Fridays except public holidays
# Saturdays except public holidays
# Daily
#
# So just match any string and return the relevant object
# Placed in its own module in case this changes or if I want to do a text intrepeter.

service_dates = [
  { 
    "from_document" : "sundays and public holidays",
    "service_days" : {
      "dayStart" : 6,
      "dayEnd" : 6,
      "runOnPublicHoliday" : 1
    }
  },
  { 
    "from_document" : "saturdays except public holidays",
    "service_days" : {
      "dayStart" : 5,
      "dayEnd" : 5,
      "runOnPublicHoliday" : 0
    }
  },
  { 
    "from_document" : "mondays to saturdays except public holidays",
    "service_days" : {
      "dayStart" : 0,
      "dayEnd" : 5,
      "runOnPublicHoliday" : 0
    }
  },
  { 
    "from_document" : "mondays to fridays except public holidays",
    "service_days" : {
      "dayStart" : 0,
      "dayEnd" : 4,
      "runOnPublicHoliday" : 0
    }
  },
  { 
    "from_document" : "daily",
    "service_days" : {
      "dayStart" : 0,
      "dayEnd" : 6,
      "runOnPublicHoliday" : 1
    }
  }
]

def get_service_days(text: str):
  for s in service_dates:
    if str.strip(text.lower()) in s["from_document"]:
      return s["service_days"]
  return {
      "dayStart" : -1,
      "dayEnd" : -1,
      "runOnPublicHoliday" : 1
    }
