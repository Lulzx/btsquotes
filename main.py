#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from logzero import logger

from telegram import ParseMode
from telegram.ext import CommandHandler, Updater


facts = []
f = open('facts.txt', mode='r')
fact_lines = f.readlines()
f.close()

for fact in fact_lines:
    facts += [fact]


def start(update, context):
    update.message.reply_text('Hi! Send /fact to get a fact about BTS.')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def send_help(update, context):
    chat_id = update.message.chat_id
    logger.info('Sending help...')
    context.bot.sendMessage(
        chat_id,
        'Get the hottest BTS fact delivered right to your inbox with /fact!',
        parse_mode=ParseMode.MARKDOWN)


def get_random_fact():
    return random.choice(facts)


def send_fact(update, context):
    chat_id = update.message.chat_id
    fact = get_random_fact()
    logger.info("Sending fact to " + str(chat_id) + ": " + fact)
    context.bot.sendMessage(chat_id, fact)


def main():
    token = "766781853:AAEKZI2OgZS2dmGJvJN2HyqHC7yvK_IK3OE"

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fact", send_fact))
    dp.add_handler(CommandHandler("help", send_help))

    dp.add_error_handler(error)

    logger.info('Listening...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
