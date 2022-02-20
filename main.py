from telethon import events
import os
from config import bot
from FastTelethonhelper import fast_download, fast_upload

is_busy = False


@bot.on(events.NewMessage(pattern=("/start")))
async def start(event):
    if event.text == '/start' or event.text == '/start@Kujo_Jotaro_Robot':
        await bot.send_message(event.chat_id, "Im Running")


@bot.on(events.NewMessage(pattern=("/rename")))
async def rename(event):
    global is_busy
    if is_busy == True:
        await event.reply("Im Busy with another process, try again later")
        return
    is_busy == True
    reply = await bot.send_message(event.chat_id, "Downloading") 
    try:
        name = event.raw_text.split()
        name.pop(0)
        name = " ".join(name)
        msg = await event.get_reply_message()
        download_location = await fast_download(bot, msg, reply=reply, download_folder='./downloads/')
        file = await fast_upload(client=bot, reply=reply, file_location=download_location, name=name)
        await bot.send_message(event.chat_id, file=file, thumb="thumb.png", force_document=True)
        await reply.delete()
        os.remove(download_location)

    except Exception as e:
        await event.reply(str(e))

    finally:
        is_busy == False


@bot.on(events.NewMessage(pattern=("/magic")))
async def batch_rename(event):
    global is_busy
    if is_busy == True:
        await event.reply("Im Busy with another process, try again later")
        return
    is_busy == True
    data = event.text.split(":")
    files = []
    try:
        for i in range(int(data[1]),int(data[2])+1):
            x = await bot.get_messages(event.chat_id, ids=i)
            if x is not None:
                files.append(x)
        a = int(data[4])
        for i in range(len(files)):
            name = data[3]
            if a<10:
                temp = name.replace("OwO", f"00{a}")
                temp = temp.replace("UwU", f"0{a}")

            elif a<100:
                temp = name.replace("OwO", f"0{a}")
                temp = temp.replace("UwU", f"{a}")

            else:
                temp = name.replace("OwO", f"{a}")

            reply = await files[i].reply("Downloading...")
            download_location = await fast_download(bot, files[i], reply)
            file = await fast_upload(client=bot, reply=reply, file_location=download_location, name=temp)
            await bot.send_message(event.chat_id, file=file, thumb="thumb.png", force_document=True)
            a = a+1
            await reply.delete()
            os.remove(download_location)

    except Exception as e:
        await event.reply(e)
    
    finally:
        is_busy == False


@bot.on(events.NewMessage(pattern=("/sthumb")))
async def thumb(event):
    x = await event.get_reply_message()
    thumb = await bot.download_media(x.photo)
    with open(thumb, "rb") as f:
        pic = f.read()
    with open("thumb.png", "wb") as f:
        f.write(pic)
    await event.reply("Set as default thumbnail")


@bot.on(events.NewMessage(pattern=("/cthumb")))
async def clear_thumb(event):
    with open("thumb.png", "w") as f:
        f.write("")
    await event.reply("cleared thumbnail")


@bot.on(events.NewMessage(pattern=("/vthumb")))
async def view(event):
    try:
        await event.reply("current default thumbnail", file="thumb.png")
    except:
        await event.reply("No default thumbnail set")


@bot.on(events.NewMessage(pattern=("/msgid")))
async def msgid(event):
    x = await event.get_reply_message()
    await x.reply(f"Message id: `{x.id}`")


bot.start()

bot.run_until_disconnected()
