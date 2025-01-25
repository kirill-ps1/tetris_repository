import os
import sys
from operator import index

import pygame
from pygame import time
from random import randint

FPS = 20
WIDTH, HEIGHT = 500, 620

figures = [['.##..',
            '..##.',],
           ['..##.',
            '.##..'],
           ['.###.',
            '.#...'],
           ['.###.',
            '...#.'],
           ['.###.',
            '..#..'],
           ['####.',
            '.....'],
           ['.##..',
            '.##..']]

board = ['..........', '..........', '..........', '..........', '..........',
         '..........', '..........', '..........', '..........', '..........',
         '..........', '..........', '..........', '..........', '..........',
         '..........', '..........', '..........', '..........', '..........']

falling = False


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

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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


class BoardBlock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images['empty']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 10)


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['block']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 10, tile_height * pos_y + 10)
        self.timer = time.get_ticks()

    def update(self):
        if (a := time.get_ticks()) - self.timer / 1000 == int(a / 1000):
            ...


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                BoardBlock(x, y)
            elif level[y][x] == '#':
                Block(x, y)
    return new_player, x, y


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Тетрис')
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_images = {
    'empty': load_image('square.png'),
    'block': load_image('square1.png')
}
level = board
tile_width = tile_height = 30

player, level_x, level_y = generate_level(level)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    if not falling:
        board[0] = '.' * (b := randint(0, 5)) + figures[(c := randint(0, 6))][0] + '.' * (10 - b - 5)
        board[1] = '.' * b + figures[c][1] + '.' * (10 - b - 5)
        for i in all_sprites:
            i.kill()
        player, level_x, level_y = generate_level(board)
        print(len(board))
        falling = True
    screen.fill('white')
    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.draw.rect(screen, 'gray', (7, 7, 306, 606), 2, 4)
    pygame.display.flip()
    clock.tick(FPS)
