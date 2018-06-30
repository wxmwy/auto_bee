import pygame
import sys
def load():
    # path of player with different states
    PLAYER_PATH = ('assets/player/p11a.png',
    'assets/player/p11b.png',
    'assets/player/p11c.png',
    'assets/player/p11d.png',
    'assets/player/p12a.png',
    'assets/player/p12b.png',
    'assets/player/p12c.png',
    'assets/player/p12d.png',
    'assets/player/p13a.png',
    'assets/player/p13b.png',
    'assets/player/p13c.png',
    'assets/player/p13d.png',
    'assets/player/p1die.png',
    'assets/player/p21a.png',
    'assets/player/p21b.png',
    'assets/player/p21c.png',
    'assets/player/p21d.png',
    'assets/player/p22a.png',
    'assets/player/p22b.png',
    'assets/player/p22c.png',
    'assets/player/p22d.png',
    'assets/player/p23a.png',
    'assets/player/p23b.png',
    'assets/player/p23c.png',
    'assets/player/p23d.png',
    'assets/player/p2die.png',
    'assets/player/p31a.png',
    'assets/player/p31b.png',
    'assets/player/p31c.png',
    'assets/player/p31d.png',
    'assets/player/p32a.png',
    'assets/player/p32b.png',
    'assets/player/p32c.png',
    'assets/player/p32d.png',
    'assets/player/p33a.png',
    'assets/player/p33b.png',
    'assets/player/p33c.png',
    'assets/player/p33d.png',
    'assets/player/p3die.png',
    'assets/player/p41a.png',
    'assets/player/p41b.png',
    'assets/player/p41c.png',
    'assets/player/p41d.png',
    'assets/player/p42a.png',
    'assets/player/p42b.png',
    'assets/player/p42c.png',
    'assets/player/p42d.png',
    'assets/player/p43a.png',
    'assets/player/p43b.png',
    'assets/player/p43c.png',
    'assets/player/p43d.png',
    'assets/player/p4die.png',
    )



    # path of pipe
    PIPE_PATH = (
        'assets/spider/plant1.png',
        'assets/spider/plant2.png',
        'assets/spider/plant3.png',
        'assets/spider/plant4.png',
    )


    IMAGES, SOUNDS, HITMASKS = {}, {}, {}

    IMAGES['score'] = pygame.image.load('assets/spider/score.png').convert_alpha()
    IMAGES['end'] = pygame.image.load('assets/spider/end.png').convert_alpha()
    IMAGES['start'] = pygame.image.load('assets/spider/start.png').convert_alpha()
    IMAGES['stop'] = pygame.image.load('assets/spider/stop.png').convert_alpha()
    IMAGES['change'] = pygame.image.load('assets/spider/change.png').convert_alpha()
    IMAGES['back'] = pygame.image.load('assets/spider/back.png').convert_alpha()

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/number/0.png').convert_alpha(),
        pygame.image.load('assets/number/1.png').convert_alpha(),
        pygame.image.load('assets/number/2.png').convert_alpha(),
        pygame.image.load('assets/number/3.png').convert_alpha(),
        pygame.image.load('assets/number/4.png').convert_alpha(),
        pygame.image.load('assets/number/5.png').convert_alpha(),
        pygame.image.load('assets/number/6.png').convert_alpha(),
        pygame.image.load('assets/number/7.png').convert_alpha(),
        pygame.image.load('assets/number/8.png').convert_alpha(),
        pygame.image.load('assets/number/9.png').convert_alpha()
    )

    # base (ground) sprite
    # IMAGES['base'] = pygame.image.load('assets/number/base.png').convert_alpha()
    IMAGES['base-fake'] = pygame.image.load('assets/fake/base.png').convert_alpha()

    # # sounds
    SOUNDS['start'] = 'sounds/start.mp3'
    SOUNDS['cheer'] = 'sounds/cheer.mp3'
    SOUNDS['die'] = 'sounds/die.mp3'
    SOUNDS['stop'] = 'sounds/stop.mp3'
    SOUNDS['change'] = 'sounds/change.mp3'

    # select random background sprites
    IMAGES['background'] = pygame.image.load('assets/spider/bg.png').convert()
    IMAGES['background-fake'] = pygame.image.load('assets/fake/background.png').convert()

    # select random player sprites
    IMAGES['player'] = (
        pygame.image.load(PLAYER_PATH[0]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[1]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[2]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[3]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[4]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[5]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[6]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[7]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[8]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[9]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[10]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[11]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[12]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[13]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[14]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[15]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[16]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[17]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[18]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[19]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[20]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[21]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[22]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[23]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[24]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[25]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[26]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[27]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[28]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[29]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[20]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[31]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[32]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[33]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[34]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[35]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[36]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[37]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[38]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[39]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[40]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[41]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[42]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[43]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[44]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[45]).convert_alpha(), 
        pygame.image.load(PLAYER_PATH[46]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[47]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[48]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[49]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[50]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[51]).convert_alpha(),

    )

    IMAGES['player-fake'] = (
        pygame.image.load('assets/fake/player-up.png').convert_alpha(),
        pygame.image.load('assets/fake/player-mid.png').convert_alpha(),
        pygame.image.load('assets/fake/player-down.png').convert_alpha(),
        pygame.image.load('assets/fake/playerdie.png').convert_alpha(),
    )

    # select random pipe sprites
    IMAGES['pipe'] = (
        pygame.image.load(PIPE_PATH[0]).convert_alpha(),
        pygame.image.load(PIPE_PATH[1]).convert_alpha(),
        pygame.image.load(PIPE_PATH[2]).convert_alpha(),
        pygame.image.load(PIPE_PATH[3]).convert_alpha(),
    )

    IMAGES['pipe-fake'] = (
        pygame.transform.rotate(pygame.image.load('assets/fake/pipe.png').convert_alpha(), 180),
        pygame.image.load('assets/fake/pipe.png').convert_alpha(),
    )

    # hismask for pipes
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0]),
        getHitmask(IMAGES['pipe'][1]),
        getHitmask(IMAGES['pipe'][2]),
        getHitmask(IMAGES['pipe'][3]),
    )

    HITMASKS['back'] = getHitmask(IMAGES['back'])
    HITMASKS['change'] = getHitmask(IMAGES['change'])
    HITMASKS['stop'] = getHitmask(IMAGES['stop'])
    HITMASKS['start'] = getHitmask(IMAGES['start'])

    # hitmask for player
    HITMASKS['player'] = (
         getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
        getHitmask(IMAGES['player'][3]),
        getHitmask(IMAGES['player'][4]),
        getHitmask(IMAGES['player'][5]),
        getHitmask(IMAGES['player'][6]),
        getHitmask(IMAGES['player'][7]),
        getHitmask(IMAGES['player'][8]),
        getHitmask(IMAGES['player'][9]),
        getHitmask(IMAGES['player'][10]),
        getHitmask(IMAGES['player'][11]),
        getHitmask(IMAGES['player'][12]),
        getHitmask(IMAGES['player'][13]),
        getHitmask(IMAGES['player'][14]),
        getHitmask(IMAGES['player'][15]),
        getHitmask(IMAGES['player'][16]),
        getHitmask(IMAGES['player'][17]),
        getHitmask(IMAGES['player'][18]),
        getHitmask(IMAGES['player'][19]),
        getHitmask(IMAGES['player'][20]),
        getHitmask(IMAGES['player'][21]),
        getHitmask(IMAGES['player'][22]),
        getHitmask(IMAGES['player'][23]),
        getHitmask(IMAGES['player'][24]),
        getHitmask(IMAGES['player'][25]),
        getHitmask(IMAGES['player'][26]),
        getHitmask(IMAGES['player'][27]),
        getHitmask(IMAGES['player'][28]),
        getHitmask(IMAGES['player'][29]),
        getHitmask(IMAGES['player'][30]),
        getHitmask(IMAGES['player'][31]),
        getHitmask(IMAGES['player'][32]),
        getHitmask(IMAGES['player'][33]),
        getHitmask(IMAGES['player'][34]),
        getHitmask(IMAGES['player'][35]),
        getHitmask(IMAGES['player'][36]),
        getHitmask(IMAGES['player'][37]),
        getHitmask(IMAGES['player'][38]),
        getHitmask(IMAGES['player'][39]),
        getHitmask(IMAGES['player'][40]),
        getHitmask(IMAGES['player'][41]),
        getHitmask(IMAGES['player'][42]),
        getHitmask(IMAGES['player'][43]),
        getHitmask(IMAGES['player'][44]),
        getHitmask(IMAGES['player'][45]),
        getHitmask(IMAGES['player'][46]),
        getHitmask(IMAGES['player'][47]),
        getHitmask(IMAGES['player'][48]),
        getHitmask(IMAGES['player'][49]),
        getHitmask(IMAGES['player'][50]),
        getHitmask(IMAGES['player'][51]),

    )

    return IMAGES, SOUNDS, HITMASKS

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask
