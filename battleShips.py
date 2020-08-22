import tkinter as tk
import random
# Design Pattern Singleton. Beim Singleton können mehrere Clients auf eine Instanz 
# einer Klasse zugreifen. Es ist dabei wichtig, dass die Clients die gleiche 
# Instanz betrachten und nicht jeder eigene Instanzen besitzt. Das Singleton Entwurfsmuster 
# bewirkt, dass nur eine Instanz der Klasse erstellt werden kann. Die Klasse GameBoard
# besitzt diese Eigenschaften und dient als Singleton Klasse.

squeareWidth = 20
squareHeigth = 20
squareNumber = 10
gameState = 0

root = tk.Tk(className="Battleships")
btn_text = tk.StringVar()
btn_text.set("Start")

class Player(object):
    # One battleship with length of 5
    battleshipX = None
    battleshipY = None
    # Two cruiser with length of 4
    cruiserX = [None] * 2
    cruiserY = [None] * 2 
    # Three destroyer with length of 3
    destroyerX = [None] * 3
    destroyerY = [None] * 3
    # Four submarines with length of 2
    submarineX = [None] * 4
    submarineY = [None] * 4

class RealPlayer(Player):
    binCanvas = [0] * squareNumber
    for i in range(squareNumber):
        binCanvas[i] = [0] * squareNumber
    name = "Own Territory"
    location = 2
    tk.Label(root, text = name).grid(row = location)
    canvas = tk.Canvas(root, width=squeareWidth*squareNumber, height=squareHeigth*squareNumber)
    canvas.grid(row = location + 1)        
    def pickCoordinates(self):
        return

class Computer(Player):
    binCanvas = [0] * squareNumber
    for i in range(squareNumber):
        binCanvas[i] = [0] * squareNumber
    name = "Computer"
    location = 0
    tk.Label(root, text = name).grid(row = location)
    canvas = tk.Canvas(root, width=squeareWidth*squareNumber, height=squareHeigth*squareNumber)
    canvas.grid(row = location + 1)
    def pickCoordinates(self):
        return

