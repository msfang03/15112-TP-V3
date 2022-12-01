#################################################
# Term Project
#
# Your name:Max Fang
# Your andrew id:msfang
# Section: O
#################################################
from cmu_112_graphics import *
import math
import random

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
#################################################

#Bloons Class
class Bloons:
    def __init__(self, x, y, life, color, speed):
        self.x = x
        self.y = y
        self.r = 20
        self.life = life
        self.color = color
        self.speed = speed

    def redraw(self, app, canvas):
        if self.life > 0:
            x0  = self.x - self.r
            y0 = self.y - self.r
            x1 = x0 + 2*self.r
            y1 = y0 + 2*self.r
            canvas.create_oval(x0, y0, x1, y1, fill=self.color)

    def timerFired(self, app):
        if self.y == app.height//2 and self.x < app.width * (2/5):
            self.x += self.speed
        elif (app.width * (3/5) > self.x >= app.width * (2/5) and 
        app.height//2 <= self.y < app.height * (3/4)):
            self.y += self.speed
        elif (self.y >= app.height * (3/4) and 
        app.width * (2/5) <= self.x < app.width * (3/5)):
            self.x += self.speed
        elif self.x >= app.width * (3/5):
            self.y -= self.speed

class RedBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 1, "red", 10)
 
class BlueBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 2, "blue", 14)

class GreenBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 1, "green", 18)

