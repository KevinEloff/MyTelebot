import logging
import time
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import json 
from vars import knowntext, grouptext
from replyhandler import getPrivateReply
from botdata import password, TOKEN
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

##  VARIABLES  ##

##  CHAT FUNCTIONS  ##
def private_msg(bot, update):
    logging.info("{}: {}".format(update.message.chat.first_name, update.message.text))
    addChat(update)
    reply = getPrivateReply(update.message.text)
    if reply != None:
        if reply != None:
            if '[sticker]' in reply:
                data = readJson('chatdata.json').get("stickers")
                
                stickers = []

                if len(reply.split()) == 3:
                    for sticker in data:
                        if sticker["emoji"] == reply.split()[2]:
                            stickers.append(sticker)
                else:
                    stickers = data
                
                if (len(stickers) < 1):
                    bot.send_message(chat_id=update.message.chat_id, text="I don't have any stickers like that yet!")
                    return

                # logging.info(reply)
                for n in range(0, int(reply.split()[1])):
                    i = random.randint(0, len(stickers)-1)
                    # logging.info("{} => {}".format(len(stickers), i))
                    bot.sendSticker(chat_id=update.message.chat_id, sticker=stickers[i].get("file_id"))
                return
            elif '[meme]' in reply:
                bot.sendPhoto(chat_id=update.message.chat_id, photo='http://i.imgflip.com/1bij.jpg', caption="One does not simply send a meme")

                return 
        reply = reply.format(update.message.chat.first_name)
        bot.send_message(chat_id=update.message.chat_id, text=reply)

def group_msg(bot, update):
    logging.info("[{}] {}: {}".format(update.message.chat.title, update.message.from_user.first_name, update.message.text))
    addChat(update, group=True)
    needname = 0
    if 'erion' in update.message.text.lower() or needname == 0:
        reply = getPrivateReply(update.message.text)
        if reply != None:
            if '[sticker]' in reply:
                data = readJson('chatdata.json').get("stickers")
                
                stickers = []

                if len(reply.split()) == 3:
                    for sticker in data:
                        if sticker["emoji"] == reply.split()[2]:
                            stickers.append(sticker)
                else:
                    sticker = data

                if (len(stickers) < 1):
                    bot.send_message(chat_id=update.message.chat_id, text="I don't have any stickers like that yet!")
                    return

                for n in range(0, int(reply.split()[1])):
                    i = random.randint(0, len(stickers)-1)
                    bot.sendSticker(chat_id=update.message.chat_id, sticker=stickers[i].get("file_id"))
                return
            elif '[meme]' in reply:
                bot.sendPhoto(chat_id=update.message.chat_id, photo='http://i.imgflip.com/1bij.jpg', caption="One does not simply send a meme")

                return
            reply = reply.format(update.message.from_user.first_name)
            bot.send_message(chat_id=update.message.chat_id, text=reply)

def sticker(bot, update):
    addSticker(update)

    target = getChatVariable(update.message.chat_id, "target")
    if target != "":
        setChatVariable(update.message.chat_id, "target", "")
        chats = readJson('chats.txt')
        for chat in chats.get("chats"):
            if target.lower() == chat.get("name").lower():
                bot.send_sticker(chat_id=chat.get("id"), sticker=update.message.sticker.file_id)
                bot.send_message(chat_id=update.message.chat_id, text="Sent!")
                return



def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

##  COMMAND FUNCTIONS  ##
def start(bot, update):
    addChat(update)
    bot.send_message(chat_id=update.message.chat_id, text="New fone who dis")

def caps(bot, update, args):
    text = ' '.join(args)
    bot.send_message(chat_id=update.message.chat_id, text=text)

def clear(bot, update):
    data = {"stickers":[]}
    writeJson(data, "chatdata.json")


def send(bot, update, args):
    if isAdmin(update.message.chat_id) == False:
        bot.send_message(chat_id=update.message.chat_id, text="You're not permitted to do that!")
        return

    chats = readJson('chats.txt')
    text = ' '.join(args[1:])
    for chat in chats.get("chats"):
        # logging.info(chat)
        if args[0].lower() == chat.get("name").lower():
            bot.send_message(chat_id=chat.get("id"), text=text)
            return
    
    bot.send_message(chat_id=update.message.chat_id, text="No person or group with the name {} found!".format(args[0]))

def delete(bot, update, args):
    if isAdmin(update.message.chat_id) == False:
        bot.send_message(chat_id=update.message.chat_id, text="You're not permitted to do that!")
        return

    #ToDo add record of bot last messages
    chats = readJson('chats.txt')
    text = ' '.join(args[1:])
    for chat in chats.get("chats"):
        # logging.info(chat)
        if args[0].lower() == chat.get("name").lower():
            bot.delete_message(chat_id=args[0], message_id=args[1])
            return
    
    bot.send_message(chat_id=update.message.chat_id, text="No person or group with the name {} found!".format(args[0]))

