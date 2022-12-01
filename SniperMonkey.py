class SniperMonkey(Monkey):
    def __init__(self, x, y):
        super().__init__(x, y, 0)
    
    def timerFired(self, app):
        if app.time % 2000 == 0:
            if len(app.bloons) > 0:
                app.bloons.pop(0)
                app.money += 1

    def redraw(self, app, canvas):
        super().redraw(app, canvas)
        x0 = self.x + 10
        y0 = self.y - 35
        x1 = x0 + 5
        y1 = y0 + 40
        canvas.create_rectangle(x0, y0, x1, y1, fill='gray')