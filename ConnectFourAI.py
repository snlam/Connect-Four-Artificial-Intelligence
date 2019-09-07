#Connect 4 Board
import random
import time
import webbrowser

def sum(L):
	result = 0
    for i in range(len(L)):
        result += L[i]
    return result
    
class Board:
    """A data type representing a Connect-4 board
       with an arbitrary number of rows and columns.
    """

    def __init__(self, width, height):
        """Construct objects of type Board, with the given width and height."""
        self.width = width
        self.height = height
        self.data = [[' ']*width for row in range(height)]

        # We do not need to return anything from a constructor!



    def __repr__(self):
        """This method returns a string representation for an object of type Board.
        """
        H = self.height
        W = self.width
        s = ''                          # the string to return
        for row in range(H):
            s += '|'
            for col in range(W):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*self.width + 1) * '-'   # bottom of the board
        s += '\n'
        for i in range(W):
            s += ' ' + str(i) # and the numbers underneath here
        return s       # the board is complete, return it
    

    def addMove(self, col, ox): 
        """takes 2 arguments: 1st = col: represents index of column to which checker will be added
                               2nd = ox: 1-character string representing checker to add to board  ('X' or 'O')
            returns Board with location
        """
        H = self.height
        for row in range(0, H):
            if self.data[row][col] != ' ':
                self.data[row-1][col] = ox
                return
        self.data[H-1][col] = ox



    def clear(self):
        """should clear the board"""
        H = self.height
        W = self.width
        col = self.width
        for row in range(H):
            if self.data[row][col-1] != ' ':
                self.data[row][col-1] = ' '
            for col in range(W):
                if self.data[row][col]!= ' ':
                    self.data[row][col] = ' '

    
    def setBoard(self, moveString):
        """Accepts a string of columns and places alternating checkers in those columns, starting with 'X'.
                EX// call b.setBoard('012345') to see 'X's and 'O's alternate on bottom row, 
                        or b.setBoard('000000') to see them alternate in the left column.
            moveString must be a string of one-digit integers
        """
        nextChecker = 'X'   # start by playing 'X'
        for colChar in moveString:
            col = int(colChar)
            if 0 <= col <= self.width:
                self.addMove(col, nextChecker)
            if nextChecker == 'X':
                nextChecker = 'O'
            else:
                nextChecker = 'X'


    def allowsMove(self, c):
        """returns True if calling object (of type Board) does allow a move into column c
            returns False if column c is not legal column number for the calling object
            returns False if column c is full (checks to be sure that c is within range from 0 to last column 
                        and make sure that there is still room left in column)
        """
        if c >= self.width or c < 0:
            return False
        elif self.data[0][c]!= ' ':
            return False
        else:
            return True

    
    def isFull(self):
        """returns True if calling object (of type Board) is completely full of checkers
            returns False otherwise
        """
        for i in range(self.width):
            if self.allowsMove(i) == True:
                return False       
        return True


    def delMove(self, c): 
        """remove the top checker from the column c
            If the column is empty, then delMove should do nothing
        """
        H = self.height
        for row in range(H):
            if self.data[row][c] != ' ':
                self.data[row][c] = ' '
                return


    def winsFor(self, ox):
        """Accepts, ox, 1-character checker: either 'X' or 'O'
            returns True if there are 4 checkers of type ox in a row on board; returns False othwerwise
        """
        H = self.height
        W = self.width
        D = self.data
        for x in range(H):
            for y in range(W):
                if inarow_Neast(ox, x, y, D, 4) == True:
                    return True
                elif inarow_Nsouth(ox, x, y, D, 4) == True:
                    return True
                elif inarow_Nnortheast(ox, x, y, D, 4) == True:
                    return True
                elif inarow_Nsoutheast(ox, x, y, D, 4) == True:
                    return True
        return False



    def play(self):
        """hosts a game of Connect Four"""
        print("Welcome to Connect Four! :)")
        print(self)
        while True:
            users_col = -1
            while not self.allowsMove(users_col):
                users_col = int(input("Choose a column (X): "))
                self.addMove(users_col, "X")
                print(self)
                if self.winsFor("X"):
                    print("Game Over!")
                    print("X Wins!")
                    return
                if self.isFull():
                    print("Game Over!")
                    print("It's a TIE!")
                    return

            users_col = -1
            while not self.allowsMove(users_col):
                users_col = int(input("Choose a column (O): "))
                self.addMove(users_col,"O")
                print(self)
                if self.winsFor("O"):
                    print("Game Over!")
                    print("O Wins!")
                    return
                if self.isFull():
                    print("Game Over!")
                    print("It's a TIE!")
                    return



    def colsToWin(self, ox):
        """accepts one argument, ox, either string 'X' or string 'O' (two possible checkers in the game)
            returns list of columns where ox can move in next turn in order to win and finish game
                columns should be in numeric order (if there are more than one)
        """
        W = self.width
        wins = []
        for a in range(W):
            if self.allowsMove(a) == True:
                self.addMove(a, ox) 
                if self.winsFor(ox) == True:
                    wins.append(a)
                self.delMove(a)
        return wins



    def aiMove(self, ox):
        """accepts one argument, ox, either string 'X' or string 'O' (two possible checkers in the game)
            returns single integer, which must be a legal column in which to make a move AND
                If ox can win, then MUST return that move (that column number). If more than one way to win: return any one of winning columns 
                If NO way for ox to win, but ox can block the opponent's win, then MUST return a move that blocks it. 
                    should not look more than one move ahead for its opponent. If no wins, but multiple ways to block opponent, then return 
                    any one of those ways to block the opponent. (Even though the opponent might win in a different way.)
                If NO way for ox to win NOR a way for ox to block opponent from winning, then return move of your (the programmer's) choice—but 
                it must be a legal move. We won't call aiMove when the board is full.
        """
        H = self.height
        W = self.width
        D = self.data
        if self.colsToWin(ox) != []:
            return random.choice(self.colsToWin(ox))
        else:
            if ox == 'X':
                i = 'O'
                if self.colsToWin(i) != []:    
                    return random.choice(self.colsToWin(i))
            elif ox == 'O':
                i = 'X'
                if self.colsToWin(i) != []:    
                    return random.choice(self.colsToWin(i))
            for x in range(H):
                for y in range(W):
                    if inarow_Neast(ox, x, y, D, 2) == True:
                        if self.allowsMove(y+2) == True:
                            return y+2
                        if self.allowsMove(y-1) == True:
                            return y-1
                    elif inarow_Nsouth(ox, x, y, D, 2) == True:
                        if self.allowsMove(y) == True:
                            return y
                    elif inarow_Nnortheast(ox, x, y, D, 2) == True:
                        if self.allowsMove(y+1) == True:
                            return y+1
                    elif inarow_Nsoutheast(ox, x, y, D, 2) == True:
                        if self.allowsMove(y-1) == True:
                            return y-1
            else:
                if self.allowsMove(3) == True:
                    return 3
                elif self.allowsMove(4) == True:
                    return 4
                elif self.allowsMove(5) == True:
                    return 5
                elif self.allowsMove(2) == True:
                    return 2
                elif self.allowsMove(1) == True:
                    return 1
                elif self.allowsMove(6) == True:
                    return 6
                elif self.allowsMove(0) == True:
                    return 0



    def hostGame(self):
        """hosts a game of Connect Four with AI"""
        print("Welcome to Connect Four! :)" )
        print(self)
        while True:
            users_col = -1
            while not self.allowsMove(users_col):
                users_col = int(input("Choose a column (X): "))
                self.addMove(users_col, "X")
                print(self)
                if self.winsFor("X"):
                    print("Game Over!")
                    print("X Wins!")
                    return
                if self.isFull():
                    print("Game Over!")
                    print("It's a TIE!")
                    return

            users_col = -1
            while not self.allowsMove(users_col):
                users_col = self.aiMove('O')
                self.addMove(users_col,"O")
                print(self)
                if self.winsFor("O"):
                    print("Game Over!")
                    print("O Wins!")
                    return
                if self.isFull():
                    print("Game Over!")
                    print("It's a TIE!")
                    return
    
    def playGame(self, px, po):
        """calls nextMove method for two objects of type Player to play a game
                objects are named px and po
                Human mode allows one computer and one human. Computer mode has 
                two computers and grutor mode plays a video. If none are chosen,
                it will play another video.
        """
        print("Welcome to Connect Four! \n")        
        user_type = input("Play as a Human or Computer...or GRUTOR? ")
        while True:      
            if user_type == "Human":              
                print(self)
                user_col = input("Choose your column: ")
                try:
                    col = int(user_col)
                except ValueError:
                    user_col = input("Choose another column: ")
                while not self.allowsMove(col):
                    print("That's not possible.")
                    user_col = input("Choose your column: ")
                    col = int(user_col)
                self.addMove(col, px.ox)

                if self.winsFor(px.ox) == True:
                    print("You win! Congratulations!")
                    break

                print(self)

                time.sleep(1)

                print("It's my turn now...thinking for a very short time...")
                col = po.nextMove(self)
                self.addMove(col, po.ox)

                if self.winsFor(po.ox) == True:
                    print("HAHAHAHAHA I HAVE OUTWITTED YOU, MEASLY HUMAN.")
                    print("First stop, Connect Four \ntomorrow...THE WORLD!")
                    break
            elif user_type == "Computer":
                print(self)

                print("X's turn")
                col = px.nextMove(self)
                self.addMove(col, px.ox)

                if self.winsFor(px.ox) == True:
                    print("X wins!")
                    break

                print(self)

                time.sleep(1)

                print("O's turn")
                col = po.nextMove(self)
                self.addMove(col, po.ox)

                if self.winsFor(po.ox) == True:
                    print("O wins!")
                    break
            elif user_type == "GRUTOR":
                webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                break
            else:
                print("Neither!! Amazing. Here's a video you should watch: https://www.youtube.com/watch?v=PFrPrIxluWk :)")
                webbrowser.open_new("https://www.youtube.com/watch?v=PFrPrIxluWk")
                break
                
        print(self)

    def playGameChance(self, px, po, chance):
        """calls nextMove method for two objects of type Player to play a game
                objects are named px and po. 
                Using a chance between 0 and 1 (floating point value), a move
                may be randomly ignored for another allowable move. 
                Human mode allows one computer and one human. Computer mode has 
                two computers and grutor mode plays a video. If none are chosen,
                it will play another video.
        """
        print("Welcome to Connect Four! \n")        
        user_type = input("Play as a Human or Computer...or GRUTOR? ")
        while True:      
            if user_type == "Human":              
                print(self)
                user_col = input("Choose your column: ")
                try:
                    col = int(user_col)
                except ValueError:
                    user_col = input("Choose another column: ")
                while not self.allowsMove(col):
                    print("That's not possible.")
                    user_col = input("Choose your column: ")
                    col = int(user_col)
                i = random.uniform(0,1)             #choose a random floating point number between 0 and 1
                if i <= chance:                     #if i is less than chance, move will be ignored and a random move will be played
                    new_col = random.randint(0,6)
                    print("HahA, i cHowoIsEd A nUwu CowoLeMnd: ", new_col, ".")
                    self.addMove(new_col, px.ox)
                else:
                    self.addMove(col, px.ox)

                if self.winsFor(px.ox) == True:
                    print("You win! Congratulations!")
                    break

                print(self)

                time.sleep(1)

                print("It's my turn now...thinking for a very short time...")
                col = po.nextMove(self)
                i = random.uniform(0,1) 
                if i <= chance:
                    new_col = random.randint(0,6)
                    print("HahA, i cHowoIsEd A nUwu CowoLeMnd: ", new_col, ".")
                    self.addMove(new_col, po.ox)
                else:
                    self.addMove(col, po.ox)

                if self.winsFor(po.ox) == True:
                    print("HAHAHAHAHA I HAVE OUTWITTED YOU, MEASLY HUMAN.")
                    print("First stop, Connect Four \ntomorrow...THE WORLD!")
                    break

            elif user_type == "Computer":
                print(self)

                print("X's turn")
                col = px.nextMove(self)
                i = random.uniform(0,1)             #choose a random floating point number between 0 and 1
                if i <= chance:                     #if i is less than chance, move will be ignored and a random move will be played
                    new_col = random.randint(0,6)
                    print("HahA, i cHowoIsEd A nUwu CowoLeMnd: ", new_col, ".")
                    self.addMove(new_col, px.ox)
                else:
                    self.addMove(col, px.ox)

                if self.winsFor(px.ox) == True:
                    print("X wins!")
                    break

                print(self)

                time.sleep(1)

                print("O's turn")
                col = po.nextMove(self)
                i = random.uniform(0,1) 
                if i <= chance:
                    new_col = random.randint(0,6)
                    print("HahA, i cHowoIsEd A nUwu CowoLeMnd: ", new_col, ".")
                    self.addMove(new_col, po.ox)
                else:
                    self.addMove(col, po.ox)

                if self.winsFor(po.ox) == True:
                    print("O wins!")
                    break
            elif user_type == "GRUTOR":
                webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                break
            else:
                print("Neither!! Amazing. Here's a video you should watch: https://www.youtube.com/watch?v=PFrPrIxluWk :)")
                webbrowser.open_new("https://www.youtube.com/watch?v=PFrPrIxluWk")
                break
                
        print(self)

