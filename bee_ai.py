import wrapped_bee as game
import tensorflow as tf
import numpy as np
import pygame
import sys
import bee_utils
import random
from collections import deque
import cv2

GAME = 'bird' # the name of the game being played for log files
ACTIONS = 2 # number of valid actions
GAMMA = 0.99 # decay rate of past observations
OBSERVE = 100000. # timesteps to observe before training
EXPLORE = 2000000. # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001 # final value of epsilon
INITIAL_EPSILON = 0.0001 # starting value of epsilon
REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 32 # size of minibatch
FRAME_PER_ACTION = 1
game_state = game.GameState()
IMAGES, SOUNDS, HITMASKS = bee_utils.load()
SCREENWIDTH  = 1920 #288
SCREENHEIGHT = 1080 #512


def hitbtn(x, y):
    if int(SCREENWIDTH-40-IMAGES['back'].get_width()) <= x <= int(SCREENWIDTH-40) and int(SCREENHEIGHT-40-IMAGES['back'].get_height()) <= y <= int(SCREENHEIGHT-40):
        if HITMASKS['back'][x-int(SCREENWIDTH-40-IMAGES['back'].get_width())][y-int(SCREENHEIGHT-40-IMAGES['back'].get_height())]:
            return 1
    elif int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()) <= x <= int(SCREENWIDTH-40-IMAGES['back'].get_width()) and int(SCREENHEIGHT-40-IMAGES['change'].get_height()) <= y <= int(SCREENHEIGHT-40):
        if HITMASKS['change'][x-int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width())][y-int(SCREENHEIGHT-40-IMAGES['change'].get_height())]:
            return 2
    elif int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()-40-IMAGES['stop'].get_width()) <= x <= int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()) and int(SCREENHEIGHT-40-IMAGES['stop'].get_height()) <= y <= int(SCREENHEIGHT-40):
        if HITMASKS['stop'][x-int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()-40-IMAGES['stop'].get_width())][y-int(SCREENHEIGHT-40-IMAGES['stop'].get_height())]:
            return 3
    elif int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()-40-IMAGES['stop'].get_width()-40-IMAGES['start'].get_width()) <= x <= int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()-40-IMAGES['stop'].get_width()-40) and int(SCREENHEIGHT-40-IMAGES['start'].get_height()) <= y <= int(SCREENHEIGHT-40):
        if HITMASKS['start'][x-int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()-40-IMAGES['stop'].get_width()-40-IMAGES['start'].get_width())][y-int(SCREENHEIGHT-40-IMAGES['start'].get_height())]:
            return 4
    return 0


def hitPixel(x, y, u0, l0, t0):
    uHitmask = HITMASKS['pipe'][t0*2 + 0]
    lHitmask = HITMASKS['pipe'][t0*2 + 1]
    try:
        if uHitmask[x-int(u0['x'])][y - int(u0['y'])]:
            return True
    except IndexError:
        try:
            if lHitmask[x-int(l0['x'])][y - int(l0['y'])]:
                return True
        except IndexError:
            return False
    return False


def hit(x, y, u, l, ty):
    for i in range(0, len(u)):
        if hitPixel(x, y, u[i], l[i], ty[i]):
            return i
    return -1


def main(level, sess, readout, s):
    start = False
    epsilon = INITIAL_EPSILON
    t = 0
    py = 0
    drag = False
    show = False
    which = -1
    # get the first state by doing nothing and pre process the image to 80x80x4
    game_state.__init__()
    do_nothing = np.zeros(ACTIONS)
    do_nothing[0] = 1
    x_t, r_0, terminal, u, l, ty, score = game_state.frame_step(do_nothing, start, level, show)
    x_t = cv2.cvtColor(cv2.resize(x_t, (80, 80)), cv2.COLOR_BGR2GRAY)
    ret, x_t = cv2.threshold(x_t, 1, 255, cv2.THRESH_BINARY)
    s_t = np.stack((x_t, x_t, x_t, x_t), axis=2)
    die = True

    while not terminal:
        if start:
            readout_t = readout.eval(feed_dict={s : [s_t]})[0]
            a_t = np.zeros([ACTIONS])
            action_index = 0
            if t % FRAME_PER_ACTION == 0:
                action_index = np.argmax(readout_t)
                a_t[action_index] = 1
            else:
                a_t[0] = 1  # do nothing

            # scale down epsilon
            if epsilon > FINAL_EPSILON and t > OBSERVE:
                epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE
            x_t1_colored, r_t, terminal, _, _, _, score = game_state.frame_step(a_t, start, level, show)
            x_t1 = cv2.cvtColor(cv2.resize(x_t1_colored, (80, 80)), cv2.COLOR_BGR2GRAY)
            ret, x_t1 = cv2.threshold(x_t1, 1, 255, cv2.THRESH_BINARY)
            x_t1 = np.reshape(x_t1, (80, 80, 1))
            s_t1 = np.append(x_t1, s_t[:, :, :3], axis=2)

            # update the old values
            s_t = s_t1
            t += 1

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    try:
                        tmpt = hitbtn(pos[0], pos[1])
                    except Exception:
                        tmpt = 0
                    if tmpt != 0:
                        if tmpt == 1:
                            terminal, die, show = True, False, False
                            pygame.mixer.music.load(SOUNDS['start'])
                            pygame.mixer.music.play()
                        elif tmpt == 2:
                            show = not show
                            pygame.mixer.music.load(SOUNDS['start'])
                            pygame.mixer.music.play()
                        elif tmpt == 3:
                            start = False
                            pygame.mixer.music.load(SOUNDS['stop'])
                            pygame.mixer.music.play()
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not drag:
                        try:
                            tmpt = hitbtn(pos[0], pos[1])
                        except Exception:
                            tmpt = 0
                        if tmpt != 0:
                            if tmpt == 1:
                                terminal = True
                                die = False
                                show = False
                                pygame.mixer.music.load(SOUNDS['start'])
                                pygame.mixer.music.play()
                            # elif tmpt == 2:
                            #     cv2.imshow('test',s_t1)
                            elif tmpt == 4:
                                start = True
                                pygame.mixer.music.load(SOUNDS['start'])
                                pygame.mixer.music.play()
                        else:   
                            which = hit(pos[0], pos[1], u, l, ty)
                            if -1 != which:
                                py = pos[1]
                                drag = True
                                pygame.mixer.music.load(SOUNDS['change'])
                                pygame.mixer.music.play()
                elif event.type == pygame.MOUSEMOTION:
                    if drag:
                        pos = pygame.mouse.get_pos()
                        game_state.changePipe(pos[1]-py, which)
                        py = pos[1]
                        _, _, terminal, u, l, ty, score = game_state.frame_step(do_nothing, start, level, show)
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag = False
    while die:
        for event in pygame.event.get():
            # TODO
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    die = False
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
