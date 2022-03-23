from telegram import Bot, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date
import pandas as pd
from os.path import exists

def start_calendar(bot: Bot, chat_id: int, min_date: date, max_date: date):
  calendar, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date).build()
  bot.send_message(
    chat_id=chat_id,
    text=f"Select {LSTEP[step]}",
    reply_markup=calendar
  )

def handle_calendar(bot: Bot, query: CallbackQuery):
  result, key, step = DetailedTelegramCalendar().process(query.data)
  if not result and key:
    bot.edit_message_text(f"Select {LSTEP[step]}",
                          query.message.chat.id,
                          query.message.message_id,
                          reply_markup=key)
  elif result:
    today = date.today()
    filename = f'{today.year}.csv'
    if exists(filename):
      schedule_df = pd.read_csv(filename)
      schedule_today = schedule_df[today]
    else:
      dates_index = pd.date_range(start=date(today.year, 1, 1), end=date(today.year, 12, 31), freq='D')
      timeslots = ['10:00 AM - 10:30 AM', '10:30 AM - 11:00 AM', '11:00 AM - 11:30 AM',
                    '12:30 PM - 1:00 PM', '1:00 PM - 1:30 PM', '1:30 PM - 2:00 PM', '2:00 PM - 2:30 PM'
                    '2:30 PM - 3:00 PM']