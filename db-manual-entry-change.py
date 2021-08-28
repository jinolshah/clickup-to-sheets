from db import db_retrieve, db_update

week_no = db_retrieve()

#writing data to sheets
def data_write():
    global week_no
    if week_no == 1:
        week_no += 1
        db_update(week_no)
    
    elif week_no > 1:
        if week_no == 4:
            week_no = 0
        week_no += 1
        db_update(week_no)

data_write()