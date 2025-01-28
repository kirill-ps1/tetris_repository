import os
import sys
import time

import pygame
from random import randint, choice

from PyQt6.QtBluetooth import QBluetoothLocalDevice

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
    intro_text = ["Тетрис", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('Screenshot_1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('Gray'))
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
    def __init__(self, block_x, block_y, color='empty'):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[color]
        self.rect = self.image.get_rect().move(
            10 + BLOCK * block_x, 10 + BLOCK * block_y)


def generate_level(lev):
    x, y = None, None
    for y in range(len(lev)):
        for x in range(len(lev[y])):
            if lev[y][x] == 'b':
                Block(x, y)
            elif lev[y][x] == 'f':
                FallenBlock(x, y)
    return x, y


def createFigure():
    figure = {'color': choice(COLORS),
              'shape': (shape := choice(list(figures.keys()))),
              'position': choice(figures[shape]),
              'x': int(CUP_W / 2) - int(FIGURE_W / 2),
              'y': -2}
    return figure


def addToCup(cup_, fig):
    for x in range(FIGURE_W):
        for y in range(FIGURE_H):
            if figures[fig['shape']][fig['rotation']][y][x] != 'o':
                cup_[x + fig['x']][y + fig['y']] = fig['color']


def speed_(p):
    lev = int(p / 10) + 1
    speed = 0.27 - (lev * 0.02)
    return level, speed


def figureInCup(fig_x, fig_y):
    return 0 <= fig_x < CUP_W and fig_y < CUP_H


def moveIsPossible(f, poss_x=0, poss_y=0):
    for i in range(FIGURE_W):
        for j in range(FIGURE_H):
            if figures[f['shape']][f['position']] or j + f['y'] + poss_y < 0:
                continue
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
    'blue': load_image('green_square.png'),
    'green': load_image('green_square.png')
}

playing = True
figure = createFigure()
move_right = False
move_left = False
points = 0
level, fall_speed = speed_(points)
fall = time.time()
cup = [['o'] * CUP_H for _ in range(CUP_W)]

while playing:
    if not figure:
        figure = createFigure()

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                ...
    if fall - time.time() > fall_speed:
        if ...:
            ...
