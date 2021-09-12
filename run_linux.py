from subprocess import check_output
from time import sleep
import os
import settings
from datetime import datetime


while True:
    print(settings.sqlite_file)
    try:
        while True:
            os.system('python3 main.py')
            print('Бот перезапущен. Время: {}'.format(datetime.now()))

        sleep(2)
    except KeyboardInterrupt:
        break
