import globals
import json
import game_play

TRAINING_LOOP = 200000
alpha = TRAINING_LOOP/1000
gamma = 0.94
utility_boost = 1.1      # used for move selection during training and is never returned as a val
boost_count_max = 10


# look into P(s'|s,a'') for when you are choosing the action
#    naw we dont need this because this is model free learning


# main Q_Learn data structure is a dictionary where:
#       key = state 
#       value = State_Info class instance
# 
#     state | action| count | qval
#   ========================================
#      S1   |   u   |   c1  |   q1
#           |   d   |   c2  |   q2
#           |   s   |   c3  |   q3
#   ----------------------------------------
#      S2   |   u   |   c1  |   q1
#           |   d   |   c2  |   q2
#           |   s   |   c3  |   q3
#
#       and so on

class State_Info:
    def __init__(self):
        self.action = [ -globals.PADDLE_VELOCITY, globals.PADDLE_VELOCITY, 0 ]
        self.count = [0, 0, 0]
        self.qval = [0.0, 0.0, 0.0]

class Q_Learn:
    def __init__(self):
        self.q_dict = dict()

    # get_best_move_training
    # argmax a' f(Q(s,a'), N(s,a'))
    # f = exploration function
    # N = number of times we've seen the state move pair 
    # Q = action utility function

    # input:    state given as a tuple of values. 
    # return:   returns the move that the paddle should make, either up down or still
    def get_best_move_training( self, state ):
        global utility_boost
        global boost_count_max

        # check if we've seen this state before
        if not state in self.q_dict:
            self.q_dict[state] = State_Info()

        cur_state_vals = self.q_dict[state]

        # find utility values (qval)
        up_val = cur_state_vals.qval[0]
        down_val = cur_state_vals.qval[1]
        still_val = cur_state_vals.qval[2]

        # check if we need to add boost (R+)
        if cur_state_vals.count[0] < boost_count_max:
            up_val = utility_boost
        if cur_state_vals.count[1] < boost_count_max:
            down_val = utility_boost
        if cur_state_vals.count[2] < boost_count_max:
            still_val = utility_boost


        # get the max of the possible actions
        move_index = 0
        max_util = up_val
        if down_val > max_util:
            move_index = 1
            max_util = down_val
        if still_val > max_util:
            move_index = 2
            max_util = still_val



        # update count 
        self.q_dict[state].count[move_index] += 1

        return move_index


    # get_best_move_testing
    # use for testing the agent
    def get_best_move_testing( self, state ):

        # check if we've seen this state before
        if not state in self.q_dict:
            self.q_dict[state] = State_Info()
            print( 'new state found during testing' )

        cur_state_vals = self.q_dict[state]

        # find utility values (qval)
        up_val = cur_state_vals.qval[0]
        down_val = cur_state_vals.qval[1]
        still_val = cur_state_vals.qval[2]

        # get the max of the possible actions
        move_index = 0
        max_util = up_val
        if down_val > max_util:
            move_index = 1
            max_util = down_val
        if still_val > max_util:
            move_index = 2
            max_util = still_val

        return move_index

    
    # get_best_util
    def get_best_util( self, state ):

        # check if we've seen this state before
        if not state in self.q_dict:
            self.q_dict[state] = State_Info()

        cur_state_vals = self.q_dict[state]

        # find utility values (qval)
        up_val = cur_state_vals.qval[0]
        down_val = cur_state_vals.qval[1]
        still_val = cur_state_vals.qval[2]

        # get the max of the possible actions
        max_util = up_val
        if down_val > max_util:
            max_util = down_val
        if still_val > max_util:
            max_util = still_val

        return max_util

    # td_update
    # temporal difference update
    # Q(s,a) <-- Q(s,a) + alpha * (R(s) + gamma max a' Q(s',a') - Q(s,a) )
    # call this function after adjusting the state for the move that was made
    # this function updates the q_dict
    # Input:    cur_state 
    #           cur_move 
    #           bounce_detected - get from collision detection 
    #           result_state - whats the result after making cur_move
    # Return:   none
    #
    # Note:     check later if the bounce detection should come from cur state or previous state
    def td_update( self, cur_state, move_index, reward, result_state, count ):
        global alpha
        global gamma
        global TRAINING_LOOP
        global boost_count_max

        # lr = alpha/(alpha + count )
        lr = alpha/(alpha + self.q_dict[cur_state].count[move_index] )
        # boost_count_max = TRAINING_LOOP / (TRAINING_LOOP + count)
        # boost_count_max = 1 - count/(TRAINING_LOOP * 2)
        # gamma2 = TRAINING_LOOP/(TRAINING_LOOP + (count/100))

        # get best utility for result_state
        next_max_util = self.get_best_util( result_state )


        # calculate new val for q
        old_q_val = self.q_dict[cur_state].qval[move_index]
        new_q_val = old_q_val + lr * (reward + gamma * next_max_util - old_q_val )

        self.q_dict[cur_state].qval[move_index] = new_q_val

        return


    def export_q_dict(self):

        q_dict_file = open( 'q_dict.json', 'w+' )



        #TODO
        pass