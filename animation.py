from graphics import *
import threading
import globals

# animation globals ~ only needed for animation
# the following are init values, don't mind them
ball = Circle(Point(0,0), 1)
paddle1 = Rectangle(Point(0,0), Point(1,1))
paddle2 = Rectangle(Point(0,0), Point(1,1))
ball_tmp = None
paddle1_tmp = None
paddle2_tmp = None

PADDLE_THICKNESS = 10


def convert_coords( coords ):
    cx = coords[0] * globals.SCALE
    cy = coords[1] * globals.SCALE
    return (cx,cy)

def draw_ball( win, coords ):
    global ball
    global ball_tmp
    a_coords = convert_coords( coords )
    ball_tmp = Circle(Point(a_coords[0], a_coords[1]), globals.SCALE )
    ball_tmp.setFill('red')
    ball.undraw()
    ball_tmp.draw(win)    
    ball = ball_tmp

def draw_paddle1( win, coords ):
    global paddle1
    global paddle1_tmp

    # get top left coord 
    tl_coord = (coords[0], coords[1] - globals.PADDLE_SIZE/2)

    # get bottom right coords 
    br_coords = (coords[0], coords[1] + globals.PADDLE_SIZE/2)

    # get coordinates for animation 
    a_tl = convert_coords( tl_coord )
    a_br = convert_coords( br_coords )
    
    tl_x = a_tl[0] - PADDLE_THICKNESS
    tl_y = a_tl[1] 
    br_x = a_br[0]
    br_y = a_br[1]

    paddle1_tmp = Rectangle( Point(tl_x, tl_y), Point(br_x, br_y) )
    paddle1_tmp.setFill('blue')

    paddle1_tmp.draw(win)
    paddle1.undraw()
    paddle1 = paddle1_tmp

def draw_paddle2( win, paddle2, coords ):
    if paddle2 == None:
        return


def draw_frame( win, game_state ):
    draw_ball( win, (game_state.ball_x, game_state.ball_y) )
    draw_paddle1( win, (globals.PADDLE1_X, game_state.paddle1_y) )

    if globals.PADDLE2_A != None:
        pass
        #TODO

# def move_ball( game_state ):
#     global ball
#     ball.move( game_state.velocity_x, game_state.velocity_y )

# def move_paddle( game_)

def init_globals( win, players ):
    global ball
    global paddle1
    global paddle2
    if players == 1:
        # get top left coord 
        tl_coord = (coords[0], coords[1] - globals.PADDLE_SIZE/2)

        # get bottom right coords 
        br_coords = (coords[0], coords[1] + globals.PADDLE_SIZE/2)

        # get coordinates for animation 
        a_tl = convert_coords( tl_coord )
        a_br = convert_coords( br_coords )
        
        tl_x = a_tl[0] - 5
        tl_y = a_tl[1] 
        br_x = a_br[0]
        br_y = a_br[1]

        paddle1.undraw()
        paddle1 = Rectangle( Point(tl_x, tl_y), Point(br_x, br_y) )
        paddle1.setFill('blue')

        paddle1.draw(win)
        
        print( 'original coords: ', coords )
        a_coords = convert_coords( coords )
        ball = Circle(Point(a_coords[0], a_coords[1]), globals.SCALE/2 )
        print( 'drawing ball to: ', a_coords)
        ball.setFill('red')
        ball.draw(win) 

