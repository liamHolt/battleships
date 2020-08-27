import tkinter as tk
import random
import copy

# Design Pattern Singleton. Beim Singleton können mehrere Clients auf eine Instanz 
# einer Klasse zugreifen. Es ist dabei wichtig, dass die Clients die gleiche 
# Instanz betrachten und nicht jeder eigene Instanzen besitzt. Das Singleton Entwurfsmuster 
# bewirkt, dass nur eine Instanz der Klasse erstellt werden kann. Die Klasse GameBoard
# besitzt diese Eigenschaften und dient als Singleton Klasse.

squeareWidth = 30
squareHeigth = 30
squareNumber = 10

root = tk.Tk(className="Battleships")
btn1_text = tk.StringVar()
btn2_text = tk.StringVar()
btn3_text = tk.StringVar()
btn4_text = tk.StringVar()



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
    pickedOnesX = []
    pickedOnesY = []
    name = "Own Territory"
    location = 2
    tk.Label(root, text = name).grid(row = location)
    canvas = tk.Canvas(root, width=squeareWidth*squareNumber, height=squareHeigth*squareNumber)
    canvas.grid(row = location + 1) 
    shipsLeft = 10       
    def pickCoordinates(self):
        return

class Computer(Player):
    binCanvas = [0] * squareNumber
    for i in range(squareNumber):
        binCanvas[i] = [0] * squareNumber
    pickedOnesX = []
    pickedOnesY = []
    name = "Computer"
    location = 0
    tk.Label(root, text = name).grid(row = location)
    canvas = tk.Canvas(root, width=squeareWidth*squareNumber, height=squareHeigth*squareNumber)
    canvas.grid(row = location + 1)
    shipsLeft = 10
    def pickCoordinates(self):
        return

