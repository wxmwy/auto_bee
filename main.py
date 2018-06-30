import sys
import wrapped_main as game
import pygame
import bee_ai as bee
import flytrap_ai as flytrap
import mountain_ai as mountain
import spider_ai as spider
import tensorflow as tf

ACTIONS = 2 # number of valid actions

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.01, shape = shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides = [1, stride, stride, 1], padding = "SAME")

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")

def createNetwork():
    # network weights
    W_conv1 = weight_variable([8, 8, 4, 32])
    b_conv1 = bias_variable([32])

    W_conv2 = weight_variable([4, 4, 32, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([3, 3, 64, 64])
    b_conv3 = bias_variable([64])

    W_fc1 = weight_variable([1600, 512])
    b_fc1 = bias_variable([512])

    W_fc2 = weight_variable([512, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # input layer
    s = tf.placeholder("float", [None, 80, 80, 4])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(s, W_conv1, 4) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, 2) + b_conv2)
    #h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 1) + b_conv3)
    #h_pool3 = max_pool_2x2(h_conv3)

    #h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
    h_conv3_flat = tf.reshape(h_conv3, [-1, 1600])

    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)

    # readout layer
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return s, readout, h_fc1


which = [0,0,0]
game_state = game.GameState()
start = False

sess = tf.InteractiveSession()
s, readout, h_fc1 = createNetwork()
# define the cost function
a = tf.placeholder("float", [None, ACTIONS])
y = tf.placeholder("float", [None])
readout_action = tf.reduce_sum(tf.multiply(readout, a), reduction_indices=1)
saver = tf.train.Saver()
sess.run(tf.initialize_all_variables())
checkpoint = tf.train.get_checkpoint_state("saved_networks")
if checkpoint and checkpoint.model_checkpoint_path:
    saver.restore(sess, checkpoint.model_checkpoint_path)
    print("Successfully loaded:", checkpoint.model_checkpoint_path)
else:
    print("Could not find old network weights")

while True:
    game_state.__init__()
    game_state.framestep(which)
    if start:
        if which[0] == 1:
            pygame.mixer.music.load('sounds/m1.mp3')
            pygame.mixer.music.play()
            flytrap.main(which[1]-1, sess, readout, s)
        elif which[0] == 2:
            pygame.mixer.music.load('sounds/m2.mp3')
            pygame.mixer.music.play()
            spider.main(which[1]-1, sess, readout, s)
        elif which[0] == 3:
            pygame.mixer.music.load('sounds/m3.mp3')
            pygame.mixer.music.play()
            mountain.main(which[1]-1, sess, readout, s)
        elif which[0] == 4:
            pygame.mixer.music.load('sounds/m4.mp3')
            pygame.mixer.music.play()
            bee.main(which[1]-1, sess, readout, s)
        start = False
        which = [0,0,0]
    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                which = game.hit(pos[0], pos[1], which)
                if(which[2] == 1):
                    start = True
                    # start game
                else:
                    game_state.framestep(which)