from telegram import Bot, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

def learn(bot: Bot, query: CallbackQuery):

  action = query.data.split('_')[1]

  if action == 'start':
    keyboard = [
      [
        InlineKeyboardButton("Beauty", callback_data='learn_beauty'),
      ],
      [
        InlineKeyboardButton("Confinement", callback_data='learn_confinement'),
      ],
      [
        InlineKeyboardButton("Vitality", callback_data='learn_vitality'),
      ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(f"What topic would you like to learn more about?",
                            query.message.chat.id,
                            query.message.message_id,
                            reply_markup=reply_markup)

  elif action == 'beauty':
    keyboard = [
      [
        InlineKeyboardButton("Honey Peach Gum and Its Benefits",
        url='https://hengfohtong.com/post_articles/honey-peach-gum-and-its-benefits/'),
      ],
      [
        InlineKeyboardButton("Top 5 Tips to Get Ready for Chinese New Year",
        url='https://hengfohtong.com/post_articles/top-5-tips-to-get-your-skin-and-body-ready-for-chinese-new-year/'),
      ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(f"What topic would you like to learn more about?",
                            query.message.chat.id,
                            query.message.message_id,
                            reply_markup=reply_markup)
      