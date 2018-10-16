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


                return
            elif '[meme]' in reply:
                bot.sendPhoto(chat_id=update.message.chat_id, photo='http://i.imgflip.com/1bij.jpg', caption="One does not simply send a meme")

                return 
            reply = reply.format(update.message.from_user.first_name)
            bot.send_message(chat_id=update.message.chat_id, text=reply)



def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

##  COMMAND FUNCTIONS  ##
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="New fone who dis")

def caps(bot, update, args):
    text = ' '.join(args)
    bot.send_message(chat_id=update.message.chat_id, text=text)

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

    if contains == False:
        if group == False:
            chats.get("chats").append({
                    "name": update.message.chat.first_name, 
                    "id": update.message.chat_id,
                    "level": 0})
        else:
            chats.get("chats").append({
                    "name": update.message.chat.title, 
                    "id": update.message.chat_id,
                    "level": 0})
    writeJson(chats, loc)

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
    
    #add_cmd('help', help_private, filters= ~ Filters.group)
    #add_cmd('help', help_group, filters= Filters.group)
    add_cmd('start', start, filters= ~ Filters.group)
    add_cmd('echo', caps, pass_args=True)
    add_cmd('send', send, pass_args=True)
    add_cmd('auth', auth, pass_args=True)
    add_msg(Filters.group & Filters.text, group_msg)
    add_msg(Filters.text, private_msg)
    
    add_msg(Filters.command, unknown)
    #add_ilq(inline_caps)

    updater.start_polling()