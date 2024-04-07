import pygame

RED = (255, 0, 0)


class ghost:
    def __init__(self, x, y, speed, radius, walls, gxy, screen, cell_size, gw, gh):
        self.x = x
        self.y = y
        self.xdir = 0
        self.ydir = 0
        self.modes = ['scatter', 'chase', 'frightened']
        self.mode = 'scatter'
        self.color = RED
        self.speed = speed
        self.radius = radius
        self.walls = walls
        # all ghosts coordinates
        self.gxy = gxy
        # self.pacman = pacman
        self.screen = screen
        self.cell_size = cell_size
        self.gw = gw
        self.gh = gh
        self.cx = (self.x * cell_size) + radius
        self.cy = (self.y * cell_size) + radius
        self.path = []
        self.inmotion = False
        self.img = pygame.image.load("shark/tiburonBoss_zps49108ed3-1.png.png")
        self.img = pygame.transform.scale(self.img, (cell_size*2, cell_size*2))

        self.grid = []
        for i in range(self.gh):
            self.grid.append([])
            for j in range(self.gw):
                if (j, i) in walls:
                    self.grid[i].append(1)
                else:
                    self.grid[i].append(0)

    def update(self):
        self.cx += self.xdir * self.speed
        self.cy += self.ydir * self.speed
        # pygame.draw.circle(self.screen, RED, (self.cx, self.cy), self.radius)
        self.screen.blit(self.img, (self.cx - self.cell_size, self.cy - self.cell_size))
        self.inmotion = True
        # print('just drawing')
        # checking if motion from one square to other is over
        if (self.cx == ((self.x + self.xdir) * self.cell_size) + self.radius) and (
            self.cy == ((self.y + self.ydir) * self.cell_size) + self.radius):
            self.inmotion = False
            self.x += self.xdir
            # print('ghost new x', self.x)
            self.y += self.ydir
            # print('ghost new y', self.y)
            # wrapping around grid edges
            self.x %= self.gw
            self.y %= self.gh
            self.cx = (self.x * self.cell_size) + self.radius
            self.cy = (self.y * self.cell_size) + self.radius

    def scatter(self):
        # random movement # go towards 'home' corners
        pass

    def chase(self, pacman):
        # use a* algorithm to find route to pacman
        if not self.inmotion:
            if (self.x, self.y) == (pacman.x, pacman.y):
                return

                # if len(self.path) > 0:
                    # if pacman and ghost havent moved, then there is no need to update path
                    # if (self.x, self.y) == self.path[0]:
                    #     return

                # marking other ghost coordinates as obstacles
            grid = self.grid
            # for [x, y] in self.gxy:
            #     grid[y][x] = 1

            print('starting point: ', self.x, self.y)
            print('pacman: ', pacman.x, pacman.y)
            self.path = self.astar((self.x, self.y), (pacman.x, pacman.y), grid)
            print(self.path)

            if self.path != None:
                if self.path[1][0] != self.x:
                    self.xdir = self.path[1][0] - self.x
                    self.ydir = 0
                elif self.path[1][1] != self.y:
                    self.xdir = 0
                    self.ydir = self.path[1][1] - self.y
            else:
                self.xdir = 0
                self.ydir = 0

    def frightened(self):
        # aimlessly wander away from pacman
        pass

    def astar(self, start, goal, grid):
        start_node = Node(start[0], start[1])
        goal_node = Node(goal[0], goal[1])

        start_node.g_score = 0
        start_node.f_score = self.heuristic(start_node, goal_node)

        open_set = []
        open_set.append(start_node)
        explored = [(start_node.x, start_node.y)]

        while len(open_set) > 0:
            current = self.lowest_f_score(open_set)

            # if final node is found
            if (current.x == goal_node.x) and (current.y == goal_node.y):
                path = []
                while current.parent != None:
                    path.append((current.x, current.y))
                    current = current.parent
                path.append((current.x, current.y))
                return path[::-1]

            open_set.remove(current)

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                neighbor_x, neighbor_y = current.x + dx, current.y + dy
                # wrapping around screen edges
                neighbor_x %= self.gw
                neighbor_y %= self.gh


                if grid[neighbor_y][neighbor_x] == 0:
                    if (neighbor_x, neighbor_y) in explored:
                        continue

                    neighbor = Node(neighbor_x, neighbor_y)
                    neighbor.parent = current
                    neighbor.g_score = current.g_score + 1
                    neighbor.f_score = neighbor.g_score + self.heuristic(neighbor, goal_node)

                    explored.append((neighbor.x, neighbor.y))
                    open_set.append(neighbor)
                else:
                    continue

        return None

    def heuristic(self, node, goal):
        # Manhattan district heuristic
        return abs(node.x - goal.x) + abs(node.y - goal.y)

    def lowest_f_score(self, open_set):
        min_node = None
        min_f_score = float('inf')
        for node in open_set:
            if node.f_score < min_f_score:
                min_node = node
                min_f_score = node.f_score
        return min_node


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # we want to pick the lowest f_score(g_score + h_score) out of the open list so we initialize it as infinity
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.parent = None
