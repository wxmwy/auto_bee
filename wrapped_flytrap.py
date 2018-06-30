import numpy as np
import sys
import random
import array
import pygame
import flytrap_utils
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle

FPS = 40
SCREENWIDTH  = 1920 #288
SCREENHEIGHT = 1080 #512

pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), NOFRAME|FULLSCREEN)
pygame.display.set_caption('Flappy Bird')

IMAGES, SOUNDS, HITMASKS = flytrap_utils.load()
PIPEGAPSIZE = int(100*SCREENHEIGHT/512) # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79

PLAYER_WIDTH = IMAGES['player'][0].get_width()
PLAYER_HEIGHT = IMAGES['player'][0].get_height()
PIPE_WIDTH = IMAGES['pipe'][0].get_width()
PIPE_HEIGHT = IMAGES['pipe'][0].get_height()
BACKGROUND_WIDTH = IMAGES['background'].get_width()

PLAYER_INDEX_GEN = cycle([0, 1, 2, 1])


class GameState:
    def __init__(self):
        self.playermark = self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(SCREENWIDTH/3* 0.2)
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)
        self.basex = 0
        # self.baseShift = IMAGES['base'].get_width() - BACKGROUND_WIDTH

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()
        newPipe3 = getRandomPipe()
        newPipe4 = getRandomPipe()
        newPipe5 = getRandomPipe()
        newPipe6 = getRandomPipe()
        self.upperPipes = [
            {'x': SCREENWIDTH * 0.33, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH * 0.495, 'y': newPipe2[0]['y']},
            {'x': SCREENWIDTH * 0.66, 'y': newPipe3[0]['y']},
            {'x': SCREENWIDTH * 0.825, 'y': newPipe4[0]['y']},
            {'x': SCREENWIDTH * 0.99, 'y': newPipe5[0]['y']},
            {'x': SCREENWIDTH * 1.155, 'y': newPipe6[0]['y']},
        ]
        self.lowerPipes = [
            {'x': SCREENWIDTH * 0.33, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH * 0.495, 'y': newPipe2[1]['y']},
            {'x': SCREENWIDTH * 0.66, 'y': newPipe3[1]['y']},
            {'x': SCREENWIDTH * 0.825, 'y': newPipe4[1]['y']},
            {'x': SCREENWIDTH * 0.99, 'y': newPipe5[1]['y']},
            {'x': SCREENWIDTH * 1.155, 'y': newPipe6[1]['y']},
        ]
        self.typePipes = [
            newPipe1[2],
            newPipe2[2],
            newPipe3[2],
            newPipe4[2],
            newPipe5[2],
            newPipe6[2],
        ]

        # player velocity, max velocity, downward accleration, accleration on flap
        self.pipeVelX = -4*SCREENWIDTH/288/3
        self.playerVelY    =  0    # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY =  10*SCREENHEIGHT/512   # max vel along Y, max descend speed
        self.playerMinVelY =  -8*SCREENHEIGHT/512   # min vel along Y, max ascend speed
        self.playerAccY    =   1*SCREENHEIGHT/512   # players downward accleration
        self.playerFlapAcc =  -9*SCREENHEIGHT/512   # players speed on flapping
        self.playerFlapped = False # True when player flaps
        self.ppnt = 0

    def frame_step(self, input_actions, start, level, show):
        pygame.event.pump()

        reward = 0.1
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')
        if start:
            # input_actions[0] == 1: do nothing
            # input_actions[1] == 1: flap the bird
            if input_actions[1] == 1:
                if self.playery > -2 * PLAYER_HEIGHT:
                    self.playerVelY = self.playerFlapAcc
                    self.playerFlapped = True
                    #SOUNDS['wing'].play()

            # check for score
            playerMidPos = self.playerx + PLAYER_WIDTH / 2
            for pipe in self.upperPipes:
                pipeMidPos = pipe['x'] + PIPE_WIDTH / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 4*SCREENWIDTH/288/3:
                    self.score += 1
                    self.ppnt = 1
                    pygame.mixer.music.load(SOUNDS['cheer'])
                    pygame.mixer.music.play()
                    reward = 1

            # playerIndex basex change
            if (self.loopIter + 1) % 3 == 0:
                self.playerIndex = next(PLAYER_INDEX_GEN)
            self.loopIter = (self.loopIter + 1) % 30
            self.basex = (self.basex - self.pipeVelX) % SCREENWIDTH

            # player's movement
            if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
                self.playerVelY += self.playerAccY
            if self.playerFlapped:
                self.playerFlapped = False
            self.playery += min(self.playerVelY, BASEY - self.playery - PLAYER_HEIGHT)
            if self.playery < 0:
                self.playery = 0

            # move pipes to left
            for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
                uPipe['x'] += self.pipeVelX
                lPipe['x'] += self.pipeVelX

            # add new pipe when first pipe is about to touch left of screen
            if 0 < self.upperPipes[0]['x'] < -self.pipeVelX:
                newPipe = getRandomPipe()
                self.upperPipes.append(newPipe[0])
                self.lowerPipes.append(newPipe[1])
                self.typePipes.append(newPipe[2])

            # remove first pipe if its out of the screen
            if self.upperPipes[0]['x'] < -PIPE_WIDTH:
                self.upperPipes.pop(0)
                self.lowerPipes.pop(0)
                self.typePipes.pop(0)
                self.ppnt = 0
                # newPipe = getRandomPipe()
                # self.upperPipes.append(newPipe[0])
                # self.lowerPipes.append(newPipe[1])
                # self.typePipes.append(newPipe[2])

            # check if crash here
            isCrash= checkCrash({'x': self.playerx, 'y': self.playery,
                                'index': level*13+self.playerIndex*4+self.playermark},
                                self.upperPipes, self.lowerPipes, self.typePipes)
            if self.score < 10 :
                self.playermark = 0
            elif 9 < self.score < 20:
                self.playermark = 1
            elif 19 < self.score < 30:
                self.playermark = 2
            elif 29 < self.score:
                self.playermark = 3
            if isCrash:
                #SOUNDS['hit'].play()
                #SOUNDS['die'].play()
                terminal = True
                #self.__init__()
                pygame.mixer.music.load(SOUNDS['die'])
                pygame.mixer.music.play()
                reward = -1
                self.playermark = 4

        # # draw sprites
        # SCREEN.blit(IMAGES['background'], (-self.basex,0))

        # for uPipe, lPipe, typep in zip(self.upperPipes, self.lowerPipes, self.typePipes):
        #     SCREEN.blit(IMAGES['pipe'][typep*2+0], (uPipe['x'], uPipe['y']))
        #     SCREEN.blit(IMAGES['pipe'][typep*2+1], (lPipe['x'], lPipe['y']))

        # SCREEN.blit(IMAGES['base'], (-self.basex, BASEY))
        # # print score so player overlaps the score
        # showScore(self.score)
        # SCREEN.blit(IMAGES['player'][self.playerIndex],
        #             (self.playerx, self.playery))

        # #image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        # pygame.display.update()
        # FPSCLOCK.tick(FPS)

        # fake 
        SCREEN.blit(IMAGES['background-fake'], (0,0))

        for uPipe, lPipe, typep in zip(self.upperPipes, self.lowerPipes, self.typePipes):
            SCREEN.blit(IMAGES['pipe-fake'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe-fake'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base-fake'], (-self.basex, BASEY))
        # print score so player overlaps the score
        #showScore(self.score)
        SCREEN.blit(IMAGES['player-fake'][self.playerIndex],
                    (self.playerx, self.playery))

        #print self.upperPipes[0]['y'] + PIPE_HEIGHT - int(BASEY * 0.2)
        image_d = pygame.surfarray.array3d(pygame.display.get_surface())
        indice = []
        brend = SCREENWIDTH
        if level == 1:
            brend /= 2.5
        elif level == 2:
            brend /= 2.7
        elif level == 3:
            brend /= 3
        else:
            brend /=2.2
        for i in range(0, int(brend)):
            indice.append(i)
        image_data = image_d.take(indice, axis = 0)

        # draw true sprites
        SCREEN.blit(IMAGES['background'], (-self.basex,0))

        for uPipe, lPipe, typep in zip(self.upperPipes, self.lowerPipes, self.typePipes):
            SCREEN.blit(IMAGES['pipe'][typep*2+0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][typep*2+1], (lPipe['x'], lPipe['y']))
            SCREEN.blit(IMAGES['pipe'][typep*2+4], (uPipe['x'], 0))
            SCREEN.blit(IMAGES['pipe'][typep*2+5], (lPipe['x'], SCREENHEIGHT-IMAGES['pipe'][typep*2+5].get_height()))

        # SCREEN.blit(IMAGES['base'], (-self.basex, BASEY))
        # print score so player overlaps the score
        showScore(self.score)
        SCREEN.blit(IMAGES['player'][level*13+self.playerIndex*4+self.playermark],
                    (self.playerx, self.playery))
        SCREEN.blit(IMAGES['back'],(SCREENWIDTH-40-IMAGES['back'].get_width(), SCREENHEIGHT-40-IMAGES['back'].get_height()))
        SCREEN.blit(IMAGES['change'], (SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width(), SCREENHEIGHT-40-IMAGES['change'].get_height()))
        SCREEN.blit(IMAGES['stop'], (SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()-40-IMAGES['stop'].get_width(), SCREENHEIGHT-40-IMAGES['stop'].get_height()))
        SCREEN.blit(IMAGES['start'], (SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['change'].get_width()-40-IMAGES['stop'].get_width()-40-IMAGES['start'].get_width(), SCREENHEIGHT-40-IMAGES['start'].get_height()))
        if show:
            color = 0,0,255
            if self.playerVelY < 0:
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery), (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery+self.playerVelY*2),5)
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width()/2+5,self.playery+self.playerVelY*2+5), (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery+self.playerVelY*2),3)
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width()/2-5,self.playery+self.playerVelY*2+5), (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery+self.playerVelY*2),3)
            elif self.playerVelY > 0:
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery+IMAGES['player'][level*13].get_width()), (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery+IMAGES['player'][level*13].get_width()+self.playerVelY*2),5)
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width()/2+5,self.playery+IMAGES['player'][level*13].get_width()+self.playerVelY*2-5), (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery+IMAGES['player'][level*13].get_width()+self.playerVelY*2),3)
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width()/2-5,self.playery+IMAGES['player'][level*13].get_width()+self.playerVelY*2-5), (self.playerx+IMAGES['player'][level*13].get_width()/2,self.playery+IMAGES['player'][level*13].get_width()+self.playerVelY*2),3)
            if self.ppnt == 0:
                color = 0,255,0
                font = pygame.font.SysFont('arial',16)
                distan = font.render(str(self.upperPipes[self.ppnt+1]['x']-self.playerx), True, color)
                SCREEN.blit(distan, ((self.playerx+IMAGES['player'][level*13].get_width()+self.upperPipes[self.ppnt+1]['x'])/2,self.upperPipes[self.ppnt+1]['y']+PIPE_HEIGHT))
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width(), self.upperPipes[self.ppnt+1]['y']+PIPE_HEIGHT), (self.upperPipes[self.ppnt+1]['x'],self.upperPipes[self.ppnt+1]['y']+PIPE_HEIGHT),5)
                
                distan = font.render(str(self.lowerPipes[self.ppnt+1]['x']-self.playerx), True, color)
                SCREEN.blit(distan, ((self.playerx+IMAGES['player'][level*13].get_width()+self.lowerPipes[self.ppnt+1]['x'])/2,self.lowerPipes[self.ppnt+1]['y']))
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width(), self.lowerPipes[self.ppnt+1]['y']), (self.lowerPipes[self.ppnt+1]['x'],self.lowerPipes[self.ppnt+1]['y']),5)
                
                distan = font.render(str(self.upperPipes[self.ppnt+1]['y']+PIPE_HEIGHT-self.playery), True, color)
                SCREEN.blit(distan, (self.playerx+IMAGES['player'][level*13].get_width()+6,(self.upperPipes[self.ppnt+1]['y']+PIPE_HEIGHT+self.playery)/2))
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width(), self.playery), (self.playerx+IMAGES['player'][level*13].get_width(),self.upperPipes[self.ppnt+1]['y']+PIPE_HEIGHT),5)
                
                distan = font.render(str(self.lowerPipes[self.ppnt+1]['y']-self.playery-IMAGES['player'][level*13].get_height()), True, color)
                SCREEN.blit(distan, (self.playerx+IMAGES['player'][level*13].get_width()+6,(self.lowerPipes[self.ppnt+1]['y']+self.playery+IMAGES['player'][level*13].get_height())/2))
                pygame.draw.aaline(SCREEN, color, (self.playerx+IMAGES['player'][level*13].get_width(), self.playery+IMAGES['player'][level*13].get_height()), (self.playerx+IMAGES['player'][level*13].get_width(),self.lowerPipes[self.ppnt+1]['y']),5)

            color = 255,0,0
            font = pygame.font.SysFont('arial',16)
            distan = font.render(str(self.upperPipes[self.ppnt]['x']-self.playerx), True, color)
            SCREEN.blit(distan, ((self.playerx+self.upperPipes[self.ppnt]['x'])/2,self.upperPipes[self.ppnt]['y']+PIPE_HEIGHT))
            pygame.draw.aaline(SCREEN, color, (self.playerx, self.upperPipes[self.ppnt]['y']+PIPE_HEIGHT), (self.upperPipes[self.ppnt]['x'],self.upperPipes[self.ppnt]['y']+PIPE_HEIGHT),5)
            
            distan = font.render(str(self.lowerPipes[self.ppnt]['x']-self.playerx), True, color)
            SCREEN.blit(distan, ((self.playerx+self.lowerPipes[self.ppnt]['x'])/2,self.lowerPipes[self.ppnt]['y']))
            pygame.draw.aaline(SCREEN, color, (self.playerx, self.lowerPipes[self.ppnt]['y']), (self.lowerPipes[self.ppnt]['x'],self.lowerPipes[self.ppnt]['y']),5)
            
            distan = font.render(str(self.upperPipes[self.ppnt]['y']+PIPE_HEIGHT-self.playery), True, color)
            SCREEN.blit(distan, (self.playerx+6,(self.upperPipes[self.ppnt]['y']+PIPE_HEIGHT+self.playery)/2))
            pygame.draw.aaline(SCREEN, color, (self.playerx, self.playery), (self.playerx,self.upperPipes[self.ppnt]['y']+PIPE_HEIGHT),5)
            
            distan = font.render(str(self.lowerPipes[self.ppnt]['y']-self.playery-IMAGES['player'][level*13].get_height()), True, color)
            SCREEN.blit(distan, (self.playerx+6,(self.lowerPipes[self.ppnt]['y']+self.playery+IMAGES['player'][level*13].get_height())/2))
            pygame.draw.aaline(SCREEN, color, (self.playerx, self.playery+IMAGES['player'][level*13].get_height()), (self.playerx,self.lowerPipes[self.ppnt]['y']),5)

            if input_actions[1] == 1:
                font = pygame.font.SysFont('arial',30)
                distan = font.render('press',True, color)
                SCREEN.blit(distan, (self.playerx+IMAGES['player'][level*13].get_width(), self.playery+IMAGES['player'][level*13].get_height()/2))
                
            #pygame.draw.aaline(SCREEN, color, (SCREENWIDTH/3, 0), (SCREENWIDTH/3, SCREENHEIGHT), 3)

        if terminal:
             SCREEN.blit(IMAGES['end'], ((SCREENWIDTH-IMAGES['end'].get_width())/2, (SCREENHEIGHT-IMAGES['end'].get_height())/2))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        return image_data, reward, terminal, self.upperPipes, self.lowerPipes, self.typePipes, self.score

    def changePipe(self, dy, w):
        self.upperPipes[w]['y'] += dy
        self.lowerPipes[w]['y'] += dy
        if   not (int(20*SCREENHEIGHT/512 + BASEY*0.2 - PIPE_HEIGHT) < self.upperPipes[w]['y'] < int(90*SCREENHEIGHT/512 + BASEY*0.2 - PIPE_HEIGHT)):
            self.upperPipes[w]['y'] -= dy
            self.lowerPipes[w]['y'] -= dy

def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapYs = [20, 30, 40, 50, 60, 70, 80, 90]

    index = random.randint(0, len(gapYs)-1)
    gapY = int(gapYs[index]*SCREENHEIGHT/512)

    gapY += int(BASEY * 0.2)
    pipeX = SCREENWIDTH + 10*SCREENWIDTH/288

    typeP = random.randint(0,1)

    return [
        {'x': pipeX, 'y': gapY - PIPE_HEIGHT},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
        typeP,
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()
    
    scorewidth = IMAGES['score'].get_width()
    scoreheight = IMAGES['score'].get_height()
    
    Xoffset = SCREENWIDTH -40-scorewidth
    Yoffset = 40 + (IMAGES['score'].get_height() - IMAGES['numbers'][digit].get_height())/2
    SCREEN.blit(IMAGES['score'], (Xoffset, 40))
    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset+ 20, Yoffset))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes, typePipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return True
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])

        for uPipe, lPipe, typep in zip(upperPipes, lowerPipes, typePipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)
            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][typep*2+0]
            lHitmask = HITMASKS['pipe'][typep*2+1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)
            if uCollide or lCollide:
                return True

    return False

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            try:
                if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                    return True
            except BaseException:
                return True
    return False
