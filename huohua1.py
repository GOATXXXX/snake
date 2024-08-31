import pygame
import random
import sys
import time
from collections import deque
from pygame.locals import *

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
SIZE = 20
LINE_WIDTH = 1

SCOPE_X = (0, SCREEN_WIDTH // SIZE - 1)
SCOPE_Y = (2, SCREEN_HEIGHT // SIZE - 1)

FOOD_STYLE_LIST = [(10, (255, 100, 100)), (20, (100, 255, 100)), (30, (100, 100, 255))]

LIGHT = (100, 100, 100)
DARK = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (200, 30, 30)
BGCOLOR = (40, 40, 60)
WEATHER = {'雨': (0.5, (128, 128, 255)), '晴': (0.8, (150, 150, 150)), '雷暴': (1.2, (255, 255, 0))}


class Spark(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # 火花的图片，可以根据需要修改或添加更多状态的图片
        self.images = [pygame.image.load('huohua.png')]

        self.image = self.images[0]
         # 缩小图片到原来的一半
        # 获取图片大小
        image_width, image_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (image_width // 1, image_height // 1))

        self.rect = self.image.get_rect()
        self.rect.center = pos

        # 火花的生命周期，以帧为单位
        self.lifetime = 120

    def update(self):
        # 火花效果的动画
        self.lifetime -= 3
        if self.lifetime < 0:
            self.kill()
        else:
            # 更换图片来实现动画效果
            frame = int((len(self.images) - 1) * (30 - self.lifetime) / 30)
            self.image = self.images[frame]

def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))

def init_snake():
    snake = deque()
    snake.append((2, SCOPE_Y[0]))
    snake.append((1, SCOPE_Y[0]))
    snake.append((0, SCOPE_Y[0]))
    return snake

def create_food(snake, sparks):
    food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
    food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    while (food_x, food_y) in snake:
        food_x = random.randint(SCOPE_X[0], SCOPE_X[1])
        food_y = random.randint(SCOPE_Y[0], SCOPE_Y[1])
    
    # 计算页面中心点坐标
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # 创建火花效果，并将其放在页面中间
    # 添加条件判断，如果食物不是首次创建，则添加火花效果
    if not (snake == init_snake() and len(sparks) == 0):
        spark = Spark((center_x, center_y))
        sparks.add(spark)

    return food_x, food_y

def get_food_style():
    return FOOD_STYLE_LIST[random.randint(0, 2)]

def start(orispeed):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('贪吃蛇')

    font1 = pygame.font.SysFont('SimHei', 24)
    font2 = pygame.font.Font(None, 72)
    fwidth, fheight = font2.size('GAME OVER')

    # 随机选择一种天气状态
    weather = random.choice(list(WEATHER.keys()))

    # 防止方向键冲突的变量
    b = True

    # 创建一个精灵组来管理火花效果
    sparks = pygame.sprite.Group()

    snake = init_snake()
    food = create_food(snake, sparks)
    food_style = get_food_style()
    pos = (1, 0)

    game_over = True
    start = False
    score = 0
    # orispeed = 0.3
    speed = orispeed
    last_move_time = None
    pause = False
    
    weather_timer = 5
    weather_change_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    if game_over:
                        start = True
                        game_over = False
                        b = True
                        snake = init_snake()
                        food = create_food(snake, sparks)
                        food_style = get_food_style()
                        pos = (1, 0)
                        # 得分
                        score = 0
                        last_move_time = time.time()

                elif event.key == K_SPACE:
                    if not game_over:
                        pause = not pause

                elif event.key in (K_w, K_UP):
                    if b and not pos[1]:
                        pos = (0, -1)
                        b = False

                elif event.key in (K_s, K_DOWN):
                    if b and not pos[1]:
                        pos = (0, 1)
                        b = False

                elif event.key in (K_a, K_LEFT):
                    if b and not pos[0]:
                        pos = (-1, 0)
                        b = False

                elif event.key in (K_d, K_RIGHT):
                    if b and not pos[0]:
                        pos = (1, 0)
                        b = False

        screen.fill(BGCOLOR)

        for x in range(SIZE, SCREEN_WIDTH, SIZE):
            pygame.draw.line(screen, BLACK, (x, SCOPE_Y[0] * SIZE), (x, SCREEN_HEIGHT), LINE_WIDTH)

        for y in range(SCOPE_Y[0] * SIZE, SCREEN_HEIGHT, SIZE):
            pygame.draw.line(screen, BLACK, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)

        if not game_over:
            curTime = time.time()
            if curTime - last_move_time > speed:
                if not pause:
                    b = True
                    last_move_time = curTime
                    next_s = (snake[0][0] + pos[0], snake[0][1] + pos[1])
                    if next_s == food:
                        snake.appendleft(next_s)
                        score += food_style[0]
                        speed = orispeed - 0.03 * (score // 100)
                        food = create_food(snake, sparks)
                        food_style = get_food_style()
                    else:
                        if SCOPE_X[0] <= next_s[0] <= SCOPE_X[1] and SCOPE_Y[0] <= next_s[1] <= SCOPE_Y[1] and next_s not in snake:  
                            snake.appendleft(next_s)  
                            # 根据当前天气状态改变蛇的移动速度  
                            # 晴天
                            if weather == '晴':  
                                speed = orispeed 
                            # 雨  
                            elif weather == '雨':  
                                speed = orispeed * 0.5  
                            # 雷暴  
                            elif weather == '雷暴':  
                                speed = orispeed * 0.25  
                            snake.pop()  
                        else:  
                            game_over = True

        if not game_over:
            pygame.draw.rect(screen, food_style[1], (food[0] * SIZE, food[1] * SIZE, SIZE, SIZE), 0)

        for s in snake:
            pygame.draw.rect(screen, DARK, (s[0] * SIZE + LINE_WIDTH, s[1] * SIZE + LINE_WIDTH,
                                            SIZE - LINE_WIDTH * 2, SIZE - LINE_WIDTH * 2), 0)

        print_text(screen, font1, 30, 7, f'速度: {score // 100}')
        print_text(screen, font1, 150, 7, f'天气: {weather}')
        print_text(screen, font1, 450, 7, f'得分: {score}')

        if game_over:
            if start:
                print_text(screen, font2, (SCREEN_WIDTH - fwidth) // 2, (SCREEN_HEIGHT - fheight) // 2, 'GAME OVER',
                           RED)

        # 检查是否需要更新天气
        if time.time() - weather_change_time > weather_timer:
            weather = random.choice(list(WEATHER.keys()))
            weather_change_time = time.time()
            
        # 更新和绘制火花效果
        sparks.update()
        sparks.draw(screen)

        pygame.display.update()