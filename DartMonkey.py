import math
import Monkey
def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

class Dart:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def timerFired(self, app, bloon, monk, pred):
        self.x += (pred.x - self.x)/5
        self.y += (pred.y - self.y)/5
        if distance(monk.x, monk.y, self.x, self.y) > monk.r:
            monk.dart.remove(self)
            app.bloons.remove(bloon)
        elif (distance(self.x, self.y, bloon.x, bloon.y) <= 
        bloon.r):  
            app.bloons.remove(bloon)
            app.predictor.remove(pred)
            monk.dart.remove(self)
        
    def redraw(self, app, canvas):
        canvas.create_polygon(self.x, self.y, self.x-5, self.y+10, self.x+5, 
        self.y+10, fill='black')


class DartMonkey(Monkey):
    def __init__(self, x, y):
        super().__init__(x, y, 100)
        self.dart = []

    def timerFired(self, app, bloon):
        i = app.bloons.index(bloon)
        pred = app.predictor[i]
        if (distance(bloon.x, bloon.y, self.x, self.y) <= self.r and 
        len(self.dart) < 1):
            pred.appear = False
            self.dart.append(Dart(self.x, self.y))
        for dart in self.dart:
            dart.timerFired(app, bloon, self, pred)
        
    
