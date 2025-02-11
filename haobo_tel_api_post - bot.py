import logging
import re
import requests
import json
import pytesseract
try:
    from PIL import Image
except ImportError:
    import Image
from telegram import Update
from telegram.ext import filters,ApplicationBuilder, ContextTypes, CommandHandler,MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Hello,{update.effective_user.username}, , Welcome to CHECK PCID!  \n 👤 ID: <tg-spoiler>{update.effective_user.id}</tg-spoiler>",parse_mode='HTML')

async def transfer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
       iid = "".join(re.findall("\\d+", update.message.text))
       d2 = "".join(re.findall("\\w+", update.message.text))
       if len(d2) == 25:
           await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=f'Received {update.effective_user.first_name}request.key:{d2}')
           url1 = "https://api.f753.com/api_pid"

           data = {'key': d2,
                   'tid': '5639210447',
                   'api': '10d7d215-ccd2-4dc2-9690-577ee9cd30d3'
                   }
           key = requests.post(url1, data=data)
           reply_key = "KEY:{}\nVersion:{}\nKEYstate:{}\nonline:{}\nPrompt code2:{}\nTIME:{}".format(
               key.json()['data_key']['key'], key.json()['data_key']['Version'], key.json()['data_key']['KEYstate'],
               key.json()['data_key']['online'], key.json()['data_key']['Prompt code2:'], key.json()['data_key']['TIME'])
           await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{reply_key}')
       elif len(iid) == 63 or len(iid) == 54:
           await context.bot.send_message(chat_id=update.effective_chat.id,text=f'receive {update.effective_user.first_name} Request iid:{iid}')
           url1 = "https://api.haobo.org/api_get"
           data = {'id': iid,
                   'tid': '5639210447',
                   'tuser': 'marksell99',
                   'api': '10d7d215-ccd2-4dc2-9690-577ee9cd30d3'
                   }
           cid = requests.post(url1, data=data)
           cids = f"IID:{cid.json()['cid_data']['IID:']}\nCID:{cid.json()['cid_data']['CID:']}"
           await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{cids}')
       else:
           pass
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        print(file_id)
        the_file = await context.bot.get_file(file_id)
        print(the_file)
        response = requests.get(the_file.file_path)
        if response.status_code == 200:
           with open('local_image2.jpg', 'wb') as f:
               # 写入获取到的内容
               f.write(response.content)
        else:
            pass
        xx = re.findall("\\d+", pytesseract.image_to_string(Image.open('local_image2.jpg',)))
        list_Img = []
        for x in xx:
            if len(x) == 6 or len(x) == 7:
                list_Img.append(x)

        x1 = "".join(list_Img)
        if len(x1) == 63 or len(x1) == 54:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=f'Received {update.effective_user.first_name}Request:{x1}')

            url1 = "https://api.haobo.org/api_get"
            data = {'id': x1,
                    'tid': '5639210447',
                    'tuser': 'marksell99',
                    'api': '10d7d215-ccd2-4dc2-9690-577ee9cd30d3'
                    }
            cid = requests.post(url1, data=data)
            cids = f"IID:{cid.json()['cid_data']['IID:']}\nCID:{cid.json()['cid_data']['CID:']}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'{cids}')
        else:
            pass





if __name__ == '__main__':
    application = ApplicationBuilder().token('7772833621:AAGujRcShWwg7WgOMDu1pv7cWfROsj_US7I').build()
    transfer_handler = MessageHandler((~filters.COMMAND), transfer)
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(transfer_handler)
    application.run_polling()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
