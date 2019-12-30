#importing the requests library 
import requests 
import json
import mistletoe
from datetime import datetime, timezone
from Utils import Utils


board = ''
APIkey = ''
APItoken = ''
# api-endpoint 
URLBoards = 'https://api.trello.com//1/members/me/boards'
URLLists = 'https://api.trello.com/1/boards/{board}/lists'
URLCards = 'https://api.trello.com/1/boards/{board}/cards'
URLListCard = 'https://api.trello.com/1/lists/[idList]/cards'

class Card:
    def __init__(self, name='', card={}, badges={}):
        self.name = name
        self.card = card
        self.labels = self.card['labels']
        self.dueDate = datetime.strptime(self.card['due']+'+0000','%Y-%m-%dT%H:%M:%S.%fZ%z').replace(tzinfo=timezone.utc).astimezone(tz=None)
        self.checklist = [ self.card['badges']['checkItemsChecked'], self.card['badges']['checkItems'] ]
        self.comments = self.card['badges']['comments']
    def processCard(self):
        s= Utils().addLabels(self.labels) + ' ' + self.name
        #TODO: due date
        #TODO: checklist badge completed incomplete
        #TODO: comments icon: #
        #TODO: attachment badge
        return s
    name = ''
    labels = []
    card = {}
    dueDate = {}

class BoardList:
    def __init__(self, name='', cardList=[],li={}):
        self.name = name
        self.cardList = cardList
        self.li = li
    name = ''
    cardList = []
    li = {}

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
    listsData = requests.get(url = URLLists.replace('{board}',board), params = PARAMS).json()
    listsData = list(filter(lambda li: li['closed'] == False, listsData))
    #print(cardsData)

    listIDCardsMap = {}
    for li in listsData:
        x = BoardList(name=li['name'], cardList=[], li=li)
        listIDCardsMap[li['id']] = x
    for card in cardsData:
        if card['idList'] in listIDCardsMap.keys():
            if not card['dueComplete']:
                x = Card(card['name'],card)
                listIDCardsMap[card['idList']].cardList.append(x)

    # filter lists by closed False and size()>0
    listIDCardsMap = { k: v for (k,v) in listIDCardsMap.items() if len(v.cardList) > 0}
    listIDCards = sorted(listIDCardsMap.items(), key=lambda kv: (len(kv[1].cardList), kv[0]), reverse=True)

    if len(listIDCards)%2==1:
            listIDCards.append(['EMPTYLIST',BoardList()])
    
    s = ""
    i = 0
    while i < len(listIDCards):
        j=0
        k=0
        s+='${font DejaVu Sans Mono:bold:size=12}${color red}' + ("{b1: <30}{align}{b2: <1}".format(b1=listIDCards[i][1].name,align='${alignr}', b2=listIDCards[i+1][1].name)) + '\n'
        while j<len(listIDCards[i][1].cardList) or k<len(listIDCards[i+1][1].cardList):
            s+= '${font DejaVu Sans Mono:size=10}${color}' +  ("{c1: <30}{align}{c2}".format(c1=' ' if j>=len(listIDCards[i][1].cardList) else listIDCards[i][1].cardList[j].processCard(),align='${alignr}', 
                    c2=' ' if k>=len(listIDCards[i+1][1].cardList) else listIDCards[i+1][1].cardList[k].processCard())) + '\n'
            if j < len(listIDCards[i][1].cardList):
                j+=1
            if k<len(listIDCards[i+1][1].cardList):
                k+=1
        #s+=('\n')
        i+=2
    
    print(s[0:-2])


if __name__ == '__main__':
   main()