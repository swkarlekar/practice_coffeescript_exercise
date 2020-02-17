#----------------------------------------------------------------------------------------
def main(): 
	database = createBoards()
	#playGameWithSelf(database, 1000000)
	#printDictionaryToOutfile(database)
	playGameWithHuman(database)
	cont = input("Continue? Y or N: ")
	while cont == "Y" or cont == 'y':
		playGameWithHuman(database)
		cont = input("Continue? Y or N: ")

#----------------------------------------------------------------------------------------
def createBoards(): 
	database = getDictionaryFromOutfile()
	return database
#----------------------------------------------------------------------------------------
def playGameWithSelf(database, n): 
	for x in range(n): 
		COM = []
		HUM = []
		board = '---------'
		while not hasWon(board)[0]:
			board = makeHumanMoveByComputer(database, board, HUM)
			if not hasWon(board)[0]: 
				board = makeComputerMove(database, board, COM)
		changeProbabilties(database, findWinner(board), COM, HUM)
		#print(x)
#----------------------------------------------------------------------------------------
def playGameWithSelf2(database, n): 
	COM = []
	HUM = []
	for x in range(n): 
		board = '---------'
		while not hasWon(board)[0]:
			board = makeHumanMoveByComputerUnexplored(database, board, HUM)
			if not hasWon(board)[0]: 
				board = makeComputerMove(database, board, COM)
		changeProbabilties(database, findWinner(board), COM, HUM)
		#print(x)
#----------------------------------------------------------------------------------------
def playGameWithHuman(database, n = 1): 
	COM = []
	HUM = []
	board = '---------'
	while not hasWon(board)[0]:
		board = makeHumanMove(database, board, HUM)
		if not hasWon(board)[0]: 
			board = makeComputerMove(database, board, COM)
	displayBoard(board)
	changeProbabilties(database, findWinner(board), COM, HUM)
	print("Winner!: ", findWinner(board))
#----------------------------------------------------------------------------------------
def printDictionaryToOutfile(dict):
	import pickle
	outfile = open('database.txt', 'wb') 
	pickle.dump(dict, outfile)
	outfile.close()
#----------------------------------------------------------------------------------------
def changeProbabilties(database, str, COM, HUM):
	if str == 'COMPUTER':
		for [board, x] in COM: 
			database[board][x] +=3
		for [board, x] in HUM:
			if database[board][x] > 1:
				database[board][x] -=1
	if str == 'HUMAN':
		for [board, x] in COM: 
			if database[board][x] > 1:
				database[board][x] -=1
		for [board, x] in HUM: 
			database[board][x] +=3
	if str == 'TIE':
		for [board, x] in COM: 
			database[board][x] +=1
		for [board, x] in HUM: 
			database[board][x] +=1
#----------------------------------------------------------------------------------------
def getDictionaryFromOutfile():
	import pickle
	outfile = open('database.txt', 'rb')
	dict = pickle.load(outfile)
	outfile.close()
	return dict
#----------------------------------------------------------------------------------------
def hasWon(board):
	if checkRows(board)[0]: return checkRows(board)
	if checkCols(board)[0]: return checkCols(board)
	if checkDiagonals(board)[0]: return checkDiagonals(board)
	if '-' not in board: return [True, 1]
	return [False, 0]
#----------------------------------------------------------------------------------------
def findWinner(board):
	if hasWon(board)[0]:
		if hasWon(board)[1] == 'X':
			return 'HUMAN'
		if hasWon(board)[1] == 'O':
			return 'COMPUTER'
		if hasWon(board)[1] == 1:
			return 'TIE'
	return ''
#----------------------------------------------------------------------------------------
def displayBoard(board):
	print("\nCurrent Board:\n")
	for x in range(0, 9, 3):
		print(" ", board[x], "|", board[x+1], "|", board[x+2])
		if x != 6: print('-'*13)
	print()
#----------------------------------------------------------------------------------------
def displayBoardForHumanMove(board):
	print("\nPick move:\n")
	temp = board 
	while '-' in temp:
		temp = temp[0:temp.index('-')] + str(temp.index('-')) + temp[temp.index('-')+1:] 
	for x in range(0, 9, 3):
		print(" ", temp[x], "|", temp[x+1], "|", temp[x+2])
		if x != 6: print('-'*13)
	print()
#----------------------------------------------------------------------------------------
def removeAlreadyTakenMoves(database, board):
	moves = database[board]
	for char in range(len(board)): 
		if board[char] != '-':
			moves[char] = 0
	database[board] = moves