def inarow_Neast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading east and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True

def inarow_Nsouth(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading south and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True

def inarow_Nnortheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading northeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start - (N-1) < 0 or r_start > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start-i][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True

def inarow_Nsoutheast(ch, r_start, c_start, A, N):
    """Starting from (row, col) of (r_start, c_start)
       within the 2d list-of-lists A (array),
       returns True if there are N ch's in a row
       heading southeast and returns False otherwise.
    """
    H = len(A)
    W = len(A[0])
    if r_start < 0 or r_start + (N-1) > H - 1:
        return False # out of bounds row
    if c_start < 0 or c_start + (N-1) > W - 1:
        return False # o.o.b. col
    # loop over each location _offset_ i
    for i in range(N):
        if A[r_start+i][c_start+i] != ch: # a mismatch!
            return False
    return True  # all offsets succeeded, so we return True












class Player:
    """An AI player for Connect Four."""

    def __init__(self, ox, tbt, ply):
        """Construct a player for a given checker, tie-breaking type,
           and ply."""
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """Create a string represenation of the player."""
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self): 
        """return other kind of checker or playing piece, i.e., piece being played by self's opponent
            if self is playing 'X', this method returns 'O' and vice-versa
        """
        if self.ox == 'X':
            return 'O'
        elif self.ox == 'O':
            return 'X'
        else:
            return "ERROR! Choose 'X' or 'O'!"
        
    def scoreBoard(self, b):
        """return single float value representing score of input b, which you may assume will be object of type Board
           return 100.0 if board b is win for self
           return 50.0 if neither win nor loss for self
           return 0.0 if loss for self (i.e., opponent won)
        """
        ox = self.ox 
        if b.winsFor(ox) == True:
            return 100.0
        elif b.winsFor(self.oppCh()) == True:
            return 0.0
        else:
            return 50.0

    def tiebreakMove(self, scores):
        """accepts scores, nonempty list of floating-point numbers
           if only 1 highest score in scores, return COLUMN number, not score
           if 1+ highest score because tie, return COLUMN number of highest score appropriate to player's tiebreaking type
                if tiebreaking type == 'LEFT', return column of leftmost highest score 
                if tiebreaking type == 'RIGHT', return column of rightmost highest score 
                if tiebreaking type == 'RANDOM', return column of randomly-chosen highest score
        """
        m = max(scores)
        col = []
        for x in range(0,7):
            if scores[x] == m:
                col += [x] #adds into list the column number of the highest score
        if self.tbt == "LEFT":
            return col[0]
        elif self.tbt == "RIGHT": 
            return col[-1]
        elif self.tbt == "RANDOM":             
            return col[random.choice(range(len(col)))]
        else: 
            print("Choose a tie-breaking type of LEFT, RIGHT, or RANDOM.")

    def scoresFor(self, b):
        """ heart of Player class
            return list of scores, with cth score representing "goodness" of input board after player moves to column c
        """
        scores = [50]*b.width
        for x in range(b.width):
            if b.allowsMove(x) == False:
                scores[x] = -1
            elif b.winsFor(self.ox) == True:
                scores[x] = 100.0
            elif b.winsFor(self.oppCh()) == True:
                scores[x] = 0
            elif self.ply == 0:
                scores[x] = self.scoreBoard(b)
            else:
                b.addMove(x, self.ox)
                op = Player(self.oppCh(), self.tbt, self.ply - 1)
                opscore = op.scoresFor(b)
                scores[x] = 100.0 - max(opscore)
                b.delMove(x)
        return scores

    def nextMove(self, b):
        """accepts b, object of type Board
           returns integer—namely, column number that calling object (of class Player) chooses to move to
        """
        scores = self.scoresFor(b)
        return self.tiebreakMove(scores)