from vars import *
from stringhandling import *
import requests
import time
import string
import random

def filtertext(text, filter):
    textwords = text.split()
    resultwords = [word for word in textwords if word.lower() not in filter]
    return ' '.join(resultwords) 


def getQuery(text):
    words = text.split()

    #Quenstion type in list
    for word in words:
        num = bestmatch(queries, word, threshold=0.2, max=2)
        if (num != -1):
            return num
    
    #General question
    if (text[-1:] == '?'):
        return -2


    return -1

def getStatement(text):
    words = text.split()

    #Quenstion type in list
    for word in words:
        num = bestmatch(statements, word, threshold=0.2, max=2)
        if (num != -1):
            return num

    return -1

def getPrivateReply(text):
    # text = replacebest(text, stopwords)
    # print(text)
    exclude = [',', '.']
    text = ''.join(ch for ch in text if ch not in exclude)
    text = filtertext(text, stopwords)
    # print(text)
    qid = getQuery(text)

    if (qid != -1):
        query = text
        for filter in queries:
            query = replacebest(query, filter, threshold=0.2)
            query = filtertext(query, filter)
            # print(query + " " + filter[0])
        
        # print(query)
        exclude = set(string.punctuation)
        query = ''.join(ch for ch in query if ch not in exclude)

        func = queryFunctions.get(qid)
        return func(query)
    
    #it was some statment
    sid = getStatement(text)
    
    if sid == 0:
        return "Hello {0}!"
    elif sid == 1:
        return "Goodbye {0}!"
    elif sid == 2:
        return "It's a pleasure"
    elif sid == 3:
        return "Nah you're ghey"

    return None

def question(text):
    return None

def what(text):
    text = replacebest(text, whats)
    indices = []
    words = text.split()
    for i in range(0, len(words)):
        for j in range(0, len(whats)):
            if words[i] == whats[j]:
                indices.append(j)

    # print(indices)
    # print(text)
    

    if indices == [0]: #Time
        date = time.localtime(time.time())
        return "The current time is {}:{}".format(date.tm_hour, date.tm_min)
    elif indices == [1]: #Date
        date = time.localtime(time.time())
        return "The date is {}/{}/{}".format(date.tm_mday, date.tm_mon, date.tm_year)
    elif indices == [0, 1] or indices == [1, 0]: #Date and time
        date = time.localtime(time.time())
        return "It is {}:{} on {}/{}/{}".format(date.tm_hour, date.tm_min, date.tm_mday, date.tm_mon, date.tm_year)
    elif indices == [2] or indices == [6, 2]: #month
        if 6 in indices:
            date = time.localtime(time.time() + 2592000)
            return "Next month is {}".format(months[date.tm_mon-1])
        else:
            date = time.localtime(time.time())
            return "This month is {}".format(months[date.tm_mon-1])
    elif indices == [1, 5] or indices == [5, 1]: #Tomorrow Date
        date = time.localtime(time.time() + 86400)
        return "Tomorrow's date is {}/{}/{}".format(date.tm_mday, date.tm_mon, date.tm_year)
    elif indices == [5]:
        date = time.localtime(time.time() + 86400)
        return "Tomorrow is {} {}/{}/{}".format(weekdays[date.tm_wday], date.tm_mday, date.tm_mon, date.tm_year)
    elif indices == [3, 4]: #Day of week
        date = time.localtime(time.time())
        return "Today is {}".format(weekdays[date.tm_wday])

    return "You'll have to ask someone else!"

def how(text):
    return None

def fetch(text):
    text = replacebest(text, gets)
    indices = []
    words = text.split()
    for i in range(0, len(words)):
        for j in range(0, len(gets)):
            if words[i] == gets[j]:
                indices.append(j)

    if indices == [0]: #Memes
        return "[meme]"
    if indices == [1]: #News
        #return "Who listens to news anyway?"

        ntoken = '02ec5c82f8d3487b8ba495c1d221ad76'
        url = 'https://newsapi.org/v2/top-headlines?sources=fox-news&apiKey='

        data = requests.get(url + ntoken).json()
        # print(type(data))

        random.seed(time.time())
        if ('random' in text.lower()):
            return "Here's a random article for you: {}".format(data.get('articles')[random.randint(0, 9)].get('url'))
        if ('top' in text.lower()):
            return "Here's the top news article: {}".format(data.get('articles')[0].get('url'))
        else:
            return "Here's an article for you: {}".format(data.get('articles')[random.randint(0, 9)].get('url'))

    if indices == [2]: #Stickers
        return "[sticker]"
    if indices == [3]: #Nudes
        return "Please visit pornhub.com"

    if len(indices) > 1:
        return "Don't ask for too much 🙄"

    return None

def want(text):
    text = replacebest(text, gets)
    indices = []
    words = text.split()
    for i in range(0, len(words)):
        for j in range(0, len(gets)):
            if words[i] == gets[j]:
                indices.append(j)

    if len(indices) == 1: 
        return "If you want {} just ask me!".format(gets[indices[0]])
    elif len(indices) > 1:
        out = gets[indices[0]]
        for i in range(1, len(indices)-1):
            out += ', ' + gets[indices[i]]
        
        return "Just ask me if you want {} or {}!".format(out, gets[indices[len(indices)-1]])

    return None

queryFunctions = {
   -2: what,
    0: what,
    1: how,
    2: fetch,
    3: want
}

if __name__ == '__main__':
    print("Testing!")

    text = "Send News"
    print(getPrivateReply(text))
    