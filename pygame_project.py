import os
import sys
import time

import pygame
from random import choice, randint

FPS = 20
WIDTH, HEIGHT = 600, 620
BLOCK, CUP_H, CUP_W = 25, 20, 10
FIGURE_W, FIGURE_H = 5, 5

COLORS = {'S': 'red',
          'Z': 'orange',
          'J': 'yellow',
          'L': 'green',
          'I': 'blue',
          'O': 'dark_blue',
          'T': 'violet'
          }

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
    pygame.mixer.quit()
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
    intro_text = ["ТЕТРИС ДЛЯ ЧАЙНИКОВ", "",
                  "Инструкция",
                  "В этой игре фигуры движутся вниз самостоятельно",
                  "Стрелкой влево/кнопкой A фигурки двигаются влево",
                  "Стрелкой вправо/кнопкой D фигурки двигаются в право",
                  "Стрелкой вниз/кнопкой S фигурки двигаются быстрее",
                  "Стрелкой вверх/кнопкой W фигурки вращаются", "",
                  "Нажмите на любую кнопку для начала"]

    fon = pygame.transform.scale(load_image('fon1.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 29)
    text_coord = 50
    pygame.draw.rect(screen, pygame.Color(45, 45, 45), (12, 55, 576, 310))
    pygame.draw.rect(screen, pygame.Color(90, 90, 90), (12, 55, 576, 310), 3)
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(225, 225, 225))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        text_rect = string_rendered.get_rect(center=(WIDTH / 2, text_coord))
        screen.blit(string_rendered, text_rect)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                terminate()
            elif ev.type == pygame.KEYDOWN or \
                    ev.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, color='empty'):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[color]
        self.rect = self.image.get_rect().move(
            50 + BLOCK * pos_x, 50 + BLOCK * pos_y)


class FallenBlock(pygame.sprite.Sprite):
    def __init__(self, block_x, block_y, color):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[color]
        self.rect = self.image.get_rect().move(
            50 + BLOCK * block_x, 50 + BLOCK * block_y)


class Figure:
    def __init__(self, shape, color, position):
        self.shape, self.color, self.position = shape, color, position
        self.x, self.y = int(CUP_W / 2) - int(FIGURE_W / 2), -2


def generate_level(lev):
    x1, y2 = None, None
    for i in range(len(lev)):
        for j in range(len(lev[i])):
            if lev[i][j] == 'o':
                Block(i, j, 'empty')
            elif lev[i][j][1] == 'b':
                Block(i, j, lev[i][j][0])
            elif lev[i][j][1] == 'f':
                FallenBlock(i, j, lev[i][j][0])
    return x1, y2


def create_figure():
    shape = choice(list(figures.keys()))
    color = COLORS[shape]
    if shape == 'I':
        position = 1
    else:
        position = 0
    fig = Figure(shape, color, position)
    return fig


def add_to_cup(fig):
    for i in range(FIGURE_W):
        for j in range(FIGURE_H):
            if figures[fig.shape][fig.position][j][i] != 'o':
                cup[i + fig.x][j + fig.y] = (fig.color, 'f')


def figure_falling(fig):
    for i in range(FIGURE_W):
        for j in range(FIGURE_H):
            if figures[fig.shape][fig.position][j][i] != 'o':
                Block(i + fig.x, j + fig.y, fig.color)


def figure_in_cup(fig_x, fig_y):
    return 0 <= fig_x < CUP_W and fig_y < CUP_H


def move_is_possible(fig, poss_x=0, poss_y=0):
    for i in range(FIGURE_W):
        for j in range(FIGURE_H):
            if figures[fig.shape][fig.position][j][i] == 'o' or j + fig.y + poss_y < 0:
                continue
            if not figure_in_cup(i + fig.x + poss_x, j + fig.y + poss_y):
                return False
            if cup[i + fig.x + poss_x][j + fig.y + poss_y] != 'o':
                return False
    return True


def layer_check(layer):
    for w in range(CUP_W):
        if cup[w][layer] == 'o':
            return False
    return True


def remove_layers():
    global score, points
    removed_layers = 0
    layer = CUP_H - 1
    while layer >= 0:
        if layer_check(layer):
            for y1 in range(layer, 0, -1):
                for x1 in range(CUP_W):
                    cup[x1][y1] = cup[x1][y1 - 1]
            for x2 in range(CUP_W):
                cup[x2][0] = 'o'
            removed_layers += 1
        else:
            layer -= 1
    points += removed_layers
    if removed_layers == 1:
        score += 40 * (points + 1)
    elif removed_layers == 2:
        score += 100 * (points + 1)
    elif removed_layers == 3:
        score += 300 * (points + 1)
    elif removed_layers == 4:
        score += 1200 * (points + 1)


