#!/usr/bin python3
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
from commands import Commands
import time
import platform
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def error(bot, update, error):
    '''Log Errors caused by Updates.'''
    logger.warning('Update "%s" caused error "%s"', update, error)

if __name__ == '__main__':
    '''Start the bot.'''
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ['UNISWAP_BOT_TOKEN'], workers=10)

    # Get the dispatcher to register handlers
    commands = Commands()
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', commands.start))
    dp.add_handler(CommandHandler('coin', commands.coin, pass_args=True))
    dp.add_handler(CommandHandler('help', commands.help))
    dp.add_handler(CommandHandler('about', commands.about))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    print('Bot is running')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()
