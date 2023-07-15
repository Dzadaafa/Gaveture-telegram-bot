import os
import NLP.simpleNLP as simpleNLP
import NLP.robomaticAi as chatBotAI
import imgbot.img4me as txt_img
import requests as req
from io import BytesIO
from dotenv import load_dotenv
from telegram.ext import *
from telegram import InputFile

command = ['start', 'quote', 'txt', 'aimode', 'help' ]
chat_with_ai = False

load_dotenv()

tokenize = os.getenv("TELEGRAM_BOT_TOKEN")
txt_img_key = os.getenv("IMG4ME_API_KEY")
robomatic = os.getenv("ROBOMATIC_KEY")

async def start_commmand(update, context):
    await update.message.reply_text("Hello there! this is GavetureBot")


uknown_stop = 0

async def use_ai(update, context):
    global chat_with_ai
    if "yes" in update.message.text.lower():
        chat_with_ai = True
        await update.message.reply_text("Done updating!\nWhenever u said something except command, AI will answer.", reply_to_message_id=None)
    elif "no" in update.message.text.lower():
        chat_with_ai = False
        await update.message.reply_text("Done updating!\nYou're no longer texting with AI.", reply_to_message_id=None)
    else:
        await update.message.reply_text("WRONG FORMAT!\nparameter not found", reply_to_message_id=None)

async def uknown_msg(update, context):
    uMsg = update.message
    respond = ''

    if chat_with_ai:
        print("0010")
        respond = chatBotAI.chat(uMsg.chat.username, uMsg.text, robomatic)
        print("0001")
    else:
        global uknown_stop

        respond = simpleNLP.cht(uMsg.text)

    print(uMsg.chat.username, f"[{uknown_stop}]", ":", uMsg.text)
    await update.message.reply_text(respond, reply_to_message_id=uMsg.message_id)


async def quote(update, context):
    uMsg = update.message

    quotes_url = req.get(f"https://api.quotable.io/random?{uMsg}").json()
    quotes = quotes_url["content"] + "\n" + "~" + quotes_url["author"]

    image = f"https://picsum.photos/2000/1000.jpg?{uMsg.message_id}"

    await update.message.reply_photo(
        image, caption=quotes, quote=quotes, reply_to_message_id=None
    )

    # return Chat.de_json(result, self)  # type: ignore[return-value]

async def send_image_as_document(update, context):
    chat_id = update.message.chat_id
    msg = update.message.text.replace("/txt", "")
    if all(c.isspace() or not c for c in msg.split()):
        await update.message.reply_text("wrong format!")
        await update.message.reply_text('Text not found')
    else:
        image_url = txt_img.generate(msg.lstrip(), txt_img_key)
        response = req.get(image_url)

        image_file = InputFile(BytesIO(response.content), filename='image.webp')

        await context.bot.send_document(chat_id=chat_id, document=image_file)

async def help(update, context):
    UMsg = update.message
    if command[1] in UMsg.text:
         await UMsg.reply_text(f"After send the '/{command[1]}' it will return you a random image with random quote\nto use it, just send '/{command[1]}'")
    elif command[2] in UMsg.text:
         await UMsg.reply_text(f"It will turn your input text into sticker\nto use it, send '/{command[2]}' and your text after it\nexample : '/{command[2]} Test")
    elif command[3] in UMsg.text:
         await UMsg.reply_text("This command will activate the AI in conversation\n to use it, you need to mention 'on/off' after the command\nexample : '/{command[3} on")
    else:
        msg = UMsg.text.replace("help", "").replace("/", "").replace("start","")
        if all(c.isspace() or not c for c in msg.split()):
            await UMsg.reply_text(f"Hello, i will help you with the command\nBut, you may haven't mention any commands yet.\nHere's how to use /{command[4]}:")
            await UMsg.reply_text(f"/{command[4]} (command without '/')\nexample : /{command[4]} txt")
            await UMsg.reply_text("Here's the list of the commands :\nstart - start the service\nhelp - how to use\ntxt - turn text to sticker\nquote - give u random quotes\naimode - Talks with AI (Beta)")
        else:
            await UMsg.reply_text(f"Sorry, command {msg} wasn't found")

if __name__ == "__main__":
    application = Application.builder().token(tokenize).build()

    application.add_handler(CommandHandler(command[0], start_commmand))
    application.add_handler(CommandHandler(command[1], quote))
    application.add_handler(CommandHandler(command[2], send_image_as_document))
    application.add_handler(CommandHandler(command[3], use_ai))
    application.add_handler(CommandHandler(command[4], help))

    #!!!!!!!!! DON'T EVER PUT COMMAND BELLOW THIS !!!!!!!!!!#
    application.add_handler(MessageHandler(filters.TEXT, uknown_msg))

    # Run bot
    application.run_polling(1.0)
