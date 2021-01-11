import os
from pytimeparse import parse
import ptbot


def notify():
    bot.send_message(TELEGRAM_CHAT_ID, 'Время вышло!')


def reply(text):
    seconds = parse(text)
    message_id = bot.send_message(
        TELEGRAM_CHAT_ID,
        f'Таймер запущен на {seconds} секунд!'
    )
    bot.create_countdown(
        seconds, notify_progress,
        message_id=message_id,
        total_seconds=seconds
    )
    bot.create_timer(seconds, notify)


def notify_progress(secs_left, message_id, total_seconds):
    str_progressbar = render_progressbar(total_seconds, secs_left)
    bot.update_message(
        TELEGRAM_CHAT_ID,
        message_id,
        f'Осталось секунд: {secs_left} \n {str_progressbar}'
    )


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = ptbot.Bot(TELEGRAM_TOKEN)

bot.send_message(TELEGRAM_CHAT_ID, 'На сколько запустить таймер?')
bot.reply_on_message(reply)
bot.run_bot()
