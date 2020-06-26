from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import conf_management as ConfMgt
import schedule
import time
import menu_recipe


def start(bot, update):
    message = "Bienvenido al bot de recetas recipesbot!"
    bot.send_message(chat_id=update.message.chat_id, text=message)

def recipe(bot, update):
    """
    reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('Ver recetas', callback_data='show_recipes')],
                [InlineKeyboardButton('Receta aleatoria', callback_data='random_recipe')],
                [InlineKeyboardButton('Cancelar', callback_data='cancel')]
            ]
        )
    """
    reply_markup = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('Ver recetas', callback_data='show_recipes'),
                    InlineKeyboardButton('Receta aleatoria', callback_data='random_recipe')],
                [InlineKeyboardButton('Adulto comida aleatoria', callback_data='adult_random_lunch'),
                    InlineKeyboardButton('Adulto cena aleatoria', callback_data='adult_random_dinner')],
                [InlineKeyboardButton('Niña comida aleatoria', callback_data='kid_random_lunch'),
                    InlineKeyboardButton('Niña cena aleatoria', callback_data='kid_random_dinner')],
                [InlineKeyboardButton('Cancelar', callback_data='cancel')]
            ]
        )

    bot.send_message(
        chat_id=update.message.chat_id,
        text='¿Qué quieres hacer?',
        reply_markup=reply_markup
        )


def button(bot, update):
    bot.deleteMessage(
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id
        )

    txt_result = ''

    if update.callback_query.data == 'show_recipes':
        txt_result = menu_recipe.Recipe.get_text_recipes()
    elif update.callback_query.data == 'cancel':
        txt_result = 'OK'
    elif update.callback_query.data == 'random_recipe':
        txt_result = menu_recipe.Recipe.get_random_recipe()
    elif update.callback_query.data == 'adult_random_lunch':
        txt_result = menu_recipe.Recipe.get_random_recipe_filtered(is_lunch=True,for_adult=True)
    elif update.callback_query.data == 'adult_random_dinner':
        txt_result = menu_recipe.Recipe.get_random_recipe_filtered(is_dinner=True,for_adult=True)
    elif update.callback_query.data == 'kid_random_lunch':
        txt_result = menu_recipe.Recipe.get_random_recipe_filtered(is_lunch=True,for_kids=True)
    elif update.callback_query.data == 'kid_random_dinner':
        txt_result = menu_recipe.Recipe.get_random_recipe_filtered(is_dinner=True,for_kids=True)

    bot.send_message(
        chat_id=update.callback_query.message.chat_id,
        text=txt_result
        )


def main(bot_token):
    """ Main function of the bot """
    updater = Updater(token=bot_token)
    dispatcher = updater.dispatcher

    # Query handler
    query_handler = CallbackQueryHandler(button)
    dispatcher.add_handler(query_handler)

    # Command handlers
    start_handler = CommandHandler('start', start)
    recipe_handler = CommandHandler('recipe', recipe)

    # Add the handlers to the bot
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(recipe_handler)

    # Starting the bot
    updater.start_polling()
    print('recipesbot configured')


def send_telegram(bot_token, id_chat, texto_send):
    update = Updater(token=bot_token)
    update.bot.send_message(chat_id=id_chat, text=texto_send)


if __name__ == "__main__":
    main(ConfMgt.get_telegram_token())

    while True:
        schedule.run_pending()
        time.sleep(1)
        print('recipesbot is running...')
