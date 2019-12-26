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
    listsData = requests.get(url = URLLists.replace('{board}',board), params = PARAMS).json()
    #print(cardsData)

    listIDCardsMap = {}
    exclude = ['Done ', 'Summer Tasks Completed']
    for li in listsData:
        if all(substring not in li['name'] for substring in exclude):
            x = BoardList(name=li['name'], cardList=[])
            listIDCardsMap[li['id']] = x
    for card in cardsData:
        if card['idList'] in listIDCardsMap.keys():
            x = Card(card['name'],card['idChecklists'])
            listIDCardsMap[card['idList']].cardList.append(x)

    listIDCards = sorted(listIDCardsMap.items(), key=lambda kv: (len(kv[1].cardList), kv[0]), reverse=True)

    if len(listIDCards)%2==1:
            listIDCards.append(['EMPTYLIST',BoardList()])
    
    s = ""
    i = 0
    while i < len(listIDCards):
        j=0
        k=0
        s+='${font Droid Sans Mono:bold:size=12}${color red}' + ("{b1: <30}{align}{b2: <1}".format(b1=listIDCards[i][1].name,align='${alignr}', b2=listIDCards[i+1][1].name)) + '\n'
        while j<len(listIDCards[i][1].cardList) or k<len(listIDCards[i+1][1].cardList):
            s+= '${font Droid Sans Mono:size=10}${color}' +  ("{c1: <30}{align}{c2}".format(c1=' ' if j>=len(listIDCards[i][1].cardList) else listIDCards[i][1].cardList[j].name,align='${alignr}', 
                    c2=' ' if k>=len(listIDCards[i+1][1].cardList) else listIDCards[i+1][1].cardList[k].name)) + '\n'
            if j < len(listIDCards[i][1].cardList):
                j+=1
            if k<len(listIDCards[i+1][1].cardList):
                k+=1
        #s+=('\n')
        i+=2

        #for odd
    
    print(s[0:-2])
    #print(markdown.markdown(s))
    #rendered = markdown(s)
    #print(mistletoe.markdown(s))


if __name__ == '__main__':
   main()