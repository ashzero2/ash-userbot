from pyrogram import Client, filters
from pyrogram.types import Message
from search_engine_parser import GoogleSearch
from utils import nekobin
from utils import formatter
import time
from googletrans import Translator, constants
from pprint import pprint
import requests

app = Client("user_name", api_id=, api_hash="")

startup = time.time()

@app.on_message(filters.command(['lazy']) & filters.user("user_name"))
async def hello(client, message):
    bot_uptime = int(time.time() - startup)
    await message.reply_text(f"TF ! I said dont distrub me, I'm already active for {formatter.get_readable_time((bot_uptime))}")

@app.on_message(filters.command(['up']) & filters.user("user_name"))
async def uptime(client, message):
    bot_uptime = int(time.time() - startup)
    await message.reply_text(
        f"Aww!! I think I'm alive for {formatter.get_readable_time((bot_uptime))}")

@app.on_message(filters.command(['google']) & filters.user("user_name"))
async def google(_, message: Message):
    text = message.text.replace("/google ", '')
    if text != '':
        gresults = await GoogleSearch().async_search(text, 1)
        result = ""
        for i in range(3):
            try:
                title = gresults["titles"][i].replace("\n", " ")
                source = gresults["links"][i]
                description = gresults["descriptions"][i]
                result += f"[{i+1} : {title}]({source})\n"
                result += f"`{description}`\n\n"
            except IndexError:
                pass
        await message.reply_text(result, disable_web_page_preview=True)
    else:
        await message.reply_text('"/google" Needs An Argument')

@app.on_message(filters.command(['ping']) & filters.user("user_name"))
async def ping(_, message: Message):
    app.set_parse_mode("markdown")
    m = await message.reply_text("Pls wait Baka . . .")
    result = ""
    for i in range(1, 6):
        datacenter = (f"https://cdn{i}.telesco.pe")
        ping1 = round(requests.head(datacenter).elapsed.total_seconds() * 1000)
        if i != message.from_user.dc_id:
            result += f"DC{i} - {ping1}ms\n"
        else:
            result += f"DC{i} - {ping1}ms [  I'm Here! ]\n"
        await m.edit(result)

@app.on_message(filters.command(['paste']) & filters.user("user_name"))
async def paste(_, message: Message):
    if bool(message.reply_to_message) is True:
        app.set_parse_mode("markdown")
        if bool(message.reply_to_message.text) is True:
            m = await message.reply_text("```Pasting To Nekobin...```")
            message_get = message.reply_to_message.text
            message_as_str = str(message_get)
            paste_link = await nekobin.neko(message_as_str)
            final_link = f"[Nekobin]({paste_link})"
            await m.edit(final_link, disable_web_page_preview=True)

        elif bool(message.reply_to_message.document) is True:
            m = await message.reply_text("```Pasting To Nekobin...```")
            await message.reply_to_message.download(file_name='paste.txt')
            i = open("downloads/paste.txt", "r")
            paste_link = await nekobin.neko(i.read())
            os.remove('downloads/paste.txt')
            final_link = f"[Nekobin]({paste_link})"
            await m.edit(final_link, disable_web_page_preview=True)
    elif bool(message.reply_to_message) is False:
        await message.reply_text(
            "Reply To A Message With /paste, Just Hitting /paste "
            + "Won't Do Anything Other Than Proving Everyone That "
            + "You Are A Spammer Who Is Obsessed To 'BlueTextMustClickofobia")

@app.on_message(filters.command(['en']) & filters.user("user_name"))
async def trans(_, message: Message):
    translator = Translator()
    text_tr = message.reply_to_message.text
    tr_word = translator.translate(text_tr)
    await message.reply_text(f"{tr_word.text}({tr_word.src})")

@app.on_message(filters.command(['spam']) & filters.user("user_name"))
async def spam(_, message: Message):
    text = message.text.replace("/spam ", '')
    for i in text:
        await message.reply_text(i)

app.run()
