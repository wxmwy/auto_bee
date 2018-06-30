import pygame
import main_utils
import time

FPS = 40
SCREENWIDTH  = 1920 #288
SCREENHEIGHT = 1080 #512
pygame.init()
pygame.mixer.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE)
pygame.display.set_caption('Flappy Bird')
start = False
which = [0, 0, 0]
IMAGES, SOUNDS = main_utils.load()

btn_width = IMAGES['btn'].get_width()
btn_height = IMAGES['btn'].get_height()
PLAYERWIDTH = IMAGES['player'][0].get_width()/2
PLAYERHEIGHT = IMAGES['player'][0].get_height()/2


class GameState:
    def __init__(self):
        self.playerx = SCREENWIDTH/2-PLAYERWIDTH
        self.playery = SCREENHEIGHT/2-PLAYERHEIGHT
        self.btnx = SCREENWIDTH/2 - btn_width/2
        self.btny = SCREENHEIGHT/2 - btn_height/2

    def framestep(self, which):
        SCREEN.blit(IMAGES['bg'][which[0]], (0,0))
        SCREEN.blit(IMAGES['player'][which[1]], (self.playerx+3, self.playery+10))
        SCREEN.blit(IMAGES['btn'],(self.btnx+7, self.btny+13))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def hit(x, y, which):
    rst = which
    if (SCREENWIDTH-btn_width)/2 < x <(SCREENWIDTH+btn_width)/2 and (SCREENHEIGHT-btn_height)/2 < y < (SCREENHEIGHT+btn_height)/2:
        if rst[0] != 0 and rst[1] != 0:
            rst[2] = 1
            pygame.mixer.music.load(SOUNDS['choose'])
            pygame.mixer.music.play()
            time.sleep(0.1)
    else:
        if x < SCREENWIDTH /2:
            if y < SCREENHEIGHT/2:
                if x > SCREENWIDTH /2 - PLAYERWIDTH and y > SCREENHEIGHT/2 - PLAYERHEIGHT:
                    #rst[1] = 1 - rst[1]
                    rst[1] = 1
                    if rst[1] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
                else:
                    #rst[0] = 1 - rst[0]
                    rst[0] = 1
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
            else:
                if x > SCREENWIDTH /2 - PLAYERWIDTH and y < SCREENHEIGHT/2 + PLAYERHEIGHT:
                    #rst[1] = 3 - rst[1]
                    rst[1] = 3
                    if rst[1] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
                else:
                    #rst[0] = 3 - rst[0]
                    rst[0] = 3
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
        else:
            if y < SCREENHEIGHT/2:
                if x < SCREENWIDTH/2 + PLAYERWIDTH and y > SCREENHEIGHT/2 - PLAYERHEIGHT:
                    #rst[1] = 2 - rst[1]
                    rst[1] = 2
                    if rst[1] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
                else:
                    #rst[0] = 2 - rst[0]
                    rst[0] = 2
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
            else:
                if  x < SCREENWIDTH/2 + PLAYERWIDTH and y < SCREENHEIGHT/2 + PLAYERHEIGHT:
                    #rst[1] = 4 - rst[1]
                    rst[1] = 4
                    if rst[1] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
                else:
                    #rst[0] = 4 - rst[0]
                    rst[0] = 4
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
    return rst