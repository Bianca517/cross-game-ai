from scanf import scanf

opponentCards = ['3-R', '11-R', '2-G', '10-V']
userCards = ['4-R', '10-R', '4-G', '11-V']

opponentSum = 0
userSum = 0

scores = {
    'User' : -1,
    'Opp' : 1
}

def gamePlay():
    global opponentSum
    global userSum

    while(0 < len(userCards)):
        #i go first
        print("Your turn! Choose the index of your cards: ", userCards)
        userInput = scanf("%d") #returns a tuple
        print("You moved: ", userCards[userInput[0]])
        userInput = userInput[0]
        userMove = userCards[userInput]
        userCards.remove(userMove)

        opponentMove = bestMove(userMove)
        print("Opponend moved: ", opponentMove)
        opponentCards.remove(opponentMove)

        if(opponentMove.split('-')[1] == userMove.split('-')[1]):
            if(int(opponentMove.split('-')[0]) > int(userMove.split('-')[0])):
                opponentSum = opponentSum + int(opponentMove.split('-')[0]) + int(userMove.split('-')[0])
            else:
                userSum = userSum + int(opponentMove.split('-')[0]) + int(userMove.split('-')[0])
        else:
            userSum = userSum + int(opponentMove.split('-')[0]) + int(userMove.split('-')[0])


    print("Game finished!")
    print("You:", userSum)
    print("Opponent:", opponentSum)


def checkWinner():
    global opponentSum
    global userSum
    if len(opponentCards + userCards) == 0:
        if userSum > opponentSum:
            return 'User'
        elif opponentSum > userSum:
            return 'Opp'
        else:
            return 0
    else:
        return 0


def getCardValue(card):
    return int(card.split('-')[0])


def whatYouCanMove(dowNCard, cards):
    #to match the color 
    newCards = []
    for card in cards:
        if card.split('-')[1] == dowNCard.split('-')[1]:
            newCards.append(card)
    
    #if no card of that color is present, move anything
    if newCards == []:
        newCards = cards
    
    return newCards


def minimax(downCard, depth, isMaximizing): 
    global opponentSum
    global userSum
    result = checkWinner()
    
    if result != 0:
        score = scores[result]
        return score
    
    if(isMaximizing):
        bestScore = -1000000

        if downCard != "":
            allowedOpponentCards = whatYouCanMove(downCard, opponentCards)
        else:
            allowedOpponentCards = opponentCards

        #print('o1', opponentCards)
        #print('o', allowedOpponentCards)

        for i in range(0, len(allowedOpponentCards)):
            move = allowedOpponentCards[i]
            #print(move)
            opponentCards.remove(move)
            opponentSum = opponentSum + getCardValue(move)
            score = minimax(move, depth + 1, False)
            opponentCards.append(move)
            opponentSum = opponentSum - getCardValue(move)
            if bestScore < score:
                bestScore = score


        return bestScore
    
    else:
        bestScore = 1000000

        if downCard != "":
            allowedUserCards = whatYouCanMove(downCard, userCards)
        else:
            allowedUserCards = userCards

        #print('u ', allowedUserCards)

        for i in range(0, len(allowedUserCards)):
            move = allowedUserCards[i]
            userCards.remove(move)
            userSum = userSum + getCardValue(move)
            score = minimax(move, depth + 1, True)
            userCards.append(move)
            userSum = userSum - getCardValue(move)
            if bestScore > score:
                bestScore = score

        return bestScore
            

def bestMove(downCard):
    score = 0
    bestScore = -10000000
    bestMove = ""

    if downCard != "":
        allowedOpponentCards = whatYouCanMove(downCard, opponentCards)
    else:
        allowedOpponentCards = opponentCards

    print(allowedOpponentCards)

    for i in range(0, len(allowedOpponentCards)):
        score = minimax(downCard, 0, True)
        if(score > bestScore):
            bestScore = score
            bestMove = allowedOpponentCards[i]
    
    return bestMove


gamePlay()
