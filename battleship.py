
import sys
import random

def checkShip(shipfile, width, height):
	content = shipfile.readlines()
    
    #if symbols contain element in theList, exit
	ship = []
	theList = ['x','X','o','O','*']
	for row in content:
		tmp = row.strip().split()
		if tmp[0] in theList:
			print("Error Can not use %s as symbol. Terminating game"%(tmp[0]))
			sys.exit(0)
		ship.append(tmp)
	
	#if user did not put ship on board or place ship diagonally, exit
	symbols = []
	for row in ship:
		symbols.append(row[0])
		if len(row) != 5:
			print("Error %s is not placed on board. Teminating game"%(row[0]))
			sys.exit(0)
		if(row[1] != row[3] and row[2] != row[4]):
			print("Ships cannot be placed diagonally. Terminating game.")
			sys.exit(0)

	#if several ships have the same symbol, exit
	if len(symbols) > len(set(symbols)):
		dup = list(set([x for x in symbols if symbols.count(x) > 1]))
		print('Error symbol %s is already in use. Terminating game'%(dup[0]))
		sys.exit(0)

	#construct user board and check if ships are on top of others 
	user_board = []
	for i in range(height):
		user_board.append(['*']*width)

	length = []
	for row in ship:
		try:
			r1 = int(row[1])
			r2 = int(row[3])
			c1 = int(row[2])
			c2 = int(row[4])
		except ValueError:
			print("Error %s Can not be placed on board. Terminating game."%(row[0]))
			sys.exit(0)

		
		#if row index or column index larger than height or width, exit
		if(r1 >= height or r2 >= height or c1 >= width or c2 >= width or r1 < 0 or r2 < 0 or c1 < 0 or c2 < 0):
			print("Error %s is placed outside of the board. Terminating game."%(row[0]))
			sys.exit(0)

		if r1 == r2:
			# horz ship
			if c1 == c2:
				if user_board[r1][c1] == '*':
					user_board[r1][c1] = row[0]
					length.append(1)
				else:
					print("There is already a ship at location %d, %d. Terminating game."%(r1, c1))
					sys.exit(0)
			else:
				minc = min(c1, c2)
				maxc = max(c1, c2)
				length.append(maxc - minc + 1)
				for index in range(maxc - minc + 1):
					if user_board[r1][minc + index] == '*':
						user_board[r1][minc + index] = row[0]
					else:
						print("There is already a ship at location %d, %d. Terminating game."%(r1, minc + index))
						sys.exit(0)
		else:
			#vert board
			minr = min(r1, r2)
			maxr = max(r1, r2)
			length.append(maxr - minr + 1)
			for index in range(maxr - minr + 1):

				if(user_board[minr + index][c1] == '*'):
					user_board[minr + index][c1] = row[0]
				else:
					print("There is already a ship at location %d, %d. Terminating game."%(minr + index, c1))
					sys.exit(0)

	return(user_board, symbols, length)

def constructAIBoard(width, height, symbols,length,seed):
	#random.seed(seed)

	ord = sorted(range(len(symbols)), key = symbols.__getitem__)
	symbols = [symbols[x] for x in ord]
	length = [length[x] for x in ord]


	AI_board = []
	for u in range(height):
		AI_board.append(['*']*width)
	suc = True

	for i in range(len(symbols)):
		#s is the symbol of that ship and l is its length
		l = length[i]
		s = symbols[i]

		direction = random.choice(['vert', 'horz'])
		while True:
			if(direction == 'horz'):
				r = random.randint(0, height - 1)
				c1 = random.randint(0, width - l)
				if AI_board[r][c1:(c1+l)] == ['*']*l:
					AI_board[r][c1:(c1+l)] = [s]*l
					print("Placing ship from %d,%d to %d,%d."%(r,c1,r,c1+l-1))
					break
				else:
					direction = random.choice(['vert', 'horz'])
			else:
				r1 = random.randint(0, height - l)
				c1 = random.randint(0, width - 1)
				subsuc = True
				for m in range(l):
					if(AI_board[r1 + m][c1] != '*'):
						subsuc = False
						break
				if subsuc == False:
					direction = random.choice(['vert', 'horz'])
				else:
					for m in range(l):
						AI_board[r1 + m][c1] = s
					print("Placing ship from %d,%d to %d,%d."%(r1,c1,r1 + l - 1,c1))
					break
	
	return(AI_board)