class GameBoard:
    computerPlayer = Computer()
    realPlayer = RealPlayer()
    members = [computerPlayer, realPlayer] # Computer = 0 You = 1
    turn = 0
    gameOver = 0
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if GameBoard.__instance == None:
            GameBoard()
        return GameBoard.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if GameBoard.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GameBoard.__instance = self        
        return
        
    def showFields(self, player):
        for y in range (squareNumber):
            for x in range (squareNumber):
                if self.members[player].binCanvas[x][y] == 1:
                    self.members[player].canvas.create_rectangle(x*squeareWidth,y*squareHeigth, (x*squeareWidth) +  squeareWidth ,(y*squareHeigth) + squareHeigth, fill="grey")
                if self.members[player].binCanvas[x][y] == 0:
                    self.members[player].canvas.create_rectangle(x*squeareWidth,y*squareHeigth,(x*squeareWidth) +  squeareWidth ,(y*squareHeigth) + squareHeigth, fill="white")
                if player == 1:    
                    if self.members[player].binCanvas[x][y] == 2:
                        self.members[player].canvas.create_rectangle(x*squeareWidth,y*squareHeigth,(x*squeareWidth) +  squeareWidth ,(y*squareHeigth) + squareHeigth, fill="green")
                else:
                    if self.members[player].binCanvas[x][y] == 2:
                        self.members[player].canvas.create_rectangle(x*squeareWidth,y*squareHeigth,(x*squeareWidth) +  squeareWidth ,(y*squareHeigth) + squareHeigth, fill="white")
                if self.members[player].binCanvas[x][y] == 3:
                    self.members[player].canvas.create_rectangle(x*squeareWidth,y*squareHeigth,(x*squeareWidth) +  squeareWidth ,(y*squareHeigth) + squareHeigth, fill="red")
    
    def shoot(self, x, y, player):
        if x < 0 or y < 0 or x > 9 or y > 9:
            return 1
        hit = 0
        print("Player: ",  type(self.members[player]), " X: ", x, " Y: ", y)
        if self.members[player].binCanvas[x][y] == 1 or self.members[player].binCanvas[x][y] == 3:
            hit = 1
            return hit
        if self.members[player].binCanvas[x][y] == 0:
            self.members[player].binCanvas[x][y] = 1
            hit = 2
        if self.members[player].binCanvas[x][y] == 2:
            self.members[player].binCanvas[x][y] = 3
            hit = 3

        self.showFields(player)
        if hit == 2:
            if self.turn == 1:
                self.turn = 0
            else:
                self.turn = 1
            return hit
        else:
            return hit

    def setFieldsRandom(self, length, player):
        while True:
                crossing = False
                direction = random.randint(0,1)
                x = random.randint(0, 9-length) if direction == 0 else random.randint(0,9)
                y = random.randint(0, 9-length) if direction == 1 else random.randint(0,9)
                print("Direction ", direction, " Length: ", length, " X: ", x, " Y: ", y)
                for i in range (0, length):
                    print(" i: ", i )
                    if direction == 1:
                        if x > 0 and x < 9 and (self.members[player].binCanvas[x+1][y+i] == 2 or self.members[player].binCanvas[x-1][y+i] == 2):
                            crossing = True
                        if y > 0 and y < 9 and (self.members[player].binCanvas[x][y+i+1] == 2 or self.members[player].binCanvas[x][y-1] == 2):
                            crossing = True
                        if self.members[player].binCanvas[x][y+i] == 2:
                            crossing = True
                        if x == 0 and (self.members[player].binCanvas[x+1][y+i] == 2):
                            crossing = True
                        if x == 9 and (self.members[player].binCanvas[x-1][y+i] == 2):
                            crossing = True
                        if y == 0 and (self.members[player].binCanvas[x][y+1+i] == 2):
                            crossing = True
                        if y == 9 and (self.members[player].binCanvas[x][y-1] == 2):
                            crossing = True
                    else:
                        if y > 0 and y < 9 and (self.members[player].binCanvas[x+i][y+1] == 2 or self.members[player].binCanvas[x+i][y-1] == 2):
                            crossing = True
                        if x > 0 and x < 9 and (self.members[player].binCanvas[x+i+1][y] == 2 or self.members[player].binCanvas[x-1][y] == 2):
                            crossing = True
                        if self.members[player].binCanvas[x+i][y] == 2:
                            crossing = True
                        if y == 0 and (self.members[player].binCanvas[x+i][y+1] == 2):
                            crossing = True
                        if y == 9 and (self.members[player].binCanvas[x+i][y-1] == 2):
                            crossing = True
                        if x == 0 and (self.members[player].binCanvas[x+i+1][y] == 2):
                            crossing = True
                        if x == 9 and (self.members[player].binCanvas[x-1][y] == 2):
                            crossing = True
                if crossing: 
                    continue
                for i in range (0,length):
                    if direction == 1:
                        self.members[player].binCanvas[x][y+i] = 2
                    else:
                        self.members[player].binCanvas[x+i][y] = 2
                break

    def choose(self, player):
        for i in range(5, 1, -1):
            for x in range(0,6-i):
                self.setFieldsRandom(i,player)



    def play(self):
        self.choose(0)
        self.choose(1)
        self.showFields(0)
        self.showFields(1)
        hit = 1
        hitX = 0
        hitY = 0
        direction = 0
        changeDirection = 0
        while not self.gameOver:
            if self.turn == 0:
                self.members[0].canvas.bind('<Button-1>', self.realPlayerShoot)
                root.update()
            else:
                self.members[0].canvas.unbind('<Button-1>')
                if direction == 0:
                    if hit == 1 or hit == 2:
                        modCheck = 0
                        while True:
                            x = random.randrange(0,9)
                            y = random.randrange(0,9)

                            if y != 0 and x > y and x % y == 0:
                                continue
                            if x != 0 and y > x and y % x == 1:
                                continue
                            if not self.members[1].binCanvas[x][y] == 1 or self.members[1].binCanvas[x][y] == 3:
                                break
                            print("MOIN")
                        print("x: ", x, "y: ", y, "Random")
                        hit = self.shoot(x, y, 1)
                        hitX = x
                        hitY = y
                    if hit == 3:
                        while True:
                            trigger = self.shoot(hitX -1, hitY, 1)
                            if trigger == 2: 
                                break
                            elif trigger == 3:
                                direction = 1
                                hit = 1
                                break
                            trigger = self.shoot(hitX + 1, hitY, 1)
                            if trigger == 2: 
                                break
                            elif trigger == 3:
                                direction = 2
                                hit = 1
                                break
                            trigger = self.shoot(hitX, hitY -1, 1)
                            if trigger == 2: 
                                break
                            elif trigger == 3:
                                direction = 3
                                hit = 1
                                break
                            trigger = self.shoot(hitX, hitY +1, 1)
                            if trigger == 2: 
                                break
                            elif trigger == 3:
                                direction = 4
                                hit = 1
                                break
                elif changeDirection < 2:
                    counter = 0
                    if changeDirection == 0:
                        counter = 2
                    else:
                        counter = 1
                    while True and counter < 5:
                        if direction == 1:
                            trigger = self.shoot(hitX - counter, hitY, 1)
                            if trigger == 2 or trigger == 1:
                                direction = 2
                                changeDirection = changeDirection + 1
                                break
                            else:
                                counter = counter + 1
                        if direction == 2:
                            trigger = self.shoot(hitX + counter, hitY, 1)
                            if trigger == 2 or trigger == 1:
                                direction = 1
                                changeDirection = changeDirection + 1
                                break
                            else:
                                counter = counter + 1
                        if direction == 3:
                            trigger = self.shoot(hitX, hitY  - counter, 1)
                            if trigger == 2 or trigger == 1:
                                direction = 4
                                changeDirection = changeDirection + 1
                                break
                            else:
                                counter = counter + 1
                        if direction == 4:
                            trigger = self.shoot(hitX, hitY + counter, 1)
                            if trigger == 2 or trigger == 1:
                                direction = 3
                                changeDirection = changeDirection + 1
                                break
                            else:
                                counter = counter + 1
                if direction > 0 and changeDirection > 1:
                    hit = 1
                    changeDirection = 0
                    direction = 0
                        
                        

                root.update()

    def realPlayerShoot(self, event):
        self.shoot(int(event.x/squeareWidth), int(event.y/squareHeigth), 0)

gameBoard = GameBoard()
gameBoard.play()
root.mainloop()

# BINDING AND UNBINDING CHEAT SHEET
#self.btn_funcid = self.DrawArea.bind("<Button 1>", self.my_button_callback, "+")

# Then some time later, to remove just the 'my_button_callback':
#self.DrawArea.unbind("<Button 1>", self.btn_funcid)

# But if you want to remove all of the callbacks for the event:
#self.DrawArea.unbind("<Button 1>")
#canvas.bind('<Button-1>', drawEnemy)
# def drawEnemy(event):
#     gameBoard.shoot(event.x, event.y)

# def motion(event):
#     mouseX, mouseY = event.x, event.y