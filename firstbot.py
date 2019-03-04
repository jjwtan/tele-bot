from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging
import requests
import json

logger = logging.getLogger(__name__)
logging.basicConfig(filename='bot.log',level=logging.INFO)

def start(bot, update):
    logger.info("start")
    chat_id = update.message.chat_id
    logger.info(update.message)
    user = str(update.message.from_user.username)
    welcome_text = "Hellooo " + user + "! I am bot"
    bot.send_message(chat_id=chat_id, text=welcome_text)
    bot.send_message(chat_id=189857418, text= user + " started")

def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def get_address(pcode):
    try:
        response = requests.get('http://developers.onemap.sg/commonapi/search?searchVal=' + pcode + '&returnGeom=Y&getAddrDetails=Y&pageNum=1').text
        result = json.loads(response)
        return result["results"][0]["ADDRESS"]
    except:
        logger.error('Fetching {} failed.'.format(pcode))


def all_message(bot, update):
    from_ = update.message.from_user.username
    text = update.message.text

    address = get_address(text)
    if address is None:
        address = "Invalid postal code"
    if from_ is None:
        from_ = update.message.from_user.first_name
    bot.send_message(chat_id=update.message.chat_id, text=address)
    bot.send_message(chat_id=189857418, text=str(from_)+": " + text)

def main():
    updater = Updater("")
    dp = updater.dispatcher

    start_handler = CommandHandler("start", start)
    command_handler = MessageHandler(Filters.command, all_message)
    text_handler = MessageHandler(Filters.text, all_message)
    dp.add_handler(start_handler)
    dp.add_handler(command_handler)
    dp.add_handler(text_handler)

    logger.info("start polling")
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()