from tkinter import *
from tkinter import messagebox
import random
import time
import math

class Game():
    def __init__(self):
        self.board = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.board2 = []
        self.board2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.board3 = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        self.window = Tk()
        self.window.title('TicTacToe')
        self.window.iconphoto(False, PhotoImage(file='_internal/xoxo.png'))

        self.blank = PhotoImage(file='_internal/blank.png')
        self.blank = self.blank.subsample(3, 3)
        self.ximg = PhotoImage(file='_internal/x.png')
        self.ximg = self.ximg.subsample(3, 3)
        self.x1img = PhotoImage(file='_internal/x1.png')
        self.x1img = self.x1img.subsample(3, 3)
        self.oimg = PhotoImage(file='_internal/o.png')
        self.oimg = self.oimg.subsample(3, 3)
        self.o1img = PhotoImage(file='_internal/o1.png')
        self.o1img = self.o1img.subsample(3, 3)

        self.title = Label(self.window, text='TICTACTOE', font=('Fixedsys', 50, 'bold'))
        self.title.pack()
        self.turnlabel = Label(self.window, font=('Fixedsys', 15, 'bold'))
        self.turnlabel.pack()

        self.turnlabel.config(text="Choose an option")

        frame = Frame(self.window)
        frame.config(pady=1)

        self.comp = Button(frame, text='vs Computer', font=('Fixedsys', 11, 'bold'), bg='grey', command=  lambda t='vs Computer' : self.gamemode(t))
        self.comp.grid(row=0, column=0)
        self.playagain = Button(frame, padx=20, text='Play again?', font=('Fixedsys', 11, 'bold'), bg='grey',
                           command=self.playagain)
        self.playagain.config(state=DISABLED)
        self.playagain.grid(row=0, column=1, padx=20)
        self.pvp = Button(frame, text='vs Player', font=('Fixedsys', 11, 'bold'), bg='grey', command=  lambda t='vs Player' : self.gamemode(t))
        self.pvp.grid(row=0, column=2)

        frame.pack()

        self.score_x = 0
        self.score_o = 0

        frame2 = Frame(self.window)
        self.title2 = Label(frame2, text=f"Score: {self.score_x} - {self.score_o}", font=('Fixedsys', 10, 'bold'),fg= 'grey')
        self.title2.grid(row=0,column=3)

        frame2.pack()

        self.players = None
        self.current_winner = None

    def gamemode(self,t):
        self.pvp.config(state=DISABLED)
        self.comp.config(state=DISABLED)
        self.createboard()
        if t == 'vs Computer':
            self.players = 'Computer'
            self.ai_computers_move()
        if t == 'vs Player':
            self.players = 'X'

        self.turnlabel.config(text=f"{self.players}'s Turn")

    def empty_spaces(self):
        space = 9
        for i in range(3):
            for j in range(3):
                if self.board[i][j]['text'] != ' ':
                    space -= 1
        if space == 0:
            return False
        else:
            return space

    def gui(self,pos,val,current_player):
        self.title2.config(text=f"Score: {self.score_x} - {self.score_o}")

        if pos == 'row':

            for i in range(3):
                if current_player == 'X' or current_player == 'Computer':
                    self.board[val][i]['image'] = self.x1img
                elif current_player == 'O' or current_player == 'Player':
                    self.board[val][i]['image'] = self.o1img
        elif pos == 'column':
            for i in range(3):
                if current_player == 'X' or current_player == 'Computer':
                    self.board[i][val]['image']= self.x1img
                elif current_player == 'O' or current_player == 'Player':
                    self.board[i][val]['image']= self.o1img
        elif pos == 'd1':
            if current_player == 'X' or current_player == 'Computer':
                self.board[0][0]['image'] = self.x1img
                self.board[1][1]['image'] = self.x1img
                self.board[2][2]['image'] = self.x1img
            elif current_player == 'O' or current_player == 'Player':
                self.board[0][0]['image'] = self.o1img
                self.board[1][1]['image'] = self.o1img
                self.board[2][2]['image'] = self.o1img
        elif pos == 'd2':
            if self.board[0][2]['text'] == 'X' or self.board[0][2]['text'] == 'Computer':
                self.board[0][2]['image'] = self.x1img
                self.board[1][1]['image'] = self.x1img
                self.board[2][0]['image'] = self.x1img
            elif self.board[0][2]['text'] == 'O' or self.board[0][2]['text'] == 'Player':
                self.board[0][2]['image'] = self.o1img
                self.board[1][1]['image'] = self.o1img
                self.board[2][0]['image'] = self.o1img
        elif pos == 'tie':
            for i in range(3):
                for j in range(3):
                    if self.board[i][j]['text'] == 'O' or self.board[i][j]['text'] == 'Player':
                        self.board[i][j]['image'] = self.o1img
                    if self.board[i][j]['text'] == 'X' or self.board[i][j]['text'] == 'Computer':
                        self.board[i][j]['image'] = self.x1img

    def available_spaces(self):
        return [i for i, spot in enumerate(self.board2) if spot == ' ']

    def ai_computers_move(self):
        if len(self.available_spaces()) == 9:
            self.computers_move()
        else:
            currentplayer = self.players

            move = self.minimax(player=currentplayer)['position']
            for i in range(3):
                for j in range(3):
                    if self.board3[i][j] == move:
                        self.turn(i, j)

    def minimax(self,player):
        max_player = 'Computer'
        other_player = 'Player' if player == 'Computer' else 'Computer'
        if self.current_winner == other_player:
            return {'position':None,
                    'score': 1 * (self.empty_spaces() + 1) if other_player == max_player else -1 * (self.empty_spaces() + 1)}
        elif not self.empty_spaces():
            return {'position':None,'score':None}

        if player == max_player:
            best = {'position':None,'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}


        for possible_move in self.available_spaces():

            self.turn_minmax(possible_move,player)
            sim_score = self.minimax(other_player)

            self.board2[possible_move] = ' '
            self.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score


        return best

    def computers_move(self):
        move = random.choice(self.available_spaces())
        for i in range(3):
            for j in range(3):
                if self.board3[i][j] == move:
                    self.turn(i,j)

    def checkwinner_minmax(self,move,currentplayer):

        row_ind = move // 3
        row = self.board2[row_ind*3:(row_ind+1)*3]
        if all(spot == currentplayer for spot in row):

            return True

        col_ind = move % 3
        column = [self.board2[col_ind + i*3] for i in range(3)]
        if all(spot == currentplayer for spot in column):

            return True

        if move % 2 ==0:
            diagonal1 = [self.board2[i]for i in [0,4,8]]
            if all(spot == currentplayer for spot in diagonal1):

                return True
            diagonal2 = [self.board2[i]for i in [2,4,6]]
            if all(spot == currentplayer for spot in diagonal2):

                return True
        else:
            return False

    def checkwinner(self):
        current_player = self.players
        for i in range(3):
            if self.board[i][0]['text'] == self.board[i][1]['text'] == self.board[i][2]['text'] != ' ':
                if current_player == 'X' or current_player == 'Computer':
                    self.score_x += 1
                else:
                    self.score_o +=1
                
                self.turnlabel.config(text=f"{self.players} WINS !")
                self.playagain.config(state=NORMAL)
                self.gui('row',i,current_player)
                self.current_winner = current_player

                return True

            elif self.board[0][i]['text'] == self.board[1][i]['text'] == self.board[2][i]['text'] != ' ':
                if current_player == 'X' or current_player == 'Computer':
                    self.score_x += 1
                else:
                    self.score_o += 1
                self.turnlabel.config(text=f"{self.players} WINS !")
                self.playagain.config(state=NORMAL)
                self.gui('column',i,current_player)
                self.current_winner = current_player

                return True

        if self.board[0][0]['text'] == self.board[1][1]['text'] == self.board[2][2]['text'] != ' ':
            if current_player == 'X' or current_player == 'Computer':
                self.score_x += 1
            else:
                self.score_o += 1
            self.turnlabel.config(text=f"{self.players} WINS !")
            self.playagain.config(state=NORMAL)
            self.gui('d1',0,current_player)
            self.current_winner = current_player

            return True

        elif self.board[0][2]['text'] == self.board[1][1]['text'] == self.board[2][0]['text'] != ' ':
            if current_player == 'X' or current_player == 'Computer':
                self.score_x += 1
            else:
                self.score_o += 1
            self.turnlabel.config(text=f"{self.players} WINS !")
            self.playagain.config(state=NORMAL)
            self.gui('d2',0,current_player)
            self.current_winner = current_player
            return True

        elif self.empty_spaces() is False:
            self.turnlabel.config(text="xX DRAW Xx")
            self.playagain.config(state=NORMAL)
            self.gui('tie',0,' ')
            return True
        else:
            return False

    def turn_minmax(self, move,currentplayer):
        if self.board2[move] == ' ':
            self.board2[move] = currentplayer
            if self.checkwinner_minmax(move, currentplayer):
                self.current_winner = currentplayer

            return True

        return False

    def turn(self, i, j):
        if self.board[i][j]['text'] == ' ' and self.checkwinner() is False:
            if self.players == 'Computer':
                self.board[i][j]['image'] = self.ximg
                self.board[i][j]['text'] = self.players
                for row in range(3):
                    for column in range(3):
                        if row == i and column == j:
                            throwaway = self.board3[i][j]
                            self.board2[throwaway] = 'Computer'

                if self.checkwinner() is False:
                    self.players = 'Player'
                    self.turnlabel.config(text=f"{self.players}'s Turn")

            elif self.players == 'Player':
                self.board[i][j]['image'] = self.oimg
                self.board[i][j]['text'] = self.players
                #self.board[i][j] = ' '
                for row in range(3):
                    for column in range(3):
                        if row == i and column == j:
                            throwaway = self.board3[i][j]
                            self.board2[throwaway] = 'Player'

                if self.checkwinner() is False:
                    self.players = 'Computer'
                    self.turnlabel.config(text=f"{self.players}'s Turn")

                    self.ai_computers_move()

            if self.players == 'X':
                self.board[i][j]['image'] = self.ximg
                self.board[i][j]['text'] = self.players
                for row in range(3):
                    for column in range(3):
                        if row == i and column == j:
                            throwaway = self.board3[i][j]
                            self.board2[throwaway] = 'X'

                if self.checkwinner() is False:
                    self.players = 'O'
                    self.turnlabel.config(text=f"{self.players}'s Turn")

            elif self.players == 'O':
                self.board[i][j]['image'] = self.oimg
                self.board[i][j]['text'] = self.players
                for row in range(3):
                    for column in range(3):
                        if row == i and column == j:
                            throwaway = self.board3[i][j]
                            self.board2[throwaway] = 'O'

                if self.checkwinner() is False:
                    self.players = 'X'
                    self.turnlabel.config(text=f"{self.players}'s Turn")

        elif self.board[i][j]['text'] != ' ':
            message = messagebox.showwarning(message="Spot Already Taken!")

    def createboard(self):
        frame = Frame(self.window)
        for i in range(3):
            for j in range(3):
                self.board[i][j] = Button(frame, text=' ',
                                    image=self.blank,
                                    command=lambda i=i, j=j: self.turn(i, j)
                                     )
                self.board[i][j].grid(row=i, column=j)
        frame.pack()



    def playagain(self):
        for i in range(3):
            for j in range(3):
                self.board[i][j].config(text=' ', image=self.blank)
        self.playagain.config(state=DISABLED)
        self.current_winner = None
        if self.players == 'Computer' or self.players == 'Player':
            self.board2 = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            self.players = 'Computer'
            self.ai_computers_move()
        else:
            self.players = 'X'
        self.turnlabel.config(text=f"{self.players}'s Turn")

    def newgame(self):
        self.window.resizable(0, 0)
        self.window.mainloop()

if __name__ == '__main__':
    app = Game()
    app.newgame()