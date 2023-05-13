from scanf import scanf

userCards = ['3-R', '4-R', '11-R', '2-G', '10-V']
opponentCards = ['2-R', '10-R', '4-G', '11-V', '10-G']

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

        turn = checkRoundWinner(userMove, opponentMove, turn)[0]
        calculateSumsWinner(turn, userMove, opponentMove)

        print("You:", userSum)
        print("Opponent:", opponentSum)

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


def calculateSumsWinner(winner, userMove, opponentMove):
    global opponentSum
    global userSum
    downCardsSum = getCardValue(userMove) + getCardValue(opponentMove)
      #map to user or opponents
    if winner == 1:
        announcement = checkAnnouncement(getCardColor(opponentMove), getCardValue(opponentMove), opponentCards)
        opponentSum = opponentSum + downCardsSum + announcement
    else:
        announcement = checkAnnouncement(getCardColor(userMove), getCardValue(userMove), userCards)
        userSum = userSum + downCardsSum + announcement


def userMoves():
    print("Your turn! Choose the index of your cards: ", userCards)
    print("Opponent Cards are: " , opponentCards)
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
    global tromf
    global userCards
    global opponentCards

    winner = 0
    winnerSum = 0

    if firstPlayerInRound == 1:
        firstPlayerInRoundSum = opponentSum
        firstPlayerInRoundCardColor = getCardColor(opponentMove)
        firstPlayerInRoundCardValue = getCardValue(opponentMove)
        secondPlayerInRoundSum = userSum
        secondPlayerInRoundCardColor = getCardColor(userMove)
        secondPlayerInRoundCardValue = getCardValue(userMove)
        cardsOfTheFirstPlayerInRound = opponentCards
    else:
        firstPlayerInRoundSum = userSum
        firstPlayerInRoundCardColor = getCardColor(userMove)
        firstPlayerInRoundCardValue = getCardValue(userMove)
        secondPlayerInRoundSum = opponentSum
        secondPlayerInRoundCardColor = getCardColor(opponentMove)
        secondPlayerInRoundCardValue = getCardValue(opponentMove)
        cardsOfTheFirstPlayerInRound = userCards

    downCardsSum = firstPlayerInRoundCardValue + secondPlayerInRoundCardValue

    #check for announcements
    announcement = checkAnnouncement(firstPlayerInRoundCardColor, firstPlayerInRoundCardValue, cardsOfTheFirstPlayerInRound)
    #print("Anunt! ", announcement)

    if(firstPlayerInRoundCardColor == secondPlayerInRoundCardColor):
        if(firstPlayerInRoundCardValue > secondPlayerInRoundCardValue):
            winnerSum = firstPlayerInRoundSum + downCardsSum
            winner = firstPlayerInRound
        else:
            winnerSum = secondPlayerInRoundSum + downCardsSum
            winner = -1 * firstPlayerInRound
    else: #different colors => if 2nd player did not move tromf, then first player wins
        if firstPlayerInRoundCardColor == tromf: #differenct colors, first card is tromf => second card != tromf
            winnerSum = firstPlayerInRoundSum + downCardsSum
            winner = firstPlayerInRound
        elif secondPlayerInRoundCardColor == tromf:
            winnerSum = secondPlayerInRoundSum + downCardsSum
            winner = -1 * firstPlayerInRound
        else: #if no tromfs => first one wins the round
            winnerSum = firstPlayerInRoundSum + downCardsSum
            winner = firstPlayerInRound

    winnerSum = winnerSum + announcement 
    
    return winner, winnerSum

    
def checkAnnouncement(movedCardColor, movedCardValue, cards):
    global tromf
    for card in cards:
        if getCardColor(card) == movedCardColor and  getCardValue(card) != movedCardValue: #different cards, same color
            if getCardValue(card) + movedCardValue == 7: #treiar + patrar
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


def whatYouCanMove(downCard, cards):
    if downCard == "":
        return cards
    else:
        #to match the color 
        newCards = []
        for card in cards:
            if getCardColor(card) == getCardColor(downCard): #if the color matches
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

        allowedOpponentCards = whatYouCanMove(downCard, opponentCards)

        #print('o1', opponentCards)
        #print('o', allowedOpponentCards)

        for i in range(0, len(allowedOpponentCards)):
            move = allowedOpponentCards[i]
            #print(move)
            opponentCards.remove(move)
            winner, sumWinner = checkRoundWinner(downCard, move, -1)
            opponentSum = opponentSum + sumWinner if winner == 1 else opponentSum
            score = minimax(move, depth + 1, False)
            opponentCards.append(move)
            opponentSum = opponentSum - sumWinner if winner == 1 else opponentSum
            if bestScore < score:
                bestScore = score

        return bestScore
    
    else:
        bestScore = 1000000

        allowedUserCards = whatYouCanMove(downCard, userCards)

        #print('u ', allowedUserCards)

        for i in range(0, len(allowedUserCards)):
            move = allowedUserCards[i]
            userCards.remove(move)
            winner, sumWinner = checkRoundWinner(downCard, move, 1)
            userSum = userSum + sumWinner if winner == -1 else userSum 
            score = minimax(move, depth + 1, True)
            userCards.append(move)
            userSum = userSum - sumWinner if winner == -1 else userSum
            if bestScore > score:
                bestScore = score

        return bestScore
            

def bestMove(downCard):
    score = 0
    bestScore = -10000000
    bestMove = ""

    isMaximizing = True if downCard == "" else False

    if downCard == "":
        allowedOpponentCards = opponentCards #opp mives first
    else:
        allowedOpponentCards = whatYouCanMove(downCard, opponentCards)
    print(allowedOpponentCards)

    if downCard == "":
        for i in range(0, len(allowedOpponentCards)):
            score = minimax(opponentCards[i], 0, False)
            if(score > bestScore):
                bestScore = score
                bestMove = allowedOpponentCards[i]
    else:
        for i in range(0, len(allowedOpponentCards)):
            score = minimax(downCard, 0, True)
            if(score > bestScore):
                bestScore = score
                bestMove = allowedOpponentCards[i]
    
    return bestMove


gamePlay()
