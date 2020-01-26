import pgzrun
from pgzero import screen

WIDTH = 300
HEIGHT = 600


def draw():
    screen.clear()
    startpos = (150, 20)
    endpos = (250, 120)
    screen.draw.line(startpos, endpos, 'BLUE')


pgzrun.go()

# %%
import pgzrun

WIDTH = 800
HEIGHT = 600


def draw():
    screen.clear()
    screen.draw.circle((400, 300), 30, 'white')


pgzrun.go()

# %%
# 参考　http://aidiary.hatenablog.com/entry/20080505/1275695237
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (640, 480)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"図形の描画")

while True:
    screen.fill((0, 0, 0))

    # 図形を描画
    # 黄の矩形
    pygame.draw.rect(screen, (255, 255, 0), Rect(10, 10, 300, 200))
    # 赤の円
    pygame.draw.circle(screen, (255, 0, 0), (320, 240), 100)
    # 紫の楕円
    pygame.draw.ellipse(screen, (255, 0, 255), (400, 300, 200, 100))
    # 白い線
    pygame.draw.line(screen, (255, 255, 255), (0, 0), (640, 480))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