class GameBoard:
    fireMode = 0
    fleet = 0
    level = 0
    shootsLeft = 6
    gameState = 0
    computerPlayer = Computer()
    realPlayer = RealPlayer()
    counter = [0,0]
    computerCount = 0
    realPlayerCount = 0
    members = [computerPlayer, realPlayer] # Computer = 0 You = 1
    turn = 0
    gameOver = 0
    pickedLength = 30
    pickedDirection = 0
    lastDrawX = []
    lastDrawY = []
    tempCanvas = copy.deepcopy(members[1].binCanvas)
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
    
    def winChecker(self):
        if self.members[0].shipsLeft == 0 :
            btn1_text.set("You Win - Play Again")
            return True
        elif self.members[1].shipsLeft == 0:
            btn1_text.set("Game Over - Play Again")
            return True
        else:
            btn1_text.set("Give Up")
            return False

    def shoot(self, x, y, player):
        if self.fireMode == 1 and self.shootsLeft == 0:
            return
        if self.gameState == 3:
            return
        self.gameState = 1
        if x < 0 or y < 0 or x > 9 or y > 9:
            return 1
        hit = 0
        if self.members[player].binCanvas[x][y] == 1 or self.members[player].binCanvas[x][y] == 3:
            hit = 1
            return hit
        if self.members[player].binCanvas[x][y] == 0:
            self.members[player].binCanvas[x][y] = 1
            hit = 2
        if self.members[player].binCanvas[x][y] == 2:
            self.members[player].binCanvas[x][y] = 3
            self.counter[player] = self.counter[player] + 1
            hit = 3
        
        self.showFields(player)
        if self.fireMode == 1:
            self.shootsLeft = self.shootsLeft - 1
            if self.shootsLeft == 0:
                if self.turn == 1:
                    self.turn = 0
                else:
                    self.turn = 1
            return hit
        
        if hit == 2:
            if self.turn == 1:
                self.turn = 0
            else:
                self.turn = 1
            return hit
        else:
            return hit

    def spaceChecker(self, length, direction, x, y, player):
        for i in range (0, length):
            if direction == 1:
                if x > 0 and x < 9 and (self.members[player].binCanvas[x+1][y+i] == 2 or self.members[player].binCanvas[x-1][y+i] == 2):
                    return True
                if y > 0 and y < 9 and (self.members[player].binCanvas[x][y+i+1] == 2 or self.members[player].binCanvas[x][y-1] == 2):
                    return True
                if self.members[player].binCanvas[x][y+i] == 2:
                    return True
                if x == 0 and (self.members[player].binCanvas[x+1][y+i] == 2):
                    return True
                if x == 9 and (self.members[player].binCanvas[x-1][y+i] == 2):
                    return True
                if y == 0 and (self.members[player].binCanvas[x][y+1+i] == 2):
                    return True
                if y == 9 and (self.members[player].binCanvas[x][y-1] == 2):
                    return True
            else:
                if y > 0 and y < 9 and (self.members[player].binCanvas[x+i][y+1] == 2 or self.members[player].binCanvas[x+i][y-1] == 2):
                    return True
                if x > 0 and x < 9 and (self.members[player].binCanvas[x+i+1][y] == 2 or self.members[player].binCanvas[x-1][y] == 2):
                    return True
                if self.members[player].binCanvas[x+i][y] == 2:
                    return True
                if y == 0 and (self.members[player].binCanvas[x+i][y+1] == 2):
                    return True
                if y == 9 and (self.members[player].binCanvas[x+i][y-1] == 2):
                    return True
                if x == 0 and (self.members[player].binCanvas[x+i+1][y] == 2):
                    return True
                if x == 9 and (self.members[player].binCanvas[x-1][y] == 2):
                    return True
        return False

    def setFields(self, length, player):
        while True:
            crossing = False
            direction = random.randint(0,1)
            x = random.randint(0, 9-length) if direction == 0 else random.randint(0,9)
            y = random.randint(0, 9-length) if direction == 1 else random.randint(0,9)
            
            crossing = self.spaceChecker(length, direction, x, y, player)

            if crossing: 
                continue
            for i in range (0,length):
                if direction == 1:
                    self.members[player].binCanvas[x][y+i] = 2
                else:
                    self.members[player].binCanvas[x+i][y] = 2
            break

    def choose(self, player):
        self.members[player].binCanvas = [0] * squareNumber
        for i in range(squareNumber):
            self.members[player].binCanvas[i] = [0] * squareNumber
        if self.fleet == 0:
            for i in range(5, 1, -1):
                for x in range(0,6-i):
                    self.setFields(i,player)
        else:
            for i in range(4, 1, -1):
                for x in range(0,5-i):
                    self.setFields(i,player)


    def play(self):
        squareNumber
        self.choose(0)
        self.choose(1)
        self.showFields(0)
        self.showFields(1)
        hit = 1
        hitX = 0
        hitY = 0
        direction = 0
        changeDirection = 0
        tempTurn = 1
        while not self.gameOver:
            if self.gameState != 0 and self.winChecker():
                self.shootsLeft = 6
                self.gameState = 0
                self.turn = 0
            if self.turn == 0:
                if tempTurn != self.turn:
                    tempTurn = self.turn
                    self.shootsLeft = self.members[1].shipsLeft
                if self.gameState == 0 or self.gameState == 3:
                    self.members[1].canvas.bind('<Button-1>', self.pick)
                else:
                    self.members[1].canvas.unbind('<Button-1>')
                
                self.members[0].canvas.bind('<Button-1>', self.realPlayerShoot)
                root.update()
            else:
                self.members[0].canvas.unbind('<Button-1>')
                if tempTurn != self.turn:
                    tempTurn = self.turn
                    self.shootsLeft = self.members[0].shipsLeft

                if self.fireMode == 1 and self.level == 1 and len(self.members[1].pickedOnesX)>0:
                    shipsLeft = True
                    for i in range(len(self.members[1].pickedOnesX)):
                        if self.members[1].binCanvas[self.members[1].pickedOnesX[i]][self.members[1].pickedOnesY[i]] != 3:
                            self.shoot(self.members[1].pickedOnesX[i], self.members[1].pickedOnesY[i], 1)
                    if not shipsLeft:
                        self.members[1].pickedOnesX.clear()
                        self.members[1].pickedOnesY.clear()
                if direction == 0:
                    if hit == 1 or hit == 2:
                        pressure = 0
                        while True:
                            pressure = pressure + 1
                            if pressure > 120:
                                break
                            x = random.randrange(0,squareNumber)
                            y = random.randrange(0,squareNumber)
                            if pressure < 60:
                                if (x % 2 == 1 and y % 2 == 0):
                                    continue
                                if x + 1 <= 9 and (self.members[1].binCanvas[x+1][y] == 1): 
                                    continue
                                if x - 1 >= 0 and (self.members[1].binCanvas[x-1][y] == 1): 
                                    continue
                                if y + 1 <= 9 and (self.members[1].binCanvas[x][y+1] == 1): 
                                    continue
                                if y - 1 >= 0 and (self.members[1].binCanvas[x][y-1] == 1): 
                                    continue
                            if (x % 2 == 1 and y % 2 == 0):
                                continue
                            if x + 1 <= 9 and (self.members[1].binCanvas[x+1][y] == 3): 
                                continue
                            if x - 1 >= 0 and (self.members[1].binCanvas[x-1][y] == 3): 
                                continue
                            if y + 1 <= 9 and (self.members[1].binCanvas[x][y+1] == 3): 
                                continue
                            if y - 1 >= 0 and (self.members[1].binCanvas[x][y-1] == 3): 
                                continue
                            if not self.members[1].binCanvas[x][y] == 1 or self.members[1].binCanvas[x][y] == 3:
                                break
                        hit = self.shoot(x, y, 1)
                        hitX = x
                        hitY = y
                        if hit == 3 and self.level == 1:
                            self.shipFinder(1, x, y)
                            for i in range(len(self.members[1].pickedOnesX)):
                                self.shoot(self.members[1].pickedOnesX[i], self.members[1].pickedOnesY[i], 1)
                            self.members[1].shipsLeft = self.members[1].shipsLeft - 1
                            hit = 1
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
                if direction != 0 and changeDirection < 2:
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
                    self.members[1].shipsLeft = self.members[1].shipsLeft - 1
                    hit = 1
                    changeDirection = 0
                    direction = 0
                root.update()

    def realPlayerShoot(self, event):
        x = int(event.x/squeareWidth)
        y = int(event.y/squareHeigth)
        hit = self.shoot(x, y, 0)
        if hit == 3:#HIER WEITERMACHEN
            self.shipFinder(0, x, y)
            print(self.members[0].pickedOnesX)
            print(self.members[0].pickedOnesY)
            shipsLeft = False
            for i in range(len(self.members[0].pickedOnesX)):
                if self.members[0].binCanvas[self.members[0].pickedOnesX[i]][self.members[0].pickedOnesY[i]] != 3:
                    shipsLeft = True
            if not shipsLeft:
                self.members[0].shipsLeft = self.members[0].shipsLeft - 1 
            
            

    def shipFinder(self, player, x, y):
        self.members[player].pickedOnesX.clear()
        self.members[player].pickedOnesY.clear()
        count = 1
        while True: 
            if (x+count < squareNumber) and (self.members[player].binCanvas[x+count][y] == 2 or self.members[player].binCanvas[x+count][y] == 3):
                self.members[player].pickedOnesX.append(x+count)
                self.members[player].pickedOnesY.append(y)
                count = count +1
            else:
                count = 1
                break
        while True: 
            if (x - count >= 0) and (self.members[player].binCanvas[x-count][y] == 2 or self.members[player].binCanvas[x-count][y] == 3):
                self.members[player].pickedOnesX.append(x-count)
                self.members[player].pickedOnesY.append(y)
                count = count +1
            else:
                count = 1
                break
        while True: 
            if (y - count >= 0) and (self.members[player].binCanvas[x][y - count] == 2 or self.members[player].binCanvas[x][y - count] == 3):
                self.members[player].pickedOnesX.append(x)
                self.members[player].pickedOnesY.append(y- count)
                count = count +1
            else:
                count = 1
                break
        while True: 
            if (y+count < squareNumber) and (self.members[player].binCanvas[x][y+count] == 2 or self.members[player].binCanvas[x][y+count] == 3):
                self.members[player].pickedOnesX.append(x)
                self.members[player].pickedOnesY.append(y+count)
                count = count +1
            else:
                break
        self.members[player].pickedOnesX.append(x)
        self.members[player].pickedOnesY.append(y)

    def pick(self, event):
        self.members[1].pickedOnesX.clear()
        self.members[1].pickedOnesY.clear()

        x = int(event.x/squeareWidth)
        y = int(event.y/squareHeigth)

        if self.members[1].binCanvas[x][y] == 2:
            self.tempCanvas = copy.deepcopy(self.members[1].binCanvas)
            self.shipFinder(1, x, y)
            self.pickedLength = self.pickedLength - len(self.members[1].pickedOnesX)
            for i in range(len(self.members[1].pickedOnesX)):
                self.members[1].binCanvas[self.members[1].pickedOnesX[i]][self.members[1].pickedOnesY[i]] = 0
        
        elif self.members[1].binCanvas[x][y] != 1 and self.pickedLength != 30:
            while True:
                direction = 0
                # Checkt ob Punkte nebeneinander gesetzt werden
                if len(self.lastDrawX) == 1 and not (( self.lastDrawX[0] == x + 1 and self.lastDrawY[0] == y) or ( self.lastDrawX[0] == x - 1 and self.lastDrawY[0] == y) or ( self.lastDrawX[0] == x and self.lastDrawY[0] == y + 1) or ( self.lastDrawX[0] == x and self.lastDrawY[0] == y - 1)):
                    break
                # Checkt in welche Richtung die Punkte gesetzt werden müssen
                if len(self.lastDrawX) > 1:
                    for i in range(len(self.lastDrawX)):
                        if self.lastDrawX[0] == self.lastDrawX[1]:
                            direction = 1
                            print("Senkrecht")
                        else:
                            direction = 2
                            print("Wagerecht")

                if direction == 2 and not ((x + 1 == min(self.lastDrawX) and y == self.lastDrawY[self.lastDrawX.index(min(self.lastDrawX))]) or (x - 1 == max(self.lastDrawX) and y == self.lastDrawY[self.lastDrawX.index(max(self.lastDrawX))])):
                    print("Fehler1")
                    break
                if direction == 1 and not ((y + 1 == min(self.lastDrawY) and x == self.lastDrawX[self.lastDrawY.index(min(self.lastDrawY))]) or (y - 1 == max(self.lastDrawY) and x == self.lastDrawX[self.lastDrawY.index(max(self.lastDrawY))])):
                    print("Fehler2")
                    break
                
                if x + 1 <= 9 and self.members[1].binCanvas[x+1][y] == 1 and not (x + 1 == min(self.lastDrawX) and y == self.lastDrawY[self.lastDrawX.index(min(self.lastDrawX))]): 
                    break
                if x - 1 >= 0 and self.members[1].binCanvas[x-1][y] == 1 and not (x - 1 == max(self.lastDrawX) and y == self.lastDrawY[self.lastDrawX.index(max(self.lastDrawX))]): 
                    break
                if y + 1 <= 9 and self.members[1].binCanvas[x][y+1] == 1 and not (y + 1 == min(self.lastDrawY) and x == self.lastDrawX[self.lastDrawY.index(min(self.lastDrawY))]): 
                    break
                if y - 1 >= 0 and self.members[1].binCanvas[x][y-1] == 1 and not (y - 1 == max(self.lastDrawY) and x == self.lastDrawX[self.lastDrawY.index(max(self.lastDrawY))]): 
                    break

                self.members[1].binCanvas[x][y] =  3
                self.pickedLength = self.pickedLength +1
                self.lastDrawX.append(x)
                self.lastDrawY.append(y)
                break

        if self.pickedLength < 30:
            btn1_text.set("Return")
            self.gameState = 3
            for t in range (squareNumber):
                for z in range (squareNumber):
                    if self.members[1].binCanvas[z][t] != 0:
                        self.members[1].binCanvas[z][t] = 1
        else:
            for t in range (squareNumber):
                for z in range (squareNumber):
                    if self.members[1].binCanvas[z][t] != 0:
                        self.members[1].binCanvas[z][t] = 2
            self.pickedDirection == 0
            self.lastDrawX.clear()
            self.lastDrawY.clear()
            btn1_text.set("Randomize")
            self.gameState = 0
        self.showFields(1)
        root.update()
    

