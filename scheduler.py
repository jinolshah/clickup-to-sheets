import schedule
import time
import main

schedule.every().monday.at("06:00").do(main.data_write)

while True:
    schedule.run_pending()
    time.sleep(31)