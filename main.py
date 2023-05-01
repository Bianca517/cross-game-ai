from scanf import scanf

opponentCards = ['3-R', '11-R', '2-G', '10-V']
userCards = ['4-R', '10-R', '4-G', '11-V']

tromf = 'R'

opponentSum = 0
userSum = 0

scores = {
    'User' : -1,
    'Opp' : 1
}

def gamePlay():
    global opponentSum
    global userSum

    turn = -1
    while(0 < len(userCards)):
        #i go first
        userMove, opponentMove = handleTurns(turn)

        turn = checkRoundWinner(userMove, opponentMove, turn)

    print("Game finished!")
    print("You:", userSum)
    print("Opponent:", opponentSum)


def handleTurns(whoWonLast):
    if(whoWonLast == 1):
        #opponent moves first
        opponentMove = opponentMoves("")  
        userMove = userMoves()
    else:
        userMove = userMoves()
        opponentMove = opponentMoves(userMove)

    return userMove, opponentMove


def userMoves():
    print("Your turn! Choose the index of your cards: ", userCards)
    userInput = scanf("%d") #returns a tuple
    print("You moved: ", userCards[userInput[0]])
    userInput = userInput[0]
    userMove = userCards[userInput]
    userCards.remove(userMove)
    return userMove


def opponentMoves(userMoveOrNull):
    opponentMove = bestMove(userMoveOrNull)
    print("Opponend moved: ", opponentMove)
    opponentCards.remove(opponentMove)
    return opponentMove


def checkRoundWinner(userMove, opponentMove, firstPlayerInRound):
    global opponentSum
    global userSum

    if firstPlayerInRound == 1:
        firstPlayerInRoundSum = opponentSum
    else:
        firstPlayerInRoundSum = userSum

    userMoveValue = getCardValue(userMove)
    opponentMoveValue = getCardValue(opponentMove)

    userMoveColor = getCardColor(userMove)
    opponentMoveColor = getCardColor(opponentMove)

    if(userMoveColor == opponentMoveColor):
        #also check for announcements
        #announcement = checkAnnouncement(userMove, cardsOfTheFirstPlayerInRound)
        if(opponentMoveValue > userMoveValue):
            opponentSum = opponentSum + opponentMoveValue + userMoveValue
            return 1
        else:
            userSum = userSum + opponentMoveValue + userMoveValue
            return -1
    else:
        firstPlayerInRoundSum = firstPlayerInRoundSum + opponentMoveValue + userMoveValue
        return firstPlayerInRound
    

def checkAnnouncement(movedCard, cards):
    global tromf
    movedCardColor = getCardColor(movedCard)
    for card in cards:
        if getCardColor(card) == movedCardColor:
            if getCardValue(card) + getCardValue(movedCard) == 7: #treiar + patrar
                if movedCardColor == tromf:
                    return 40
                else:
                    return 20
    return 0


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


def getCardColor(card):
    return card.split('-')[1]


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
