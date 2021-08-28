import json
import sheets
import clickup
from db import db_retrieve, db_update

first_row = ["Client", "Rate", "Available Hours", "Week 1", "Week 2", "Week 3", "Week 4", "Time Tracked This Month"]

# setting week number
week_no = db_retrieve()

#writing data to sheets
def data_write():
    global week_no
    work = clickup.clickup_data()
    if week_no == 1:
        sheets_existing = sheets.gsheet_names()
        for key, value in work.items():
            if value['name'] not in sheets_existing:
             sheets.add_sheet(value['name'])
            elif value['name'] in sheets_existing:
                sheets.clear_sheet(value['name'])

        for person, values in work.items():
            matrix = [first_row]
            i = 1
            for task in values['tasks']:
                i += 1
                matrix.append([task['name'], task['rate'], task['available hours'], int(task['hours logged'])/3600000,
                             '', '', '', f'=SUM(D{i}:G{i})'])
            sheets.write_sheets(values['name'], matrix)
        week_no += 1
        db_update(week_no)
    
    elif week_no > 1:
        for key, value in work.items():
            sheet_val = sheets.values_get(value['name'])
            for task in value['tasks']:          # adding tasks if not in list
                for sheet_tasks in sheet_val:
                    if task['name'] == sheet_tasks[0]:
                        is_there = True
                        break
                    else:
                        is_there = False
                if not is_there:
                    sheet_val.append([task['name'], task['rate'], task['available hours'], '',
                             '', '', '', 'sum'])
            for task in value['tasks']:
                k = 0
                for sheet_tasks in sheet_val:
                    k += 1
                    if task['name'] == sheet_tasks[0]:
                        sheet_tasks[2 + week_no] = int(task['hours logged'])/3600000
                        sheet_tasks[7] = f'=SUM(D{k}:G{k})'
                        break
                    else:
                        continue
            sheets.write_sheets(value['name'], sheet_val)
        if week_no == 4:
            week_no = 0
        week_no += 1
        db_update(week_no)