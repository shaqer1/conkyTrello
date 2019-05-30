#importing the requests library 
import requests 
import json
import mistletoe


board = ''
APIkey = ''
APItoken = ''
# api-endpoint 
URLBoards = 'https://api.trello.com//1/members/me/boards'
URLLists = 'https://api.trello.com/1/boards/{board}/lists'
URLCards = 'https://api.trello.com/1/boards/{board}/cards'
URLListCard = 'https://api.trello.com/1/lists/[idList]/cards'

class Card:
    def __init__(self, name='', idCheckLists=[]):
        self.name = name
        self.idCheckLists = idCheckLists
    name = ''
    idCheckLists = []

class BoardList:
    def __init__(self, name='', cardList=[]):
        self.name = name
        self.cardList = cardList
    name = ''
    cardList = []

def main():    
    with open('/home/shafay/conkyConfigs/trello/APIKey.json') as config_file:
        APIKeyData = json.load(config_file)

    APIkey = APIKeyData['key']
    APItoken = APIKeyData['token']
    board = APIKeyData['board']
    PARAMS = {
        'key': APIkey,
        'token': APItoken,
    }

    cardsData = requests.get(url = URLCards.replace('{board}',board), params = PARAMS).json()
    #print(cardsData)

    exclude = ['Done SP 2019', 'Done']

    listsData = requests.get(url = URLLists.replace('{board}',board), params = PARAMS).json()
    
    listCardPair = []
    for li in listsData:
        #print(li['name']+'\n')
        if li['name'] not in exclude:
            listCardsData = requests.get(url = URLListCard.replace('[idList]',li['id']), params = PARAMS).json()
            cardList = []
            for card in listCardsData:
                x = Card(card['name'],card['idChecklists'])
                cardList.append(x) 
            listCardPair.append(BoardList(li['name'],cardList))
    if len(listCardPair)%2==1:
            listCardPair.append(BoardList())
    #print(listCardPair)
    #todo in markown table
    s = ""
    i = 0
    while i < len(listCardPair):
        j=0
        k=0
        s+=("|{:<50}|{:<50}|".format(listCardPair[i].name,
                    listCardPair[i+1].name)) + '\n'
        s+=('|:------------------------------------------------:|:------------------------------------------------:|') + '\n'
        
        while j<len(listCardPair[i].cardList) or k<len(listCardPair[i+1].cardList):
            s+=("|{:<50}|{:<50}|".format(' ' if j>=len(listCardPair[i].cardList) else listCardPair[i].cardList[j].name,
                    ' ' if k>=len(listCardPair[i+1].cardList) else listCardPair[i+1].cardList[k].name)) + '\n'
            if j < len(listCardPair[i].cardList):
                j+=1
            if k<len(listCardPair[i+1].cardList):
                k+=1
        s+=('\n\n')
        i+=2

        #for odd
    
    print(s)
    rendered = mistletoe.markdown(s)
    #print(rendered)


if __name__ == '__main__':
   main()

# curl file:/home/shafay/conkyConfigs/trello/file.html
   # ${offset 15}${font Droid Sans Mono:size=10}${execi 14400 curl file:/home/shafay/conkyConfigs/trello/file.html}
   #cat ~/conkyConfigs/trello/file.html | lynx -stdin
   #${offset 15}${font Droid Sans Mono:size=10}${execi 14400 cat /home/shafay/conkyConfigs/trello/file.html | lynx -stdin}
   # ${offset 15}${font Droid Sans Mono:size=10}${execi 14400 python ~/conkyConfigs/trello/trelloMain.py}