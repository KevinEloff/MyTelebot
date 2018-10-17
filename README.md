# MyTelebot
A simple telegram chat bot created in python using python-telegram-bot api
--------------

Overview
--------------
This is a simple chatbot that works through telegram's api. It is able to extract queries from text and act accordingly. The bot makes use of **Levenshtein Distance** to assist it in locating keywords. The bot uses these queries to do various tasks, such as retrieving news from a news API, fetching images from url's, collecting and sending stickers or sending the current date or time. These are just some simple uses of this bot. It could further be used for controlling other scripts/servers/data in an easily manageble and interactive environment. This bot also works great in groups.

How it works
--------------
The bot first recieves a **query** in text form from the user. It processes this **query** by first removing punctuation and unneccessary words such as:
```
a is that this the I how to lol it again
```

It then further processes the **query** by searching for **keywords** that are used to sort the **query** into **catagories**.
```python
'what', 'what's'
'how'
'get', 'fetch', 'send', 'show', 'give'
```

Once the **catagory** is known and removed from the **query**, the bot uses the rest of the information as parameters for the **catagory**. It then looks for other **keywords** such as date/news/time or numbers that may assist it in responding to the **query**.


Other functionality
--------------
Here are some other **commands** the bot understands:
```
/start                                (Start new interaction with bot)
/send <chat name> <text>              (Send text to specifc person or group)
/sticker <chat name> <sticker ID>     (Send sticker to chat, leave <sticker ID> blank to send your own)
/echo <text>                          (Echo sent text)
/auth <password>                      (Grant administration priveledges)
```

To see the bot in action, add **erion_bot** on telegram!

Dependencies
--------------
- python-telegram-bot
- requests


This bot makes use of python-telegram-bot. Found here: https://github.com/python-telegram-bot/python-telegram-bot
