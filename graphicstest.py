from graphics import *

beep = 5

def main():
    print( beep )
    win = GraphWin("My Circle", 500, 500)
    c = Circle(Point(50,50), 10)
    c.setFill('blue')
    # c.draw(win)

    # animation loop
    x = 10
    y = 10
    while True:
        x += 5
        y += 5
        # c.undraw()
        j = c
        j.undraw()
        c = Circle(Point(x,y), 10)

        c.draw(win)



    win.getMouse() # pause for click in window
    win.close()
main()