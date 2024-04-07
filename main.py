import pygame
import asyncio
import random
from pacman import pacman
from ghost import ghost

pygame.init()

# screen width and height
WIDTH, HEIGHT = 600, 750
# 20x20 grid
GRID_WIDTH = 28
GRID_HEIGHT = 36
# cell size = 30
CELL_SIZE = WIDTH//GRID_WIDTH
# CELL_WIDTH_SIZE = WIDTH//GRID_WIDTH
# CELL_HEIGHT_SIZE = HEIGHT//GRID_HEIGHT
RADIUS = CELL_SIZE//2
COIN_SIZE = 6
ENERGIZER_SIZE = 10
FPS = 100
# has to be divisible with cell size (30 % 2 = 0)
SPEED = 1
BOOSTED_SPEED = 5
# for ghosts
SLOWED_SPEED = 2
# ghosts will be on scatter mode for 7 seconds
SCATTER = 7
# ghosts will be on chase mode for 20 seconds
CHASE = 20
# Whenever Pacman eats an energizer, he gets boosted speed for 12 seconds
BOOST_TIME = 12

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pacman')


clock = pygame.time.Clock()

# walls
# can produce array with walldrawing.py which can give list of boxes clicked
# Classic Pacman
walls = [(0, 35), (0, 34), (0, 33), (0, 32), (0, 31), (0, 30), (0, 29), (0, 28), (0, 27), (0, 26), (0, 25), (0, 24), (1, 35), (2, 35), (4, 35), (3, 35), (5, 35), (6, 35), (7, 35), (8, 35), (9, 35), (10, 35), (11, 35), (12, 35), (13, 35), (14, 35), (15, 35), (16, 35), (17, 35), (18, 35), (20, 35), (19, 35), (21, 35), (22, 35), (23, 35), (25, 35), (24, 35), (26, 35), (27, 35), (27, 34), (27, 33), (27, 29), (27, 30), (27, 32), (27, 31), (27, 28), (27, 27), (27, 26), (27, 25), (1, 24), (2, 24), (3, 24), (4, 24), (5, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24), (2, 33), (2, 32), (3, 32), (3, 33), (4, 33), (5, 33), (6, 33), (7, 33), (8, 33), (9, 33), (10, 33), (11, 33), (11, 32), (10, 32), (9, 32), (8, 32), (7, 32), (6, 32), (5, 32), (4, 32), (1, 30), (1, 29), (2, 30), (2, 29), (4, 30), (5, 30), (5, 29), (4, 29), (4, 28), (5, 28), (4, 27), (5, 27), (5, 26), (4, 26), (3, 26), (3, 27), (2, 27), (2, 26), (7, 26), (8, 26), (9, 26), (10, 26), (11, 26), (7, 27), (8, 27), (9, 27), (10, 27), (11, 27), (7, 29), (7, 30), (7, 31), (8, 31), (8, 30), (8, 29), (10, 30), (10, 29), (11, 29), (12, 29), (12, 30), (11, 30), (13, 29), (13, 30), (14, 31), (13, 31), (13, 32), (13, 33), (14, 33), (14, 32), (14, 30), (14, 29), (15, 29), (16, 29), (17, 29), (17, 30), (16, 30), (15, 30), (16, 33), (16, 32), (17, 32), (18, 32), (19, 32), (20, 32), (22, 32), (21, 32), (23, 32), (24, 32), (25, 32), (25, 33), (24, 33), (23, 33), (22, 33), (21, 33), (20, 33), (19, 33), (18, 33), (17, 33), (25, 29), (26, 29), (26, 30), (25, 30), (19, 31), (19, 30), (19, 29), (20, 29), (20, 30), (20, 31), (23, 30), (22, 30), (22, 29), (23, 29), (23, 28), (22, 28), (22, 27), (23, 27), (24, 27), (25, 27), (25, 26), (24, 26), (23, 26), (22, 26), (13, 27), (13, 26), (14, 26), (14, 27), (16, 27), (18, 27), (17, 27), (19, 27), (20, 27), (20, 26), (19, 26), (18, 26), (17, 26), (16, 26), (14, 25), (14, 24), (15, 24), (16, 24), (17, 24), (17, 23), (16, 23), (15, 23), (14, 23), (12, 23), (13, 23), (5, 23), (5, 22), (5, 21), (5, 20), (22, 23), (22, 22), (22, 21), (22, 20), (13, 24), (13, 25), (12, 24), (11, 24), (10, 24), (7, 23), (7, 24), (8, 24), (8, 23), (8, 22), (7, 22), (7, 21), (8, 21), (7, 20), (8, 20), (10, 23), (11, 23), (20, 24), (19, 24), (19, 23), (20, 23), (20, 22), (19, 22), (19, 20), (19, 21), (20, 21), (20, 20), (23, 20), (24, 20), (26, 20), (25, 20), (27, 20), (4, 20), (3, 20), (2, 20), (1, 20), (0, 20), (0, 18), (1, 18), (2, 18), (3, 18), (4, 18), (5, 18), (22, 18), (23, 18), (24, 18), (25, 18), (26, 18), (27, 18), (20, 18), (19, 18), (22, 17), (22, 16), (22, 15), (22, 14), (5, 17), (5, 16), (5, 15), (5, 14), (8, 18), (7, 18), (7, 16), (8, 16), (8, 17), (7, 17), (7, 15), (8, 15), (8, 14), (7, 14), (19, 17), (20, 17), (20, 16), (19, 16), (19, 15), (20, 15), (20, 14), (19, 14), (10, 21), (11, 21), (12, 21), (13, 21), (15, 21), (14, 21), (16, 21), (17, 21), (17, 19), (17, 20), (17, 18), (18, 15), (17, 15), (16, 15), (16, 14), (18, 14), (17, 14), (9, 15), (11, 15), (10, 15), (11, 14), (10, 14), (9, 14), (13, 15), (14, 15), (14, 14), (13, 14), (17, 17), (16, 17), (15, 17), (12, 17), (11, 17), (10, 17), (10, 18), (10, 19), (10, 20), (23, 14), (25, 14), (24, 14), (27, 14), (26, 14), (4, 14), (3, 14), (2, 14), (1, 14), (0, 14), (0, 13), (0, 12), (0, 11), (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (2, 5), (1, 5), (3, 5), (4, 5), (6, 5), (5, 5), (7, 5), (9, 5), (8, 5), (11, 5), (10, 5), (13, 5), (12, 5), (14, 5), (16, 5), (15, 5), (17, 5), (19, 5), (18, 5), (20, 5), (22, 5), (21, 5), (23, 5), (25, 5), (24, 5), (27, 5), (26, 5), (27, 6), (27, 7), (27, 8), (27, 10), (27, 9), (27, 11), (27, 12), (27, 13), (3, 12), (2, 12), (4, 12), (5, 12), (5, 11), (4, 11), (3, 11), (2, 11), (2, 9), (3, 9), (4, 9), (5, 9), (5, 8), (5, 7), (4, 7), (3, 7), (2, 7), (2, 8), (3, 8), (4, 8), (7, 11), (7, 13), (7, 12), (8, 11), (8, 13), (8, 12), (7, 9), (7, 8), (7, 7), (8, 8), (10, 7), (9, 7), (8, 7), (11, 7), (11, 8), (11, 9), (10, 9), (9, 9), (8, 9), (9, 8), (10, 8), (13, 6), (13, 7), (13, 8), (13, 9), (14, 8), (14, 9), (14, 7), (14, 6), (14, 11), (13, 11), (13, 12), (13, 13), (14, 13), (14, 12), (12, 11), (11, 11), (10, 11), (10, 12), (11, 12), (12, 12), (15, 12), (16, 12), (17, 12), (17, 11), (16, 11), (15, 11), (19, 12), (19, 11), (20, 11), (20, 12), (20, 13), (19, 13), (16, 7), (16, 8), (16, 9), (17, 9), (18, 9), (19, 9), (20, 9), (20, 8), (20, 7), (19, 7), (18, 7), (17, 7), (17, 8), (19, 8), (18, 8), (22, 11), (22, 12), (23, 12), (24, 12), (25, 12), (25, 11), (23, 11), (24, 11), (22, 7), (23, 9), (22, 9), (22, 8), (23, 8), (23, 7), (24, 7), (24, 8), (24, 9), (25, 9), (25, 8), (25, 7), (0, 5)]
PX, PY = 13, 7
gxy = [[11, 18], [13, 18], [14, 18], [15, 18]]
# ACM
# walls = [(3, 4), (2, 5), (1, 6), (1, 7), (1, 8), (2, 7), (3, 7), (4, 7), (4, 5), (5, 6), (5, 7), (5, 8), (7, 6), (7, 7), (8, 8), (9, 8), (8, 4), (9, 4), (7, 5), (10, 4), (10, 8), (13, 4), (13, 5), (13, 6), (13, 8), (13, 7), (17, 4), (18, 4), (18, 5), (14, 4), (15, 5), (16, 5), (18, 6), (18, 7), (18, 8)]
# Penis
# walls = [(7, 4), (8, 3), (11, 4), (10, 3), (12, 5), (11, 6), (11, 7), (6, 5), (7, 6), (7, 7), (7, 9), (7, 8), (7, 10), (11, 8), (11, 9), (11, 10), (12, 6), (6, 6), (7, 11), (7, 12), (7, 13), (11, 11), (11, 13), (11, 12), (11, 14), (7, 14), (7, 15), (11, 15), (6, 16), (5, 15), (2, 15), (2, 16), (2, 17), (5, 18), (6, 18), (3, 14), (4, 14), (2, 14), (7, 18), (3, 18), (4, 18), (8, 18), (9, 18), (11, 18), (10, 18), (12, 18), (13, 18), (12, 16), (13, 15), (14, 14), (15, 14), (16, 14), (16, 15), (16, 16), (16, 17), (15, 18), (14, 18)]
# small
# walls = [(0, 2), (0, 3), (0, 4), (0, 6), (0, 5), (0, 7), (0, 8), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (9, 8), (9, 6), (9, 7), (9, 5), (9, 3), (9, 4), (9, 2), (9, 1), (9, 0), (8, 0), (7, 0), (6, 0), (4, 0), (5, 0), (2, 0), (3, 0), (1, 0), (0, 0), (0, 1), (2, 2), (2, 3), (2, 4), (7, 2), (7, 3), (7, 4), (4, 3), (5, 3), (5, 6), (4, 6), (3, 6), (6, 6), (2, 7), (2, 6), (7, 6), (7, 7)]

# PX, PY = 1, 1
pacman = pacman(PX, PY, SPEED, RADIUS, screen, walls, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT)
# gxy = [[8, 8], [5, 5], [2, 8], [7, 5]]
ghosts = []
ghosts.append(ghost(gxy[0][0], gxy[0][1], SPEED, RADIUS, walls, gxy, screen, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT))
ghosts.append(ghost(gxy[1][0], gxy[1][1], SPEED, RADIUS, walls, gxy, screen, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT))
ghosts.append(ghost(gxy[2][0], gxy[2][1], SPEED, RADIUS, walls, gxy, screen, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT))
ghosts.append(ghost(gxy[3][0], gxy[3][1], SPEED, RADIUS, walls, gxy, screen, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT))

coins = []
coin_img = pygame.image.load("coin-1.png.png")
coin_img = pygame.transform.scale(coin_img, (CELL_SIZE//2, CELL_SIZE//2))
noofcoins = 0
for i in range(GRID_HEIGHT):
    for j in range(GRID_WIDTH):
        if [j, i] == [PX, PY]:
            continue
        if [j, i] in gxy:
            continue
        if (j, i) in walls:
            continue
        coins.append([j, i])
        noofcoins += 1

score = 0
boosted = False
boost_time = 0
scatter_time = SCATTER
chase_time = CHASE

# energizers = [[]]
# for [x, y] in energizers:
#     coins.remove([x, y])
#     noofcoins -= 1


def check_food():
    global score, noofcoins
    if [pacman.x, pacman.y] in coins:
        coins.remove([pacman.x, pacman.y])
        score += 10
        noofcoins -= 1
    # elif [pacman.x, pacman.y] in energizers:
    #     energizers.remove([pacman.x, pacman.y])
    #     boost()


def check_dead():
    for ghost in ghosts:
        if (pacman.x == ghost.x) and (pacman.y == ghost.y):
            return True
    return False


def boost():
    global boost_time, boosted
    boosted = True
    pacman.speed = BOOSTED_SPEED
    for ghost in ghosts:
        ghost.mode = 'frightened'
        ghost.speed = SLOWED_SPEED
    # boost time = 20 secs
    boost_time = BOOST_TIME*FPS


def unboost():
    global boost_time, boosted
    boosted = False
    pacman.speed = SPEED
    for ghost in ghosts:
        ghost.mode = 'scatter'
        ghost.speed = SPEED
    boost_time = 0


async def main():

    not_dead = True
    while not_dead:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                not_dead = False
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP) or (event.key == pygame.K_w):
                    pacman.up()
                elif (event.key == pygame.K_DOWN) or (event.key == pygame.K_s):
                    pacman.down()
                elif (event.key == pygame.K_LEFT) or (event.key == pygame.K_a):
                    pacman.left()
                elif (event.key == pygame.K_RIGHT) or (event.key == pygame.K_d):
                    pacman.right()

        # grid
        screen.fill(BLACK)
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                pygame.draw.rect(screen, BLUE, (i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

        # walls
        for (i, j) in walls:
            pygame.draw.rect(screen, BLUE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for [x, y] in coins:
            cx = (x * CELL_SIZE) + ((CELL_SIZE // 2) - (COIN_SIZE // 2))
            cy = (y * CELL_SIZE) + ((CELL_SIZE // 2) - (COIN_SIZE // 2))
            # pygame.draw.rect(screen, WHITE, (cx, cy, COIN_SIZE, COIN_SIZE))
            screen.blit(coin_img, (cx, cy))

        # for [x, y] in energizers:
        #     cx = (x * CELL_SIZE) + ((CELL_SIZE // 2) - (ENERGIZER_SIZE // 2))
        #     cy = (y * CELL_SIZE) + ((CELL_SIZE // 2) - (ENERGIZER_SIZE // 2))
        #     pygame.draw.rect(screen, WHITE, (cx, cy, ENERGIZER_SIZE, ENERGIZER_SIZE))

        pacman.update()
        for i in range(len(ghosts)):
            ghosts[i].chase(pacman)
            ghosts[i].update()
            gxy[i] = [ghosts[i].x, ghosts[i].y]
        # print('pacman x', pacman.x)
        # print('pacman y', pacman.y)

        if boosted:
            global boost_time
            boost_time -= 1
            if boost_time == 0:
                unboost()

        check_food()
        if noofcoins == 0:
            not_dead = False

        if not boosted:
            if check_dead():
                not_dead = False

        pygame.display.update()
        await asyncio.sleep(0)

    print('game over')
    print('score: ', score)
    pygame.quit()

asyncio.run(main())