#----------------------------------------------------------------------------------------
def createInitialDatabase():
	database = {'---------': [9]*9} #{empty board}
	sequence = [0, 1, 2, 3, 4, 5, 6, 7, 8,]
	from itertools import permutations
	filledBoards = list(permutations(sequence, 9))
	for perm in filledBoards:
		for x in range(8):
			database[stringBoard(perm, x)] = [9]*9
	database = removeWinners(database)
	for board in database.keys():
		removeAlreadyTakenMoves(database, board)
	printDictionaryToOutfile(database)
	return database
#----------------------------------------------------------------------------------------
def makeComputerMove(database, board, COM):
	moves = database[board]
	index = findProbableMove(database, board)
	COM.append([board, index])
	board = board[:index] + 'O' + board[index+1:]
	return board
#----------------------------------------------------------------------------------------
def makeHumanMoveByComputer(database, board, HUM):
	moves = database[board]
	index = findProbableMove(database, board)
	HUM.append([board, index])
	board = board[:index] + 'X' + board[index+1:]
	return board
#----------------------------------------------------------------------------------------
def makeHumanMoveByComputerUnexplored(database, board, HUM):
	moves = database[board]
	index = findUnexploredMove(database, board)
	HUM.append([board, index])
	board = board[:index] + 'X' + board[index+1:]
	return board
#----------------------------------------------------------------------------------------
def makeHumanMove(database, board, HUM):
	moves = database[board]
	displayBoard(board)
	displayBoardForHumanMove(board)
	index = int(input("Please enter index of move: "))
	while not isViableMove(board, index):
		print("Sorry, that move is not valid. Please try again.")
		index = int(input("Please enter index of move: "))
	HUM.append([board, index])
	board = board[:index] + 'X' + board[index+1:]
	return board
#----------------------------------------------------------------------------------------
def isViableMove(board, index):
	if index > -1 and index < 9 and board[index] == '-':
		return True
	return False
#----------------------------------------------------------------------------------------
def findProbableMove(database, board):
	moves = database[board]
	lst = [0]
	for x in range(len(moves)): 
		lst.append(moves[x]/sum(moves))
	rand = random()
	for x in range(1, len(lst)): 
		if sum(lst[0:x]) < rand < sum(lst[0:x+1]): return x-1
#----------------------------------------------------------------------------------------
def findRandomMove(database, board):
	moves = database[board]
	index = int(random()*len(moves))
	while not isViableMove(board, index):
		index = int(random()*len(moves))
	return index
#----------------------------------------------------------------------------------------
def findUnexploredMove(database, board):
	moves = database[board]
	min = float('inf')
	minindex = 0
	for x in range(9): 
		if isViableMove(board, x):
			if abs(10-moves[x]) < min: 
				min = abs(10-moves[x])
				minindex = x
	return minindex
#----------------------------------------------------------------------------------------
def removeWinners(database): 
	from copy import copy
	temp = database.copy()
	for key in database.keys():
		if checkRows(key)[0] == True or checkCols(key)[0] == True or checkDiagonals(key)[0] == True:
			del temp[key]
	return temp
#----------------------------------------------------------------------------------------
def checkRows(board):
	for x in range(0, 9, 3):
		if board[x] == board[x+1] == board[x+2] != '-':
			return [True, board[x]]
	return [False, 0]
#----------------------------------------------------------------------------------------
def checkCols(board):
	for x in range(0, 3):
		if board[x] == board[x+3] == board[x+6] != '-':
			return [True, board[x]]
	return [False, 0]
#----------------------------------------------------------------------------------------
def checkDiagonals(board):
	if board[0] == board[4] == board[8] != '-':
		return [True, board[0]]
	if board[2] == board[4] == board[6] != '-':
		return [True, board[2]]
	return [False, 0]
#----------------------------------------------------------------------------------------
def stringBoard(perm, limit): 
	newBoard = '---------'
	for n in range(limit+1):
		if n%2 == 0: 
			newBoard = insertX(newBoard, perm.index(n))
		else:
			newBoard = insertO(newBoard, perm.index(n))
	return newBoard
#----------------------------------------------------------------------------------------
def insertX(newBoard, n):
	return newBoard[0:n] + 'X' + newBoard[(n+1):]
#----------------------------------------------------------------------------------------
def insertO(newBoard, n):
	return newBoard[0:n] + 'O' + newBoard[(n+1):]
#----------------------------------------------------------------------------------------
def printDictionary(dict):
    numkeys = 0
    numvalues = 0
    for k, v in dict.items():
        print('{0}: {1}'.format(k, v))
    print('Number of Keys: ' + str(len(dict)))
#----------------------------------------------------------------------------------------
from random import random
from time import clock; START_TIME = clock(); main();
print (' | %5.6f seconds |' %(clock()-START_TIME))
#----------------------------------------------------------------------------------------