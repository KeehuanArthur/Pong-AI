This is a python script that uses Q-learning to teach itself how to play pong. To do this, it tries to bounce the
ball against a wall for as long as possible. The more it can bounce the ball, the higher the reward. The sensory
inputs to this algorithm are:
    - ball's position where the board is split into a 12 by 12 grid
    - the velocity of the ball
    - position of the paddle

To run the script, use python game_play.py. This will start the Q-learning algorithm and will play 200000
games by itself. This process takes about 30 minutes. The training time will depend on the processor it
is running on. After this, a window will pop up with the AI bouncing the ball.

When the training process is done, it will save a file called qlearn.pkl. This file contains the dictionary
of values used by the Q-learning algorithm during the game play. To used pre-trained data, use the
command python game_play.py <name of pkl file>

To display the graphics, I used graphics.py.
        http://mcsp.wartburg.edu/zelle/python/graphics.py
        http://mcsp.wartburg.edu/zelle/python/graphics/graphics.pdf

