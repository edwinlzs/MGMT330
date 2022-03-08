from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update, User
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Filters, MessageHandler, Updater
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
import logging
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

bot = Bot(token='5254310301:AAFpjmHpHHKNa_QH94L_Ey0lBOK6e5BfpuA')

updater = Updater(token='5254310301:AAFpjmHpHHKNa_QH94L_Ey0lBOK6e5BfpuA', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
  user = update.message.from_user
  context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello, {user['first_name']}!")

  with open("message_logs/message_logs.txt", "a") as f:
    timestamp  = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    username = update.effective_user.username
    f.write(f"{timestamp}: user [{username}] initialized with /start \n")

  keyboard = [
      [
          InlineKeyboardButton("Confinement Plan", callback_data='confinement'),
          InlineKeyboardButton("Subscription Plan", callback_data='subscription'),
      ],
      [
        InlineKeyboardButton("Shop on our Website", url='https://hengfohtong.com/shop/products/'),
      ],
      [
        InlineKeyboardButton("Book a Consultation", callback_data='book'),
      ],
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)

  update.message.reply_text(
    'Welcome to Heng Foh Tong\'s Test Bot.\n\n'\
    'What would you like to do today?',
    reply_markup=reply_markup
  )

def handleCalendar(c):
  result, key, step = DetailedTelegramCalendar().process(c.data)
  if not result and key:
    bot.edit_message_text(f"Select {LSTEP[step]}",
                          c.message.chat.id,
                          c.message.message_id,
                          reply_markup=key)
  elif result:
    bot.edit_message_text(f"You selected {result}",
                          c.message.chat.id,
                          c.message.message_id)

def maintenance_message(update: Update, context: CallbackContext):
  with open("message_logs/message_logs.txt", "a") as f:
    timestamp  = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    username = update.effective_user.username
    f.write(f"{timestamp}: [{username}] {update.message.text}\n")

  context.bot.send_message(
    chat_id=update.effective_chat.id,
    text="This bot is not ready to respond to manual questions yet, please use /start and test the buttons first"
  )

def button(update: Update, context: CallbackContext) -> None:
  query = update.callback_query
  query.answer()
  chat_id = update.effective_chat.id

  with open("message_logs/message_logs.txt", "a") as f:
    timestamp  = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    username = update.effective_user.username
    f.write(f"{timestamp}: [{username}] clicked on button: {query.data} \n")

  if query.data == 'confinement':
    context.bot.send_message(
      chat_id=chat_id,
      text='Today on your confinement plan, you need to consume Herb ABC'
    )
  elif query.data == 'subscription':
    context.bot.send_message(
      chat_id=chat_id,
      text='Your current subscription plan consists of the following items:\n'\
      '1. Herb ABC - this supplements your energy\n'\
      '2. Herb BCD - this helps you stay beautiful\n'\
      '3. Herb CDE - this boosts your immunity\n'\
    )
  elif query.data == 'book':
    min_date = date.today()
    max_date = min_date + relativedelta(years=3)
    calendar, step = DetailedTelegramCalendar(min_date=min_date, max_date=max_date).build()
    context.bot.send_message(
      chat_id=chat_id,
      text=f"Select {LSTEP[step]}",
      reply_markup=calendar
    )
  elif query.data.startswith('cbcal'):
    handleCalendar(query)

message_handler = MessageHandler(Filters.text & (~Filters.command), maintenance_message)

dispatcher.add_handler(message_handler)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
updater.idle()