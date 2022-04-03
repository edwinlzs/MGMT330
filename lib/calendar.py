from telegram import Bot, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date
import pandas as pd
import numpy as np
from os.path import exists

def start_calendar(bot: Bot, chat_id: int, min_date: date, max_date: date):
  calendar, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date).build()
  bot.send_message(
    chat_id=chat_id,
    text=f"Select {LSTEP[step]}",
    reply_markup=calendar
  )

def handle_calendar(bot: Bot, query: CallbackQuery):
  # selected timeslot
  if ('selected' in query.data):
    details = query.data.split('_')
    selected_date = details[2]
    selected_timeslot = details[3]
    selected_year = selected_date.split('/')[2]

    filename = f'./data/schedule/{selected_year}.csv'
    schedule_df = pd.read_csv(filename, index_col=0)
    schedule_df.loc[selected_date, selected_timeslot] = query.message.chat.username
    schedule_df.to_csv(filename)

    bot.edit_message_text(f"You have selected {selected_timeslot} on {selected_date}.\n\n"\
                          "We look forward to seeing you!",
                            query.message.chat.id,
                            query.message.message_id)
    
  # still selecting stuff
  else:
    result, key, step = DetailedTelegramCalendar().process(query.data)
    if not result and key:
      bot.edit_message_text(f"Select {LSTEP[step]}",
                            query.message.chat.id,
                            query.message.message_id,
                            reply_markup=key)
    elif result:
      filename = f'./data/schedule/{result.year}.csv'
      
      if exists(filename):
        schedule_df = pd.read_csv(filename, index_col=0)
      else:
        dates_index = pd.date_range(start=date(result.year, 1, 1), end=date(result.year, 12, 31), freq='D')
        timeslots = ['10:00 AM - 10:30 AM', '10:30 AM - 11:00 AM', '11:00 AM - 11:30 AM',
                      '12:30 PM - 1:00 PM', '1:00 PM - 1:30 PM', '1:30 PM - 2:00 PM', '2:00 PM - 2:30 PM',
                      '2:30 PM - 3:00 PM']
        schedule_df = pd.DataFrame(index=dates_index, columns=timeslots)
        schedule_df.to_csv(filename)

      selected_date = f'{result.day}/{result.month}/{result.year}'
      schedule_selected = schedule_df.loc[selected_date]
      
      free_slots = [x for x in schedule_selected[schedule_selected.isna()].index]
      markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(free_slot, callback_data=f'cbcal_selected_{selected_date}_{free_slot}')] for free_slot in free_slots]
      )

      bot.edit_message_text(f"Select consultation slot",
                            query.message.chat.id,
                            query.message.message_id,
                            reply_markup=markup)

    