def is_game_over(user_board, AI_board, numShips):
    return user_win(AI_board, numShips) or AI_win(user_board, numShips)

def user_win(AI_board, numGrids):  #numShips = sum(length)
    #if the about of 'X' equals to sum(length) then all ships got sunk by AI
    # sum(length) is the total amount of alphabets were placed on the board initially
    if sum([l.count('X') for l in AI_board]) == numGrids:
        return True
    else:
        return False


def AI_win(user_board, numGrids):
    if sum([l.count('X') for l in user_board]) == numGrids:
        return True
    else:
        return False

def print_all(AI_board, user_board):
	print('Scanning Board')
	print_hidden_board(AI_board)
	print()
	print('My Board')
	print_board(user_board)
	print()


def print_board(board):
    print(' '*2, end = '')
    for i in range(len(board[0])):
    	#print i ,
        print(i, end=' ')
    #print
    print()
    for row_num, row in enumerate(board):
    	#print row_num ,
        print(row_num, end = ' ')
        for r in row:
        	#print r ,
            print(r, end = ' ')
        #print
        print()

def print_hidden_board(board):
	#print ' ',
	print(' '*2, end = '')
	for i in range(len(board[0])):
		#print i ,
		print(i, end =' ')
	#print
	print()
	for row_num, row in enumerate(board):
		print(row_num, end = ' ')
		#print row_num ,
		for r in row:
			if r == 'X' or r == 'O' or r =='x' or r == 'o':
				#print r ,
				print(r, end = ' ')
			else:
				#print '*' ,
				print('*', end = ' ')
		#print
		print()



def get_user_move(AI_board):
	play = input('Enter row and column to fire on separated by a space: ').strip()

	while not valid_play(play, AI_board):
		play = input('Enter row and column to fire on separated by a space: ').strip()

	row, col = play.split()
	row = int(row)
	col = int(col)
	return(row, col)

def valid_play(play, board):
	"""Return true if the play is valid on this board and False otherwise"""
	# play is a string that contains two numbers seperated by a space
	play = play.split()
	if(len(play)!=2):
		return False
	row, col = play
	if not (row.isdigit() and col.isdigit()):
		return False
	row = int(row)
	col = int(col)

	# Make sure the input location index does not go out the board boundary
	if not ((0<= row < len(board)) and (0<=col<len(board[0]))):
		return False
	# Make sure the input location hasn't been fired before
	if (board[row][col] == 'X') or (board[row][col] == 'O' or board[row][col] == 'x' or board[row][col] == 'o') :
		return False

	return True

def get_AI_hunt_move(user_board):
	width = len(user_board[0])
	height = len(user_board)
	unfireLoc = []
	for i in range(height):
		for j in range(width):
			if not (user_board[i][j] == 'X' or user_board[i][j] == 'O' or user_board[i][j] == 'x' or user_board[i][j] == 'o'):
				unfireLoc.append([i, j])

	row, col = random.choice(unfireLoc)
	return(row, col)

def get_AI_cheating_move(user_board):
	#random.seed(seed)
	width = len(user_board[0])
	height = len(user_board)
	for i in range(height):
		for j in range(width):
			if not (user_board[i][j] == '*' or user_board[i][j] == 'X' or user_board[i][j] == 'O' or user_board[i][j] == 'x' or user_board[i][j] == 'o'):
				return(i, j)


def get_AI_destory_move(user_board, destoryList, destoryMode):
	[rol, col] = destoryList[0]
	suc = True
	while user_board[rol][col] == 'X' or user_board[rol][col] == 'O' or user_board[rol][col] == 'x' or user_board[rol][col] == 'o':
		del(destoryList[0])
		if len(destoryList) > 0:
			[rol, col] = destoryList[0]
		else:
			suc = False
			break

	if suc == True:
		del(destoryList[0])
		destoryMode = False
		return(rol, col, destoryList, destoryMode)
	else:
		[rol, col] = get_AI_hunt_move(user_board)
		destoryMode = False
		return(rol, col, destoryList, destoryMode)




