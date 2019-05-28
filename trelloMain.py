#importing the requests library 
import requests 
import json

board = ''
APIkey = ''
APItoken = ''
# api-endpoint 
URLBoards = 'https://api.trello.com//1/members/me/boards'
URLLists = 'https://api.trello.com/1/boards/{board}/lists'
URLCards = 'https://api.trello.com/1/boards/{board}/cards'
URLListCard = 'https://api.trello.com/1/lists/[idList]/cards'

class Card:
    def __init__(self, name, idCheckLists):
        self.name = name
        self.idCheckLists = idCheckLists
    name = ''
    idCheckLists = []

def main():    
    with open('APIKey.json') as config_file:
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

    listsData = requests.get(url = URLLists.replace('{board}',board), params = PARAMS).json()
    #print(listsData)
    
    listCardPair = {}
    for li in listsData:
        #print(li['name']+'\n')
        listCardsData = requests.get(url = URLListCard.replace('[idList]',li['id']), params = PARAMS).json()
        cardsList = []
        for card in listCardsData:
            #print(card['name']) 
            x = Card(card['name'],card['idChecklists'])
            cardsList.append(x) 
        listCardPair[li['name']] = cardsList
        #print('\n')
    #print(listCardPair)
    #todo read one by one 
    print("{:<15} {:<15}".format(' ',' '))
    for k, v in listCardPair.iteritems():
        for c in v:
            print( "{:<15} {:<15}".format(k, c.name))
    """ for x in listCardPair:
        print('\n')
        print(x)
        for y in listCardPair[x]:
            print(y.name)
        print('\n') """

if __name__ == '__main__':
   main()