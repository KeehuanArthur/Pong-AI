import globals
import random
import animation
import math

# Game Notes:
# - center of play field is (0,0)
# - game field size is: 
# - paddle size is: 
# - everything is scaled to 100 so we don't have to deal with floats


# detect_paddle_collision 
# return true if 
#   - hit paddle left 
#   - hit paddle right
def detect_paddle_collision( game_state ):
    
    # hit the paddle
    if (game_state.ball_x >= globals.PADDLE1_X and
        game_state.ball_y <= game_state.paddle1_y + globals.PADDLE_SIZE/2 and
        game_state.ball_y >= game_state.paddle1_y - globals.PADDLE_SIZE/2):
        return True 
    
    # if its only single player, just make ball bounce when it gets to other side
    if game_state.paddle2_y == None:
        if game_state.ball_x <= globals.BOARD_LEFT:
            # game_state.velocity_y *= -1  # it will be flipped again for left side
            return True
        return False

    elif (game_state.ball_x == globals.PADDLE2_X and
        game_state.ball_y < game_state.paddle2_y + globals.PADDLE_SIZE/2 and
        game_state.ball_y > game_state.paddle2_y - globals.PADDLE_SIZE/2):
        return True 
    
    return False

# detect_edge_collision
# make sure the ball doesn't go out of bounds
def detect_edge_collision( game_state ):
    if( game_state.ball_y < globals.BOARD_TOP or game_state.ball_y > globals.BOARD_BOTTOM):
        return True
    return False

# randomize_velocity
def randomize_velocity( vx, vy ):
    vx += random.uniform(-1.5, 1.5)
    vy += random.uniform(-3.0, 3.0)
    # vx += random.randint(-1,1)
    # vy += random.randint(-3, 3)

    #! why is it that when i use uniform for the y axis, it freaks out??


    # make sure that vx is at least some speed
    if vx > 0 and vx < 3:
        vx = 3
    elif vx < 0 and vx > -3:
        vx = -3

    # make sure not to overshoot the velocity
    if vx > 100:
        vx = 99
    elif vx < -100:
        vx = -99
    if vy > 100:
        vy = 99
    elif vy < -100:
        vy = -99
    
    return vx, vy


# depending on mode, paddle2_y will be None
# the x positions of the paddles are in the globals file because they shouldn't change
class Game_State:
    def __init__( self, ball_x, ball_y, velocity_x, velocity_y, paddle1_y, paddle2_y ):
        self.ball_x = ball_x
        self.ball_y = ball_y 
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.paddle1_y = paddle1_y
        self.paddle2_y = paddle2_y

    # used to get the state for q learning
    # (ballx, bally, vx, vy, paddley)
    def get_discrete_game_stats(self):
        ball_x_d = int(self.ball_x / 12)
        ball_y_d = int(self.ball_y / 12)
        vx_d = 1
        if self.velocity_x < 0:
            vx_d = -1 
        vy_d = 0
        if self.velocity_y <= -1.5:
            vy_d = -1
        elif self.velocity_y >= 1.5:
            vy_d = 1
        # paddle1_y_d = int(self.paddle1_y / 12)
        paddle1_y_d = int( (1200*self.paddle1_y)/(100 - globals.PADDLE_SIZE)  )

        if (self.ball_x > globals.BOARD_RIGHT and
            self.ball_y > self.paddle1_y + globals.PADDLE_SIZE/2 and
            self.ball_y < self.paddle1_y - globals.PADDLE_SIZE/2 ):
            return ( 1000, 1000, 1000, 1000, 1000 )

        return (ball_x_d, ball_y_d, vx_d, vy_d, paddle1_y_d)

    def move_ball(self):
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y

    def move_paddle1(self, dy):

        # make sure the paddle doesn't go past the edges
        if (self.paddle1_y - globals.PADDLE_SIZE/2 + dy) < globals.BOARD_TOP:
            # self.paddle1_y = globals.BOARD_TOP + 1
            return
        if (self.paddle1_y + globals.PADDLE_SIZE/2 + dy) > globals.BOARD_BOTTOM:
            # self.paddle1_y = globals.BOARD_BOTTOM - 1
            return

        self.paddle1_y += dy
    
    def move_paddle2(self, dy):
        if (self.paddle2_y + globals.PADDLE_SIZE/2 + dy) > globals.BOARD_TOP:
            return
        if (self.paddle2_y - globals.PADDLE_SIZE/2 + dy) < globals.BOARD_BOTTOM:
            return
        self.paddle2_y += dy


    # collision_detect
    # change velocity of paddle 
    # change position of ball
    # Input:    None
    # Return:   Return True only if the paddle at the left hits it.
    def collision_detect(self):
        if detect_paddle_collision( self ):
            self.velocity_x = -self.velocity_x
            # self. velocity_y = -self.velocity_y


            # reset ball position 
            if self.ball_x <= 0:
                self.ball_x = 0
            elif self.ball_x >= globals.BOARD_RIGHT:
                self.ball_x = globals.BOARD_RIGHT
            if self.ball_y <= 0:
                self.ball_y = 0
            elif self.ball_y >= globals.BOARD_BOTTOM:
                self.bally = globals.BOARD_BOTTOM

            # only increment if you bounce on the right side
            if self.ball_x >= globals.BOARD_RIGHT:
                self.velocity_x, self.velocity_y = randomize_velocity( self.velocity_x, self.velocity_y )
                return True

        return False

    def edge_detect(self):
        if detect_edge_collision(self):
            self.velocity_y = -self.velocity_y
            # self.velocity_x, self.velocity_y = randomize_velocity( self.velocity_x, self.velocity_y )
            
            # reposition the ball
            if self.ball_x < 0:
                self.ball_x = 0
            elif self.ball_x > globals.BOARD_RIGHT:
                self.ball_x = globals.BOARD_RIGHT
            if self.ball_y < 0:
                self.ball_y = 0
            elif self.ball_y > globals.BOARD_BOTTOM:
                self.ball_y = globals.BOARD_BOTTOM

    def detect_gameset(self):

        # there is case where the ball might be moving too fast and move past the paddle
        if ( self.ball_y < self.paddle1_y + globals.PADDLE_SIZE/2 and
             self.ball_y > self.paddle1_y - globals.PADDLE_SIZE/2 ):
             return False


        if self.ball_x > globals.BOARD_RIGHT:
            return True 
        else:
            return False
        
        #TODO: take care of 2 player case

    def reset(self):
        self.ball_x = globals.BOARD_RIGHT/2
        self.ball_y = globals.BOARD_BOTTOM/2
        self.velocity_x = 3
        self.velocity_y = 1
        self.paddle1_y = globals.BOARD_BOTTOM/2


    def win_detect_two_player(self):
        pass



