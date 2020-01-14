# conkyTrello
Trello widget for conky 

# Conky Installation

# Setup

## APIKey.json

1. Get Trello API key, Token, BoardID from 
1. ```cd conkyTrello```
1. ```touch APIKey.json```
1. Modify APIKey_Default.json with API key, token and board ID
    - example below
    ```
    {
        "key": "TrelloKey",
        "token":"Trello Token",
        "board": "BoardID"
    }
    ```
1. 


# Run 

```conky -c ~/conkyTrello/.conkyrc3 > /dev/null```

# Comming soon
- Python script for config
- config file