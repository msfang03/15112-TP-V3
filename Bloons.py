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
    
class Predictor(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 'red', 10)
        self.appear = True

    def timerFired(self, app):
        if self.appear:
            super().timerFired(app)

class RedBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 1, "red", 10)
 
class BlueBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 2, "blue", 14)


class GreenBloon(Bloons):
    def __init__(self, x, y):
        super().__init__(x, y, 1, "green", 18)
    
    

        