gameBoard = GameBoard()

def startStoper():
    if gameBoard.gameState == 3:
        gameBoard.pickedLength = 30
        gameBoard.members[1].binCanvas = copy.deepcopy(gameBoard.tempCanvas)
        gameBoard.showFields(1)
        btn1_text.set("Randomize")
        gameBoard.gameState = 0
        gameBoard.lastDrawX.clear()
        gameBoard.lastDrawY.clear()

    else:
        gameBoard.counter = [0,0]
        btn1_text.set("Randomize")
        gameBoard.gameState = 0
        gameBoard.choose(0)
        gameBoard.choose(1)
        gameBoard.showFields(0)
        gameBoard.showFields(1)
        gameBoard.turn = 0
        if gameBoard.fireMode == 0:
            gameBoard.members[0].shipsLeft = 10
            gameBoard.members[1].shipsLeft = 10
        else:
            gameBoard.members[0].shipsLeft = 6
            gameBoard.members[1].shipsLeft = 6
            gameBoard.tempTurn = 1
            gameBoard.shootsLeft = 6
            gameBoard.turn = 0
        gameBoard.play()
        gameBoard.pickedLength = 30
def fleetChanger():
    if gameBoard.gameState == 0:
        if gameBoard.fleet == 0:
            gameBoard.fleet = 1
            gameBoard.members[0].shipsLeft = 6
            gameBoard.members[1].shipsLeft = 6
            btn4_text.set("Small Fleet")
        else:
            if gameBoard.fireMode == 1:
                gameBoard.fireMode = 0
                btn3_text.set("Classic Fire-Mode")
            gameBoard.fleet = 0
            gameBoard.members[0].shipsLeft = 10
            gameBoard.members[1].shipsLeft = 10
            btn4_text.set("Big Fleet (Classic)")
        startStoper()

