def calcY(x, m, b):
    y = m*x + b
    return y

def inBox(x0, x1, y0, y1, px, py):
    is_in = 0
    if px > x0 and px < x1 and py > y0 and py < y1:
        is_in = 1
    return is_in

def inParallelogram(px, py,  m, b, var):
    is_in = 0
    y_top = calcY(px, m, b+var)
    y_bot = calcY(px, m, b-var)
    if py > y_bot and py < y_top:
        is_in = 1
    return is_in
