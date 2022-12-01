class Monkey:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.state = True

    def redraw(self, app, canvas):
        x0  = self.x - 20
        y0 = self.y - 20
        x1 = x0 + 40
        y1 = y0 + 40
        canvas.create_oval(x0, y0, x1, y1, fill='sienna')

