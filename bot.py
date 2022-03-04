from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, Updater
import logging

bot = Bot(token='5254310301:AAFpjmHpHHKNa_QH94L_Ey0lBOK6e5BfpuA')

updater = Updater(token='5254310301:AAFpjmHpHHKNa_QH94L_Ey0lBOK6e5BfpuA', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
  context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to HFT Test Bot!")

  keyboard = [
      [
          InlineKeyboardButton("Option 1", callback_data='1'),
          InlineKeyboardButton("Option 2", callback_data='2'),
      ],
      [InlineKeyboardButton("Option 3", callback_data='3')],
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)

  update.message.reply_text('Please choose:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
  query = update.callback_query

  query.answer()

  query.edit_message_text(text=f"Select Option: {query.data}")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CallbackQueryHandler(button))
# dispatcher.add_handler(CommandHandler('help', help_command))

updater.start_polling()
updater.idle()