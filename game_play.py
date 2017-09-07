import game_state
import globals
from graphics import *
import animation
import q_learning
import time
import sys
import pickle
import sys 
import os

ANIMATION_ON = True

# start_S
# this function starts a single paddle that keeps reflecting the ball
def start_S( ql ):

    # init globals
    globals.BOARD_LEFT = 0
    globals.BOARD_RIGHT = 100
    globals.BOARD_BOTTOM = 100
    globals.BOARD_TOP = 0
    globals.BOARD_X = 100
    globals.BOARD_Y = 100
    globals.PADDLE1_X = 100
    globals.SCREEN_X = globals.BOARD_X * globals.SCALE
    globals.SCREEN_Y = globals.BOARD_Y * globals.SCALE

    # create game state
    gs = game_state.Game_State( 50, 50, 3, 1, 50, None )

    # # create q_learning AI 
    # ql = q_learning.Q_Learn()

    # create animation window
    if ANIMATION_ON:
        win = GraphWin( "Pong", globals.SCREEN_X, globals.SCREEN_Y )
    

    # initialize drawing objs
    globals.BALL_A = Circle(Point(0,0), 1)
    globals.PADDLE1_A = Rectangle( Point(0,0), Point(1,1))

    games_played = 0
    numb_bounces = 0
    total_bounces = 0

    # main game loop
    while True:
        
        # give ai the state and make it make a move
        cur_game_state = gs.get_discrete_game_stats()
        move_index = ql.get_best_move_testing( cur_game_state )
        
        ai_move = -globals.PADDLE_VELOCITY
        if move_index == 1:
            ai_move = globals.PADDLE_VELOCITY
        elif move_index == 2:
            ai_move = 0

        # move ball and paddle positions 
        gs.move_ball()
        gs.move_paddle1( ai_move )

        # check for collisions
        gs.edge_detect()
        
        
        if gs.collision_detect():
            numb_bounces += 1

        if gs.detect_gameset():
            games_played += 1
            total_bounces += numb_bounces
            avg = total_bounces / games_played
            print( 'game number:', games_played, '\t numb_bounces:', numb_bounces, '\taverage:', avg )
            numb_bounces = 0
            gs.reset()

            if not ANIMATION_ON:
                time.sleep(0.07)

        if ANIMATION_ON:
            animation.draw_frame( win, gs )

        # time.sleep(0.01)


def train_agent():
    # init globals
    globals.BOARD_LEFT = 0
    globals.BOARD_RIGHT = 100
    globals.BOARD_BOTTOM = 100
    globals.BOARD_TOP = 0
    globals.BOARD_X = 100
    globals.BOARD_Y = 100
    globals.PADDLE1_X = 100
    globals.SCREEN_X = globals.BOARD_X * globals.SCALE
    globals.SCREEN_Y = globals.BOARD_Y * globals.SCALE

    # create game state
    gs = game_state.Game_State( 50, 50, 3, 1, 50, None )

    # create q_learning AI 
    ql = q_learning.Q_Learn()

    # training loop 
    games_played = 0
    numb_bounces = 0
    
    print( 'training: 0%' )
    while games_played < q_learning.TRAINING_LOOP:

        # give ai the state and make it make a move
        cur_game_state = gs.get_discrete_game_stats()
        move_index = ql.get_best_move_training( cur_game_state )
        
        # get ai move from move index
        ai_move = - globals.PADDLE_VELOCITY
        if move_index == 1:
            ai_move = globals.PADDLE_VELOCITY
        elif move_index == 2:
            ai_move = 0

        # move ball and paddle positions 
        gs.move_ball()
        gs.move_paddle1( ai_move )

        # check for collisions
        gs.edge_detect()
        bounce_detected = gs.collision_detect()
        gameset_detected = gs.detect_gameset()
        
        # calculate reward
        reward = 0
        if bounce_detected:
            numb_bounces += 1
            reward = 1
        if gameset_detected:
            reward = -1

        # update q_learning
        new_state = gs.get_discrete_game_stats()
        ql.td_update( cur_game_state, move_index, reward, new_state, games_played )

        # print status
        if gameset_detected and games_played == q_learning.TRAINING_LOOP * 0.25:
            print( 'training: 25% \t numb_bounces:', numb_bounces )

        if gameset_detected and games_played == q_learning.TRAINING_LOOP * 0.5:
            print( 'training: 50% \t numb_bounces:', numb_bounces )

        if gameset_detected and games_played == q_learning.TRAINING_LOOP * 0.75:
            print( 'training: 75% \t numb_bounces:', numb_bounces )

        # check gameset
        if gameset_detected:
            games_played += 1
            numb_bounces = 0
            gs.reset()            

    print( 'training: 100%' )
    print( 'numb_bounces: ', numb_bounces )
    return ql

#
#
# modes:    PvH, PvM, HvM, S
#           P = human player
#           H = hard code
#           M = Machine Learning
#           S = single player machine learning
def start_game( mode, input_dict ):

    if input_dict == None:
        ql = train_agent()

        # save agent info
        q_file = open( 'q_file.txt', 'w' )
        for k in ql.q_dict:
            q_file.write( str(k) + ' ' + str(ql.q_dict[k].qval) + ' ' + str(ql.q_dict[k].count) + '\n' )
        q_file.close()
        
        # save dict
        q_pickle_file = open( 'qlearn.pkl', 'wb' )
        pickle.dump( ql.q_dict, q_pickle_file )

        if sys.platform == 'darwin':
            os.system( 'say "done training" ')

    else:
        ql = q_learning.Q_Learn()
        ql.q_dict = input_dict

    start_S( ql )

    return


def main():        

    # if you are given an already trained agent
    if len(sys.argv) == 2:
        q_file = open( sys.argv[1], 'rb' )
        q_dict = pickle.load(q_file)

        start_game('S', q_dict )

    start_game( 'S', None )


if __name__ == '__main__':
    main()
