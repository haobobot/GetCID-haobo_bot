import logging
import re
import requests
from telegram import Update
from telegram.ext import filters,ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
       iid = "".join(re.findall("\\d+", update.message.text))
       if len(iid) == 63 or len(iid) == 54:
           await context.bot.send_message(chat_id=update.effective_chat.id,text=f'receive {update.effective_user.first_name} Request iid:{iid}')
           url = 'https://api.haobo.org/api_get?id={}&tid={}&tuser={}&api={}'.format(iid,"YOUID","None",'API')
           getiid = requests.get(url)
           await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{getiid.text}')
       else:
           cid_message = "The number of iIDs is incorrect, please check."
           await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{cid_message}')





if __name__ == '__main__':
    application = ApplicationBuilder().token('your token').build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
