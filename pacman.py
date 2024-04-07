import pygame

YELLOW = (255, 255, 0)


class pacman:
    def __init__(self, x, y, speed, radius, screen, walls, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT):
        self.x = x
        self.y = y
        self.xdir = 0
        self.ydir = 0
        self.speed = speed
        self.radius = radius
        self.screen = screen
        self.walls = walls
        self.cell_size = CELL_SIZE
        self.gw = GRID_WIDTH
        self.gh = GRID_HEIGHT
        self.cx = (self.x * CELL_SIZE) + radius
        self.cy = (self.y * CELL_SIZE) + radius
        self.txdir = 0
        self.tydir = 0
        self.img = pygame.image.load("pirate/Copy of pirate-nosword-moving-1.png.png")
        self.img = pygame.transform.scale(self.img, (CELL_SIZE*3, CELL_SIZE*3))

        self.inmotion = False

    def update(self):
        if self.inmotion:
            self.cx += self.txdir*self.speed
            self.cy += self.tydir*self.speed
            # pygame.draw.circle(self.screen, YELLOW, (self.cx, self.cy), self.radius)
            self.screen.blit(self.img, (self.cx - self.cell_size, self.cy - self.cell_size))
            # checking if motion from one square to other is over
            if (self.cx == ((self.x + self.txdir)*self.cell_size) + self.radius) and (self.cy == ((self.y + self.tydir)*self.cell_size) + self.radius):
                self.x += self.txdir
                self.y += self.tydir
                # wrapping around grid edges
                self.x %= self.gw
                self.y %= self.gh
                self.cx = (self.x * self.cell_size) + self.radius
                self.cy = (self.y * self.cell_size) + self.radius
                if (self.xdir != 0) or (self.ydir != 0):
                    if (self.x + self.xdir, self.y + self.ydir) in self.walls:
                        self.xdir = 0
                        self.ydir = 0
                        self.inmotion = False
                    else:
                        self.txdir = self.xdir
                        self.tydir = self.ydir
                else:
                    self.inmotion = False
        else:
            # pygame.draw.circle(self.screen, YELLOW, (self.cx, self.cy), self.radius)
            self.screen.blit(self.img, (self.cx - self.cell_size, self.cy - self.cell_size))

    def up(self):
        if (self.x, self.y - 1) in self.walls:
            if self.inmotion:
                if (self.x + self.txdir, self.y + self.tydir -1) not in self.walls:
                    self.xdir = 0
                    self.ydir = -1
                else:
                    self.xdir = 0
                    self.ydir = 0
            else:
                self.xdir = 0
                self.ydir = 0
        else:
            self.xdir = 0
            self.ydir = -1
            if not self.inmotion:
                self.txdir = self.xdir
                self.tydir = self.ydir
                self.inmotion = True

    def down(self):
        if (self.x, self.y + 1) in self.walls:
            if self.inmotion:
                if (self.x + self.txdir, self.y + self.tydir + 1) not in self.walls:
                    self.xdir = 0
                    self.ydir = 1
                else:
                    self.xdir = 0
                    self.ydir = 0
            else:
                self.xdir = 0
                self.ydir = 0
        else:
            self.xdir = 0
            self.ydir = 1
            if not self.inmotion:
                self.txdir = self.xdir
                self.tydir = self.ydir
                self.inmotion = True

    def left(self):
        if (self.x - 1, self.y) in self.walls:
            if self.inmotion:
                if (self.x + self.txdir - 1, self.y + self.tydir) not in self.walls:
                    self.xdir = -1
                    self.ydir = 0
                else:
                    self.xdir = 0
                    self.ydir = 0
            else:
                self.xdir = 0
                self.ydir = 0
        else:
            self.xdir = -1
            self.ydir = 0
            if not self.inmotion:
                self.txdir = self.xdir
                self.tydir = self.ydir
                self.inmotion = True

    def right(self):
        if (self.x + 1, self.y) in self.walls:
            if self.inmotion:
                if (self.x + self.txdir + 1, self.y + self.tydir) not in self.walls:
                    self.xdir = 1
                    self.ydir = 0
                else:
                    self.xdir = 0
                    self.ydir = 0
            else:
                self.xdir = 0
                self.ydir = 0
        else:
            self.xdir = 1
            self.ydir = 0
            if not self.inmotion:
                self.txdir = self.xdir
                self.tydir = self.ydir
                self.inmotion = True