def draw_score(sc):
    font = pygame.font.Font(None, 45)
    tit_score = font.render("score:", True, pygame.Color(54, 156, 78))
    text_x = 390
    text_y = 480
    screen.blit(tit_score, (text_x, text_y))
    f = pygame.font.Font(None, 37)
    pygame.draw.rect(screen, 'black', (390, 515, 120, 40))
    pygame.draw.rect(screen, pygame.Color(180, 180, 180), (390, 515, 120, 40), 3)
    string = f.render(str(sc), 1, pygame.Color(225, 225, 225))
    rect = string.get_rect()
    rect.x = 395
    rect.y = 100
    rect.topright = (503, 525)
    screen.blit(string, rect)


def draw_name():
    font = pygame.font.Font(None, 75)
    tit_score = font.render("TETRIS", True, pygame.Color(237, 118, 14))
    text_x = 360
    text_y = 20
    screen.blit(tit_score, (text_x, text_y))


def record(rec="0"):
    font = pygame.font.Font(None, 45)
    tit_rec = font.render("record:", True, pygame.Color(54, 156, 78))
    text_x = 390
    text_y = 400
    screen.blit(tit_rec, (text_x, text_y))
    f = pygame.font.Font(None, 37)
    pygame.draw.rect(screen, 'black', (390, 435, 120, 40))
    pygame.draw.rect(screen, pygame.Color(180, 180, 180), (390, 435, 120, 40), 3)
    string = f.render(rec, 1, pygame.Color(225, 225, 125))
    rect = string.get_rect()
    rect.x = 395
    rect.y = 100
    rect.topright = (503, 445)
    screen.blit(string, rect)

def get_record():
    try:
        with open("record") as f:
            return f.readlines()
    except FileNotFoundError:
        with open("record", "w") as f:
            f.write("0")
    return 0

def set_record(rec, score):
    r = max(int(rec), score)
    with open("record", "w") as f:
        f.write(str(r))


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(0.7)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mixer.music.load('data/tetris.mp3')
pygame.display.set_caption('Тетрис')
clock = pygame.time.Clock()
start_screen()
# background = pygame.image.load("data/fon_fon.jpg")
# background = pygame.transform.scale(background, (width, height))


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()

tile_images = {
    'empty': load_image('blacksquare.png'),
    'red': load_image('red_square.png'),
    'blue': load_image('blue_square.png'),
    'green': load_image('green_square.png'),
    'yellow': load_image('yellow_square.png'),
    'orange': load_image('orange_square.png'),
    'violet': load_image('violet_square.png'),
    'dark_blue': load_image('dark_blue_square.png')
}

while True:
    rec = "".join(get_record())
    pygame.mixer.music.play(loops=-1)
    cup = [['o'] * CUP_H for _ in range(CUP_W)]
    x, y = generate_level(cup)
    # screen.blit(background, (0, 0))
    all_sprites.draw(screen)

    col = randint(0, 3)
    figure = create_figure()
    last_down = time.time()
    last_left_right = time.time()
    fall = time.time()
    score = 0
    points = 0
    playing = True
    move_right = False
    move_left = False
    move_down = False

    level, fall_speed = 1, 0.25

    while playing:
        if not figure:
            col = randint(0, 3)
            figure = create_figure()
            fall = time.time()
            if not move_is_possible(figure):
                set_record(rec, score)
                playing = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    figure.position = (figure.position + 1) % len(figures[figure.shape])
                    if not move_is_possible(figure):
                        figure.position = (figure.position - 1) % len(figures[figure.shape])
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s)and move_is_possible(figure, poss_y=1):
                    move_down = True
                    move_right = False
                    move_left = False
                    figure.y += 1
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d)and move_is_possible(figure, poss_x=1):
                    move_right = True
                    move_left = False
                    move_down = False
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and move_is_possible(figure, poss_x=-1):
                    move_right = False
                    move_left = True
                    move_down = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    ...
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    move_left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    move_right = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    move_down = False

        if move_down and time.time() - last_down > 0.05 and move_is_possible(figure, poss_y=1):
            figure.y += 1
            last_down = time.time()

        elif (move_left or move_right) and time.time() - last_left_right > 0.12:
            if move_left and move_is_possible(figure, poss_x=-1):
                figure.x -= 1
            elif move_right and move_is_possible(figure, poss_x=1):
                figure.x += 1
            last_left_right = time.time()

        if time.time() - fall > fall_speed:
            if not move_is_possible(figure, poss_y=1):
                add_to_cup(figure)
                remove_layers()
                figure = None
            else:
                figure.y += 1
                fall = time.time()
        screen.fill(pygame.Color(80, 80, 80))
        for i in all_sprites:
            i.kill()
        generate_level(cup)
        if not figure is None:
            if figure.y > -2:
                figure_falling(figure)
        pygame.draw.rect(screen, 'black', (50, 50, BLOCK * CUP_W + 6, BLOCK * CUP_H + 6))
        tiles_group.draw(screen)
        pygame.draw.rect(screen, pygame.Color(180, 180, 180), (50, 50, BLOCK * CUP_W + 6, BLOCK * CUP_H + 6), 3)
        draw_score(score)
        record(rec)
        draw_name()
        #record()
        pygame.display.flip()
