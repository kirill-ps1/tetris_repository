import os
import sys
import time

import pygame
from random import choice, randint

FPS = 20
WIDTH, HEIGHT = 600, 620
BLOCK, CUP_H, CUP_W = 30, 20, 10
FIGURE_W, FIGURE_H = 5, 5

COLORS = ['red', 'blue', 'green', 'yellow']

figures = {'S': [['ooooo', 'ooooo', 'ooxxo', 'oxxoo', 'ooooo'],
                 ['ooooo', 'ooxoo', 'ooxxo', 'oooxo', 'ooooo']],
           'Z': [['ooooo', 'ooooo', 'oxxoo', 'ooxxo', 'ooooo'],
                 ['ooooo', 'ooxoo', 'oxxoo', 'oxooo', 'ooooo']],
           'J': [['ooooo', 'oxooo', 'oxxxo', 'ooooo', 'ooooo'],
                 ['ooooo', 'ooxxo', 'ooxoo', 'ooxoo', 'ooooo'],
                 ['ooooo', 'ooooo', 'oxxxo', 'oooxo', 'ooooo'],
                 ['ooooo', 'ooxoo', 'ooxoo', 'oxxoo', 'ooooo']],
           'L': [['ooooo', 'oooxo', 'oxxxo', 'ooooo', 'ooooo'],
                 ['ooooo', 'ooxoo', 'ooxoo', 'ooxxo', 'ooooo'],
                 ['ooooo', 'ooooo', 'oxxxo', 'oxooo', 'ooooo'],
                 ['ooooo', 'oxxoo', 'ooxoo', 'ooxoo', 'ooooo']],
           'I': [['ooxoo', 'ooxoo', 'ooxoo', 'ooxoo', 'ooooo'],
                 ['ooooo', 'ooooo', 'xxxxo', 'ooooo', 'ooooo']],
           'O': [['ooooo', 'ooooo', 'oxxoo', 'oxxoo', 'ooooo']],
           'T': [['ooooo', 'ooxoo', 'oxxxo', 'ooooo', 'ooooo'],
                 ['ooooo', 'ooxoo', 'ooxxo', 'ooxoo', 'ooooo'],
                 ['ooooo', 'ooooo', 'oxxxo', 'ooxoo', 'ooooo'],
                 ['ooooo', 'ooxoo', 'oxxoo', 'ooxoo', 'ooooo']]}

num = [i for i in range(1, 22)]
falling = None


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["                     ТЕТРИС ДЛЯ ЧАЙНИКОВ", "",
                  "                            Правила игры",
                  "В этой игре фигуры движутся вниз самостоятельно",
                  "стрелочками влево и вправо можно двигать фигурки",
                  "При нажатии стрелочки вниз, фигурки движутся быстрее",
                  "                            Желаем удачи!"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(175, 65, 68))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color='empty'):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[color]
        self.rect = self.image.get_rect().move(
            10 + BLOCK * pos_x, 10 + BLOCK * pos_y)


class FallenBlock(pygame.sprite.Sprite):
    def __init__(self, block_x, block_y, color):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[color]
        self.rect = self.image.get_rect().move(
            10 + BLOCK * block_x, 10 + BLOCK * block_y)


def generate_level(lev):
    x, y = None, None
    for y in range(len(lev)):
        for x in range(len(lev[y])):
            if lev[y][x] == 'o':
                Block(y, x, 'empty')
            elif lev[y][x][1] == 'b':
                Block(y, x, lev[y][x][0])
            elif lev[y][x][1] == 'f':
                FallenBlock(y, x, lev[y][x][0])
    return x, y


def createFigure(color):
    fig = {'color': color,
           'shape': (shape := choice(list(figures.keys()))),
           'position': randint(0, len(figures[shape]) - 1),
           'x': int(CUP_W / 2) - int(FIGURE_W / 2),
           'y': -2}
    return fig


def addToCup(fig):
    for i in range(FIGURE_W):
        for j in range(FIGURE_H):
            if figures[fig['shape']][fig['position']][j][i] != 'o':
                cup[i + fig['x']][j + fig['y']] = (fig['color'], 'f')


def figureFalling(fig):
    for i in range(FIGURE_W):
        for j in range(FIGURE_H):
            if figures[fig['shape']][fig['position']][j][i] != 'o':
                Block(i + fig['x'], j + fig['y'], fig['color'])


def speed_(p):
    lev = int(p / 10) + 1
    speed = 0.27 - (lev * 0.02)
    return level, speed


def figureInCup(fig_x, fig_y):
    return 0 <= fig_x < CUP_W and fig_y < CUP_H


def moveIsPossible(f, poss_x=0, poss_y=0):
    for i in range(FIGURE_W):
        for j in range(FIGURE_H):
            if figures[f['shape']][f['position']][j][i] == 'o' or j + f['y'] + poss_y < 0:
                continue
            if not figureInCup(i + f['x'] + poss_x, j + f['y'] + poss_y):
                return False
            if cup[i + f['x'] + poss_x][j + f['y'] + poss_y] != 'o':
                return False
    return True


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Тетрис')
clock = pygame.time.Clock()
start_screen()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

tile_images = {
    'empty': load_image('empty_square.png'),
    'red': load_image('red_square.png'),
    'blue': load_image('blue_square.png'),
    'green': load_image('green_square.png'),
    'yellow': load_image('yellow_square.png')
}
cup = [['o'] * CUP_H for _ in range(CUP_W)]
x, y = generate_level(cup)

col = randint(0, 3)
figure = createFigure(COLORS[col])
last_side = time.time()
fall = time.time()
playing = True
move_right = False
move_left = False
points = 0
level, fall_speed = 1, 0.25

while playing:
    if not figure:
        col = randint(0, 3)
        figure = createFigure(COLORS[col])
        fall = time.time()
        if not moveIsPossible(figure):
            playing = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and moveIsPossible(figure, poss_x=-1):
                figure['x'] -= 1
                move_right = False
                move_left = True
            if event.key == pygame.K_RIGHT and moveIsPossible(figure, poss_x=1):
                move_right = True
                move_left = False
                figure['x'] += 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                ...
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    if move_right or move_left:
        ...
    if time.time() - fall > fall_speed:
        if not moveIsPossible(figure, poss_y=1):
            addToCup(figure)
            figure = None
        else:
            figure['y'] += 1
            fall = time.time()
    screen.fill('white')
    for i in all_sprites:
        i.kill()
    generate_level(cup)
    if not figure is None:
        figureFalling(figure)
    tiles_group.draw(screen)
    pygame.display.flip()