def main():
	while True:
		try:
			seed = int(input('Enter the seed: '))
			break
		except ValueError:
			continue

	while True:
		try:
			width = int(input('Enter the width of the board: '))
			if( width < 1):
				continue
			break
		except ValueError:
			continue
			

	while True:
		try:
			height = int(input('Enter the height of the board: '))
			if( height < 1):
				continue
			break
		except ValueError:
			continue

	#check the file containing the user's ship placements
	shipFilename = input("Enter the name of the file containing your ship placements: ")
	try:
		shipfile = open(shipFilename)
	except IOError as e:
		print("Can not open the file")
		sys.exit(0)

	
	while True:
		try:
			print('Choose your AI. \n1. Random \n2. Smart \n3. Cheater')
			numAI = int(input(' Your choice: '))
			if( numAI != 1 and numAI != 2 and numAI != 3):
				continue
			break
		except ValueError:
			continue

	[user_board, symbols, length] = checkShip(shipfile, width, height)

	numGrids = sum(length)


	

	#construct the AI board
	random.seed(seed)
	AI_board = constructAIBoard(width, height, symbols,length, seed)

	
	# user_board and AI_board have be constructed.
    #if random.randint is 0, player first; else AI first
    #Seed the random number generator with seed

	player_turn = random.randint(0,1)
	destoryMode = False
	destoryList = []

	
	#play until game is over
	while not is_game_over(user_board, AI_board, numGrids):
		if player_turn == 0:
			player_turn = 1
			print_all(AI_board, user_board)
			#user play
			#get row and column number which user want to hit
			rol, col = get_user_move(AI_board)
			if AI_board[rol][col] != '*':
				tmp = AI_board[rol][col]
				AI_board[rol][col] = 'X'
				if sum([l.count(tmp) for l in AI_board]) == 0:
					print('You sunk my %s'%(tmp))
				else:
					print('Hit!')
			else:
				print("Miss!")
				AI_board[rol][col] = 'O'
			if user_win(AI_board, numGrids):
				print_all(AI_board, user_board)
				print('You win!')
				sys.exit(0)
		else:
			player_turn = 0
			if numAI == 1:
				rol, col = get_AI_hunt_move(user_board)	
			elif numAI == 2:
				if destoryMode == False:
					rol, col = get_AI_hunt_move(user_board)	
				else:
					[rol, col, destoryList, destoryMode] = get_AI_destory_move(user_board, destoryList, destoryMode)
					#print("%d %d"%(rol, col))
			else:
				rol, col = get_AI_cheating_move(user_board)
			
			print("The AI fires at location (%d, %d)"%(rol, col))
			if user_board[rol][col] != '*':
				tmp = user_board[rol][col]
				user_board[rol][col] = 'X'
				if sum([l.count(tmp) for l in user_board]) == 0:
					print('You sunk my %s'%(tmp))
				else:
					print('Hit!')
			else:
				print("Miss!")
				user_board[rol][col] = 'O'
			if AI_win(user_board, numGrids):
				print_all(AI_board, user_board)
				print('The AI wins.')
				sys.exit(0)

			if numAI == 2:
				if user_board[rol][col] == 'X':
					if rol > 0:
						if not (user_board[rol - 1][col] == 'X' or user_board[rol - 1][col] =='O' or user_board[rol - 1][col] =='x' or user_board[rol - 1][col] =='o'):
							if destoryList.count([rol - 1, col]) == 0:
								destoryList.append([rol - 1, col])

					if rol < (height - 1):
						if not (user_board[rol + 1][col] == 'X' or user_board[rol + 1][col] == 'O' or user_board[rol + 1][col] == 'x' or user_board[rol + 1][col] == 'o'):
							if destoryList.count([rol + 1, col]) == 0:
								destoryList.append([rol + 1, col])
					if col > 0:
						if not (user_board[rol][col - 1] == 'X' or user_board[rol][col - 1] == 'O' or user_board[rol][col - 1] == 'x' or user_board[rol][col - 1] == 'o'):
							if destoryList.count([rol, col - 1]) == 0:
								destoryList.append([rol, col - 1])
					if col < (width - 1):
						if not (user_board[rol][col + 1] == 'X' or user_board[rol][col + 1] == 'O' or user_board[rol][col + 1] == 'x' or user_board[rol][col + 1] == 'o'):
							if destoryList.count([rol, col + 1]) == 0:
								destoryList.append([rol, col + 1])
				if(len(destoryList) > 0):
					destoryMode = True



if __name__ == '__main__':
	main()