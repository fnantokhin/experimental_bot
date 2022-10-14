#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
bot ver 0.11

The project is based of https://habr.com/ru/post/341678/
This bot is based of https://github.com/python-telegram-bot/
python-telegram-bot/blob/master/examples/echobot.py
(using python-telegram-bot)

my_homepc surveillance monitor telegram bot

This bot is meant as a part of an exercise pet project that
performs functions of a home monitor. The project goal is to
use an old notebook repurposed as an experimental debian bullseye
server to utilise https://motion-project.github.io/ to setup
automatic webcam capture and motion detection for no hassle
"video monitoring" of some area e.g. my studio appartment.
python-telegram-bot.org is used to build telegram bot, that will
be acting as a remote front end and will run on an experimental
debian bullseye server.

Usage:
/start
/debug
/help
TO_DO /update x
"""

import logging

from telegram import Update
from telegram.ext import ApplicationHandlerStop, Application
from telegram.ext import TypeHandler, CommandHandler, ContextTypes
import custom_config

# Enable logging
logging.basicConfig(
    format=(
        "%(asctime)s - %(name)s - %(levelname)s -"
        "%(message)s"), level=logging.INFO
)
logger = logging.getLogger(__name__)


async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Block bot for non AUTHENTICATED USERS"""
    if update.effective_user.id in custom_config.SPECIAL_USERS:
        pass
    else:
        """Print back user id"""
        await update.message.reply_text(update.effective_user.id)
        raise ApplicationHandlerStop

# Define a few command handlers. These usually take the two arguments update
# and context.


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) \
      -> None:
    """Send a message when the command /start is issued."""
    # user = update.effective_user
    await update.message.reply_text("homewebcamssurveillance_9581_bot start()")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) \
      -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Usage:\n"
        "/debug - send last snapshot made by motion "
        "program and last motion capture video recorded\n"
        "/help - send this message")


async def debug_command(update: Update, context: ContextTypes.DEFAULT_TYPE) \
      -> None:
    await update.message.reply_photo(open(custom_config.CURRENT_PHOTO, 'rb'))
    await update.message.reply_video(open(custom_config.CURRENT_VIDEO, 'rb'))


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(custom_config.BOT_TOKEN).build()

    # before anything else assess if the current user is
    # in the SPECIAL_USERS constant
    application.add_handler(TypeHandler(Update, callback), -1)
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("debug", debug_command))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