def sendsticker(bot, update, args):
    if isAdmin(update.message.chat_id) == False:
        bot.send_message(chat_id=update.message.chat_id, text="You're not permitted to do that!")
        return

    stickers = readJson('chatdata.json').get("stickers")

    if len(args) == 1:
        setChatVariable(update.message.chat_id, "target", args[0])
        bot.send_message(chat_id=update.message.chat_id, text="Send me a sticker to forward!")
        return

    i = 0
    try:
        i = int(args[1])
    except ValueError:
        bot.send_message(chat_id=update.message.chat_id, text="{} is not a valid sticker number or ID!".format(args[1]))
        return 

    
    chats = readJson('chats.txt')
    for chat in chats.get("chats"):
        if args[0].lower() == chat.get("name").lower():
            bot.send_sticker(chat_id=chat.get("id"), sticker=stickers[i].get("file_id"))
            return
    
    bot.send_message(chat_id=update.message.chat_id, text="No person or group with the name {} found!".format(args[0]))

def auth(bot, update, args):
    if args[0] == password:
        chats = readJson("chats.txt")
        # logging.info(update.message)
        for chat in chats.get("chats"):
            if update.message.chat_id == chat.get("id"):
                if chat.get("level") == 1:
                    bot.send_message(chat_id=update.message.chat_id, text="You're already an admin!")
                else:
                    chat["level"] = 1
                    bot.send_message(chat_id=update.message.chat_id, text="You're now an admin!")

        writeJson(chats, "chats.txt")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Shoo Mr Wrongboi")

def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


##  OTHER FUNCTIONS  ##
def writeJson(data, file):
    "Write json data to file"
    with open(file, 'w') as fp:
        json.dump(data, fp, indent=4)

def readJson(file):
    with open(file, 'r') as fp:
        if fp == None:
            return None
        return json.load(fp)

def addChat(update, group=False):
    loc = "chats.txt"
    chats = readJson(loc)
    # logging.info(update.message)
    contains = False
    for chat in chats.get("chats"):
        # logging.info(chat)
        if update.message.chat_id == chat.get("id"):
            contains = True
            chat["last"] = update.message.text

    if contains == False:
        if group == False:
            chats.get("chats").append({
                    "name": update.message.chat.first_name, 
                    "id": update.message.chat_id,
                    "level": 0,
                    "target": None,
                    "last": update.message.text})
        else:
            chats.get("chats").append({
                    "name": update.message.chat.title, 
                    "id": update.message.chat_id,
                    "level": 0,
                    "target": None,
                    "last": update.message.text})
    writeJson(chats, loc)

def addSticker(update):
    logging.info("Adding sticker from chat_id = {}, emoji = {}".format(update.message.chat_id, update.message.sticker.emoji))
    loc = "chatdata.json"
    data = readJson(loc)
    
    if data == None:
        data = {"stickers":[]}

    contains = False
    for sticker in data.get("stickers"):
        if update.message.sticker.file_id == sticker.get("file_id"):
            contains = True

    if contains == False:
        # if len(update.message.sticker.emoji) < 5:
        #     return

        data.get("stickers").append({
                "file_id": update.message.sticker.file_id,
                "emoji": update.message.sticker.emoji
            })
        writeJson(data, loc)

def getChatVariable(chat_id, variable):
    chats = readJson("chats.txt")
    # logging.info(update.message)
    for chat in chats.get("chats"):
        if chat_id == chat.get("id"):
            return chat.get(variable)


def setChatVariable(chat_id, variable, val):
    chats = readJson("chats.txt")
    # logging.info(update.message)
    for chat in chats.get("chats"):
        if chat_id == chat.get("id"):
            chat[variable] = val

    writeJson(chats, "chats.txt")

def isAdmin(chat_id):
    chats = readJson("chats.txt")
    # logging.info(update.message)
    for chat in chats.get("chats"):
        if chat_id == chat.get("id"):
            if chat.get("level") == 1:
                return True

    return False

##  SETUP  ##
def add_cmd(command, function, pass_args=False, filters=None):
    handler = CommandHandler(command, function, pass_args=pass_args, filters=filters)
    dispatcher.add_handler(handler)

def add_msg(message, function):
    handler = MessageHandler(message, function)
    dispatcher.add_handler(handler)

def add_ilq(function):
    handler = InlineQueryHandler(function)
    dispatcher.add_handler(handler)



##  MAIN  ##
if __name__ == '__main__':
    print("Starting bot!")
    random.seed(time.time())
    #add_cmd('help', help_private, filters= ~ Filters.group)
    #add_cmd('help', help_group, filters= Filters.group)
    add_cmd('start', start, filters= ~ Filters.group)
    add_cmd('echo', caps, pass_args=True)
    add_cmd('send', send, pass_args=True)
    add_cmd('clear', clear, pass_args=True)
    add_cmd('sticker', sendsticker, pass_args=True)
    add_cmd('auth', auth, pass_args=True)
    add_cmd('delete', delete)
    add_msg(Filters.group & Filters.text, group_msg)
    add_msg(Filters.text, private_msg)
    add_msg(Filters.sticker, sticker)
    
    add_msg(Filters.command, unknown)
    #add_ilq(inline_caps)

    updater.start_polling()