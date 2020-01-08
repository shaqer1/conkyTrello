#importing the requests library 
import requests 
import json
import mistletoe
from datetime import datetime, timezone
from Utils import Utils
from decimal import localcontext, Decimal, ROUND_HALF_UP

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
        #process labels
        s= Utils().addLabels(self.labels) + ' ' + self.name
        # due date 📅
        s += str(Utils().processDate(self.dueDate))
        #checklist badge completed incomplete 🗹
        chkIt, chkItT = self.card['badges']['checkItemsChecked'], self.card['badges']['checkItems']
        checkListStr = '' if chkItT == 0 else '${font Symbola} 🗹$font ' + str(chkIt) + '/' + str(chkItT) # 
        if chkItT != 0:
            s+= Utils().getColors('green', checkListStr) if Decimal(3*chkItT/4).to_integral_value(rounding=ROUND_HALF_UP) <= chkIt else Utils().getColors('red', checkListStr) if Decimal(chkItT/4).to_integral_value(rounding=ROUND_HALF_UP) > chkIt else Utils().getColors('yellow', checkListStr)
        # comments icon: # 💬
        s += '' if self.card['badges']['comments'] == 0 else Utils().getColors('green', '${font Symbola} 💬$font ' + str(self.card['badges']['comments']))
        # attachment badge 📎
        s += '' if self.card['badges']['attachments'] == 0 else Utils().getColors('green', '${font Symbola} 📎$font ' + str(self.card['badges']['attachments']))
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
        self.maxCardW = 0
    name = ''
    cardList = []
    maxCardW = 0
    li = {}
def getOptimal(q, li1, li2):
    if len(q) == 0:
        return li1,li2
    li = q.pop(0)
    if li2['maxW'] < li1['maxW']:
        li2[len(li2)-1] = li[1]
        li2['maxW']+= len(li[1].cardList) +1
    else:
        li1[len(li1)-1] = li[1]
        li1['maxW']+= len(li[1].cardList) +1
    return getOptimal(q, li1, li2)
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

    listIDCardsMap = {}
    for li in listsData:
        x = BoardList(name=li['name'], cardList=[], li=li)
        listIDCardsMap[li['id']] = x
    for card in cardsData:
        if card['idList'] in listIDCardsMap.keys():
            if not card['dueComplete']:
                x = Card(card['name'],card)
                listIDCardsMap[card['idList']].cardList.append(x)
                listIDCardsMap[card['idList']].maxCardW = listIDCardsMap[card['idList']].maxCardW if len(card['name']) < listIDCardsMap[card['idList']].maxCardW else len(card['name'])

    # filter lists by closed False and size()>0
    listIDCardsMap = { k: v for (k,v) in listIDCardsMap.items() if len(v.cardList) > 0}
    listIDCards = sorted(listIDCardsMap.items(), key=lambda kv: (len(kv[1].cardList), kv[0]), reverse=True)
    
    #Optimal stacking
    queue = [] 
    for li in listIDCards:
        queue.append(li)
    listIDCards1 = {}
    listIDCards1['maxW'] = 0
    listIDCards2 = {}
    listIDCards2['maxW'] = 0
    listIDCards1, listIDCards2 = getOptimal(queue, listIDCards1, listIDCards2)
    maxW = listIDCards2['maxW'] if listIDCards2['maxW'] > listIDCards1['maxW'] else listIDCards1['maxW']
    del listIDCards1['maxW']
    del listIDCards2['maxW']
    s, i = "", 0
    isTitle1, isTitle2, j, k, l, m = True, True, 0, 0, 0, 0
    while i<maxW:
        if isTitle1:
            if j == len(listIDCards1):
                s1 = ' '
            else:
                s1, isTitle1 = "{b1: <30}".format(b1=Utils().getColors('red', Utils().getFont('title', listIDCards1[j].name))), False
        else:
            s1, l = "{c1: <30}".format(c1=Utils().getFont('body', listIDCards1[j].cardList[l].processCard())), l+1
            if l == len(listIDCards1[j].cardList):
                isTitle1, j, l = True, j+1, 0
        if isTitle2:
            if k == len(listIDCards2):
                s2 = ' '
            else:
                s2, isTitle2 = "{b2: <1}".format(b2=Utils().getColors('red', Utils().getFont('title', listIDCards2[k].name))), False
        else:
            s2, m = "{c2}".format(c2=Utils().getFont('body', listIDCards2[k].cardList[m].processCard())), m+1
            if m == len(listIDCards2[k].cardList):
                isTitle2, k, m = True, k+1, 0
        s+= s1 + '${alignr}' + s2 + '\n'
        i+=1
    
    print(s[0:-1])


if __name__ == '__main__':
   main()