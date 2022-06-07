# Sun Ferry Timetables to JSON

Sun Ferry Services Company Limited provides their timetable data in CSV format on data.gov.hk [link](https://data.gov.hk/en-datasets/provider/sunferry).

Started this project to convert the English timetable data into JSON.

The CSVs references a set of Remarks for each route that is not included in the CSV but are defined in their data spec document. These were manually written in JSON format to be used in the module.

## Requirements

Download the CSV timetables from the dataset offered by them and put in ```sunferry_timetables``` directory.

To run  
```python parseCsvTimetables.py```

## Result

JSON for each schedule is as follows:

```js
{
    "routes": [
        {
            "routeCode"
            "origin"
            "destination"
            "departures": [
                {
                    "dayStart"
                    "dayEnd"
                    "runOnPublicHoliday"
                    "serviceDaysString"
                    "serviceTimes": [
                        {
                            "time"
                            "remark"
                        }
                    ]
                }
            ]
        }
    ],
    "remarks": [
        {
            "code"
            "remark"
        }
    ]
}
```

```routeCode``` - Code used for the routes, can be used in ETA API calls
```routeName``` - ```origin``` to ```destination```
```origin``` - Where route begins
```destination``` - Where route ends
```departures``` - List of departures
```dayStart``` - Starting day of the week (0 = Sunday) for this schedule
```dayEnd``` - Ending day of the week (0 = Sunday) for this schedule
```runOnPublicHoliday``` - If schedule applies on a Public Holiday
```serviceDaysString``` - String from the CSV file
```serviceTimes``` - List of departures and any special remarks for that departure
```code``` - Remark code
```remark``` - Remark Text

### Notes

- Parsed Data is in English only since the provided data dictionaries are in English.

- Service Dates are determined by matching text that is in the "Service Date" column of the CSVs. It is not the most reliable since they might change the text in the future, but they don't define it any other way in their documentation.

- Fare tables are not included but should be straightforward to implement.