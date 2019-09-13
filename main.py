#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

__version__ = "1.0.0"
import logging
import random
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, ParseMode
from telegram.ext import CommandHandler, InlineQueryHandler, Updater

from util import levenshteinDistance as distance

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


class Facts(object):
    def __init__(self):
        self.facts = []
        self.load_facts()

    def load_facts(self):
        f = open('facts.txt', mode='r')
        fact_lines = f.readlines()
        f.close()

        for fact in fact_lines:
            self.facts += [fact]

    def get_facts(self):
        return self.facts


all_facts = Facts()


def start(update, context):
    update.message.reply_text('Hi! Send /fact to get a fact about BTS.')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def send_help(update, context):
    chat_id = update.message.chat_id
    logging.info('Sending help...')
    context.bot.sendMessage(
        chat_id,
        'Get the hottest BTS fact delivered right to your inbox with /fact!',
        parse_mode=ParseMode.MARKDOWN)


def get_random_fact():
    return random.choice(all_facts.get_facts())


def send_fact(update, context):
    chat_id = update.message.chat_id
    fact = get_random_fact()
    logging.info("Sending fact to " + str(chat_id) + ": " + fact)
    context.bot.sendMessage(chat_id, fact)


def inlinequery(update, context):
    logging.info('Answering inline query')
    query = update.inline_query.query
    results_list = list()

    facts = all_facts.get_facts()
    search_results = [
        f for f in facts
        if distance(query, f, ignore_case=True) < 3 or query.lower() in f.lower()
    ]

    if len(search_results) > 0:
        facts = search_results[0:49]
    else:
        # 50 random facts
        range_start = random.randint(0, len(facts))
        facts = facts[range_start:range_start + 49]
        results_list.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title="No search results for '{}'.".format(query),
                input_message_content=InputTextMessageContent(
                    message_text=get_random_fact()),
                description='Use a random fact below'))

    for fact in facts:
        results_list.append(
            InlineQueryResultArticle(
                id=uuid4(),
                title='BTS Fact',
                input_message_content=InputTextMessageContent(
                    message_text=fact),
                description=fact))

    context.bot.answerInlineQuery(update.inline_query.id, results=results_list)


def main():
    token = "766781853:AAEKZI2OgZS2dmGJvJN2HyqHC7yvK_IK3OE"

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(InlineQueryHandler(inlinequery))

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fact", send_fact))
    dp.add_handler(CommandHandler("help", send_help))

    dp.add_error_handler(error)

    print('Listening...')
    logging.info('Listening...')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