def fireMode():
    print(gameBoard.fireMode, " GAMESTATE")
    if gameBoard.gameState == 0:
        if gameBoard.fireMode == 1:
            btn3_text.set("Classic Fire-Mode")
            gameBoard.fireMode = 0
        else:
            btn3_text.set("Chain Fire-Mode") 
            gameBoard.fireMode = 1
            if gameBoard.fleet == 0:
                gameBoard.fleet = 1
                gameBoard.members[0].shipsLeft = 6
                gameBoard.members[1].shipsLeft = 6
                btn4_text.set("Small Fleet")
                startStoper()
        
def level():
    if gameBoard.level == 0:
        gameBoard.level = 1
        btn2_text.set("Rage-Mode")
    else:
        gameBoard.level = 0
        btn2_text.set("Easy")


tk.Button(root, text="Start", command=startStoper, textvariable=btn1_text).grid(row = 5)
tk.Button(root, text="Rule", command=level, textvariable=btn2_text).grid(row = 6)
tk.Button(root, text="Classic Fire-Mode", command=fireMode, textvariable=btn3_text).grid(row = 7)
tk.Button(root, text="Big Fleet (Classic)", command=fleetChanger, textvariable=btn4_text).grid(row = 8)


btn1_text.set("Randomize")
btn2_text.set("Easy")
btn3_text.set("Classic Fire-Mode")
btn4_text.set("Big Fleet (Classic)")


gameBoard.play()

root.mainloop()