class PredictRed(RedBloon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.appear = True

    def timerFired(self, app):
        if self.appear:
            super().timerFired(app)

class PredictBlue(BlueBloon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.appear = True

    def timerFired(self, app):
        if self.appear:
            super().timerFired(app)

class PredictGreen(GreenBloon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.appear = True

    def timerFired(self, app):
        if self.appear:
            super().timerFired(app)

def demote(app, bloon, pred):
    if isinstance(bloon, GreenBloon):
        app.bloons.remove(bloon)
        app.bloons.append(BlueBloon(bloon.x, bloon.y))
        app.predictor.remove(pred)
        app.predictor.append(BlueBloon(pred.x, pred.y))
    elif isinstance(bloon, BlueBloon):
        app.bloons.remove(bloon)
        app.bloons.append(RedBloon(bloon.x, bloon.y))
        app.predictor.remove(pred)
        app.predictor.append(RedBloon(bloon.x, pred.y))

#Monkey class
class Monkey:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.state = True
        self.placed = False

    def redraw(self, app, canvas):
        x0  = self.x - 20
        y0 = self.y - 20
        x1 = x0 + 40
        y1 = y0 + 40
        canvas.create_oval(x0, y0, x1, y1, fill='sienna')

#most hp, fastest, first 
class Dart:
    def __init__(self, x, y, pred, bloon, monkey):
        self.x = x
        self.y = y
        self.bloon = bloon
        self.monkey = monkey
        self.pred = pred

    def timerFired(self, app):
        self.x += (self.pred.x - self.x)/3
        self.y += (self.pred.y - self.y)/3
        if (distance(self.monkey.x, self.monkey.y, self.x, self.y) > 
        self.monkey.r):
            app.dart.remove(self)
        elif (distance(self.x, self.y, self.bloon.x, self.bloon.y) <= 
        self.bloon.r):  
            if isinstance(self.bloon, RedBloon):
                app.money += 1
                app.bloons.remove(self.bloon)
                app.predictor.remove(self.pred)
                app.dart.remove(self)
            # else:
            #     demote(app, self.bloon, self.pred)
            #     app.money += 1
        
    def redraw(self, app, canvas):
        canvas.create_polygon(self.x, self.y, self.x-5, self.y+10, self.x+5, 
        self.y+10, fill='black')


class DartMonkey(Monkey):
    def __init__(self, x, y, time):
        super().__init__(x, y, 100)
        self.dart = None
        self.target = None
        self.time = time

    def timerFired(self, app):
        if self.placed:
            i = -1
            for bloon in app.bloons:
                i += 1
                if (distance(bloon.x, bloon.y, self.x, self.y) <= self.r):
                    self.target = bloon
                    break
            if self.target != None:
                pred = app.predictor[i]
                pred.appear = False
                if (len(app.dart) < len(app.monkey) and 
                app.time - self.time > 500):
                    self.time = app.time
                    app.dart.append(Dart(self.x, self.y, pred, self.target, 
                    self))
                self.target = None
        
class SniperMonkey(Monkey):
    def __init__(self, x, y):
        super().__init__(x, y, 0)
    
    def timerFired(self, app):
        if self.placed:
            if app.time % 2000 == 0:
                if len(app.bloons) > 0:
                    app.bloons.pop(0)
                    app.predictor.pop(0)
                    app.money += 1
            return False

    def redraw(self, app, canvas):
        super().redraw(app, canvas)
        x0 = self.x + 10
        y0 = self.y - 35
        x1 = x0 + 5
        y1 = y0 + 40
        canvas.create_rectangle(x0, y0, x1, y1, fill='gray')

# Code structured after class notes - OOP part 1
def appStarted(app):
    app.bloons = []
    app.predictor = []
    app.time = 0
    app.timerDelay = 40
    app.health = 100
    app.monkey = []
    app.money = 650
    app.size = app.width//11
    app.row = 20
    app.col = 30
    app.cellSizeY = app.height/app.row
    app.cellSizeX = app.width/app.col
    app.board = [[True] * app.col for i in range(app.row)]
    drawPath(app)
    app.state = False
    app.dartMonkPrice = 170
    app.snipeMonkPrice = 300
    app.dart = []

def getCell(app, x, y):
    resultx = x//app.cellSizeX
    resulty = y//app.cellSizeY
    return int(resulty), int(resultx)

def isLegal(app, x, y):
    row, col = getCell(app, x, y)
    return app.board[row][col]

def drawBoard(app, canvas):
    roadCol = 'burlywood'
    for i in range(app.col):
        for j in range(app.row):
            if (j == 10 or j == 9) and i <= 12:
                color = roadCol
            elif (i == 12 or i == 11) and 10 < j <= 15:
                color = roadCol
            elif (j == 15 or j == 14) and 12 < i <= 18:
                color = roadCol
            elif (i == 18 or i == 17) and j < 15:
                color = roadCol
            else: color = 'green'
            x0 = app.width * (i/app.col)
            y0 = app.height * (j/app.row)
            x1 = x0 + app.cellSizeX
            y1 = y0 + app.cellSizeY
            canvas.create_rectangle(x0,y0,x1,y1, fill=color, width = 0)

def drawPath(app):
    for i in range(app.col):
        for j in range(app.row):
            if (j == 10 or j == 9) and i <= 12:
                app.board[j][i] = False
            elif (i == 12 or i == 11) and 10 < j <= 15:
                app.board[j][i] = False
            elif (j == 15 or j == 14) and 12 < i <= 18:
                app.board[j][i] = False
            elif (i == 18 or i == 17) and j < 15:
                app.board[j][i] = False
            elif i > 23:
                app.board[j][i] = False

def drawMenu(app, canvas):
    size = app.size
    x0 = app.width*(4/5)
    y0 = app.height*(1/4) - size
    x1 = x0 + size*2
    y1 = y0 + size
    canvas.create_rectangle(x0,y0,x1,y1, fill='white')
    for i in range(2):
        for j in range(3):
            x0 = app.width*(4/5) + i*size
            y0 = app.height*(1/4) + j*size
            x1 = x0 + size
            y1 = y0 + size
            canvas.create_rectangle(x0,y0,x1,y1, fill='white')
    x0 = app.width*(4/5) + size//2 - 20
    y0 = app.height*(1/4) + size//2 - 20
    x1 = x0 + 40
    y1 = y0 + 40
    canvas.create_oval(x0, y0, x1, y1, fill='sienna')
    x0 = app.width*(4/5) + 3*size//2 - 20
    y0 = app.height*(1/4) + size//2 - 20
    x1 = x0 + 40
    y1 = y0 + 40
    canvas.create_oval(x0, y0, x1, y1, fill='sienna')
    v0 = x0 + 30
    w0 = y0 - 15
    v1 = v0 + 5
    w1 = w0 + 40
    canvas.create_rectangle(v0, w0, v1, w1, fill='gray')

def timerFired(app):
    app.time += app.timerDelay
    if app.health > 0:
        for monkey in app.monkey:
            monkey.timerFired(app)
        for dart in app.dart:
            dart.timerFired(app)
        if app.time % 250 == 0:
            num = random.randint(1, 1)
            if num == 1:
                app.bloons.append(RedBloon(0, app.height//2))
                app.predictor.append(PredictRed(30, app.height//2))
            elif num == 2:
                app.bloons.append(BlueBloon(0, app.height//2))
                app.predictor.append(PredictBlue(30, app.height//2))
            elif num == 3:
                app.bloons.append(GreenBloon(0, app.height//2))
                app.predictor.append(PredictGreen(30, app.height//2))
        for bloon in app.bloons:
            bloon.timerFired(app)
            if bloon.y < -bloon.r:
                app.health -= 5
                app.bloons.remove(bloon)
        for bloon in app.predictor:
            bloon.timerFired(app)

def mousePressed(app, event):
    size = app.size
    x0 = app.width*(4/5) 
    y0 = app.height*(1/4) 
    x1 = x0 + size
    y1 = y0 + size
    if x0 < event.x < x1 and y0 < event.y < y1:
        if app.money - app.dartMonkPrice > 0:
            app.state = True
            app.monkey.append(DartMonkey(event.x, event.y, app.time))
    v0 = x0 + size
    w0 = y0
    v1 = v0 + size
    w1 = y0 + size
    if v0 < event.x < v1 and w0 < event.y < w1:
        if app.money - app.snipeMonkPrice > 0:
            app.state = True
            app.monkey.append(SniperMonkey(event.x, event.y))

def mouseDragged(app, event):
    if app.state:
        monk = app.monkey[-1]
        monk.x = event.x
        monk.y = event.y

def mouseReleased(app, event):
    if app.state:
        monkey = app.monkey[-1]
        if isLegal(app, event.x, event.y):
            app.money -= app.dartMonkPrice
            monkey.x = event.x
            monkey.y = event.y
            monkey.state = False
            app.state = False
            monkey.placed = True
        else:
            app.monkey.remove(monkey)
            app.state = False

def redrawAll(app, canvas):
    drawBoard(app, canvas)
    drawMenu(app, canvas)
    canvas.create_text(app.width*(4/5)+app.size/2,app.height*(1/4)-app.size/2, 
    text = f'{app.health}', font="Times 28 bold")
    canvas.create_text(app.width*(4/5)+3*app.size/2,app.height*(1/4)-app.size/2, 
    text = f'{app.money}', font="Times 28 bold")
    for bloon in app.bloons:
        bloon.redraw(app, canvas)
    # for bloon in app.predictor:
    #     bloon.redraw(app, canvas)
    for monkey in app.monkey:
        monkey.redraw(app, canvas)
        if monkey.state == True:
            x0 = monkey.x-monkey.r
            y0 = monkey.y-monkey.r
            x1 = x0 + 2*monkey.r
            y1 = y0 + 2*monkey.r
            canvas.create_oval(x0,y0,x1,y1)
    for dart in app.dart:
        dart.redraw(app, canvas)
    if app.health == 0:
        canvas.create_rectangle(app.width//3, app.height//3, 2*app.width//3,
        2*app.height//3, fill='goldenrod',)
        canvas.create_text(app.width//2, app.height//2, text = "Game Over",
        font='Times 50 bold')

#Full Screen code from Piazza Post question @2426
runApp(width = 1440, height = 792)