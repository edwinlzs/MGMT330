import sched
import pandas as pd
import numpy as np
from datetime import datetime, date

today = date.today()
filename = f'./data/schedule/{today.year}.csv'
# dates_index = pd.date_range(start=date(today.year, 1, 1), end=date(today.year, 12, 31), freq='D')
# timeslots = ['10:00 AM - 10:30 AM', '10:30 AM - 11:00 AM', '11:00 AM - 11:30 AM',
#               '12:30 PM - 1:00 PM', '1:00 PM - 1:30 PM', '1:30 PM - 2:00 PM', '2:00 PM - 2:30 PM',
#               '2:30 PM - 3:00 PM']
# schedule_df = pd.DataFrame(index=dates_index, columns=timeslots)
# schedule_df.to_csv(filename)

schedule_df = pd.read_csv(filename, index_col=0)
schedule_today = schedule_df.loc[f'{today.day}/{today.month}/{today.year}']

free_slots = [x for x in schedule_today[schedule_today.isna()].index]
print(free_slots)