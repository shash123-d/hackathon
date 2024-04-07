import pygame

pygame.init()

GRID_SIZE = 30
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_SIZE = (GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


def get_grid_coordinates(pos):
    x, y = pos
    grid_x = x // GRID_SIZE
    grid_y = y // GRID_SIZE
    return grid_x, grid_y


def main():
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Grid")

    grid = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    clicked_boxes = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    grid_x, grid_y = get_grid_coordinates(event.pos)
                    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
                        grid[grid_y][grid_x] = not grid[grid_y][grid_x]
                        if grid[grid_y][grid_x]:
                            clicked_boxes.append((grid_x, grid_y))
                        else:
                            clicked_boxes.remove((grid_x, grid_y))

        screen.fill(WHITE)

        # Draw grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                if grid[y][x]:
                    pygame.draw.rect(screen, BLUE, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

        pygame.display.flip()

    pygame.quit()
    print(clicked_boxes)


if __name__ == "__main__":
    main()
