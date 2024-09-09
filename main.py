import pygame
from pygame.locals import *

WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10

COL1 = (0, 0, 0)
COL2 = (255, 255, 255)
COL3 = (20, 20, 20)
COL4 = (40, 40, 40)

FRAMERATE = 60

running = True
paused = True
tick_time = 0
time_tick = 100
board = []

clock = pygame.time.Clock()


class Cell:
    def __init__(self, pos, state):
        self.pos = {"x": pos[0], "y": pos[1]}

        self.state = state

    def check_neighbours(self):
        global board
        non = 0

        for offset in [
            [-1, -1],
            [0, -1],
            [1, -1],
            [1, 0],
            [1, 1],
            [0, 1],
            [-1, 1],
            [-1, 0],
        ]:
            if (
                self.pos["y"] // CELL_SIZE + offset[1] >= 0
                and self.pos["y"] // CELL_SIZE + offset[1] <= (HEIGHT // CELL_SIZE) - 1
                and self.pos["x"] // CELL_SIZE + offset[0] >= 0
                and self.pos["x"] // CELL_SIZE + offset[0] <= (WIDTH // CELL_SIZE) - 1
            ):
                if (
                    board[self.pos["y"] // CELL_SIZE + offset[1]][
                        self.pos["x"] // CELL_SIZE + offset[0]
                    ].state
                    == True
                ):
                    non += 1

        return non

    def toggle_self(self):
        self.state = not self.state


def create_board():
    board = []
    for i in range(HEIGHT // CELL_SIZE):
        _y = []
        for j in range(WIDTH // CELL_SIZE):
            _y.append(Cell((j * CELL_SIZE, i * CELL_SIZE), False))
        board.append(_y)
    return board


board = create_board()

display = pygame.display.set_mode((WIDTH, HEIGHT))
display.fill(COL1)
pygame.display.set_caption("Game Of Life")


def draw_square(size, pos, color):
    square_surf = pygame.Surface(size)
    square_surf.fill(color)
    display.blit(square_surf, pos, square_surf.get_rect())


def update_cells():
    global board

    new_board = create_board()

    for _y, r in enumerate(board):
        for _x, c in enumerate(r):
            non = c.check_neighbours()
            if c.state:
                if non < 2 or non > 3:
                    new_board[_y][_x].state = False
                else:
                    new_board[_y][_x].state = True
            elif non == 3:
                new_board[_y][_x].state = True

    board = new_board.copy()


pygame.display.flip()

while running:
    for event in pygame.event.get():
        # Input
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Pause/Play
                paused = not paused
            elif event.key == K_c:
                # Clear
                board = create_board()
            elif event.key == K_UP:
                time_tick -= 50
                if time_tick < 0:
                    time_tick = 0
            elif event.key == K_DOWN:
                time_tick += 50

        # Check for quit event
        if event.type == QUIT:
            running = False

    # Mouse input
    # Mouse 1
    if pygame.mouse.get_pressed()[0]:
        _x, _y = pygame.mouse.get_pos()
        if (
            _x >= 0
            and _x < WIDTH
            and _y >= 0
            and _y < HEIGHT
            and not board[_y // CELL_SIZE][_x // CELL_SIZE].state
        ):
            board[_y // CELL_SIZE][_x // CELL_SIZE].toggle_self()

    # Mouse 2
    if pygame.mouse.get_pressed()[2]:
        _x, _y = pygame.mouse.get_pos()
        if (
            _x >= 0
            and _x < WIDTH
            and _y >= 0
            and _y < HEIGHT
            and board[_y // CELL_SIZE][_x // CELL_SIZE].state
        ):
            board[_y // CELL_SIZE][_x // CELL_SIZE].toggle_self()

    _y = 0
    for row in board:
        _x = 0
        for c in row:
            if paused:
                if c.state:
                    draw_square((CELL_SIZE, CELL_SIZE), (_x, _y), (COL4))
                    draw_square(
                        (CELL_SIZE - 2, CELL_SIZE - 2), (_x + 1, _y + 1), (COL2)
                    )
                else:
                    draw_square((CELL_SIZE, CELL_SIZE), (_x, _y), (COL4))
                    draw_square(
                        (CELL_SIZE - 2, CELL_SIZE - 2), (_x + 1, _y + 1), (COL3)
                    )
            else:
                if c.state:
                    draw_square((CELL_SIZE, CELL_SIZE), (_x, _y), (COL3))
                    draw_square(
                        (CELL_SIZE - 2, CELL_SIZE - 2), (_x + 1, _y + 1), (COL2)
                    )
                else:
                    draw_square((CELL_SIZE, CELL_SIZE), (_x, _y), (COL3))
                    draw_square(
                        (CELL_SIZE - 2, CELL_SIZE - 2), (_x + 1, _y + 1), (COL1)
                    )
            _x += CELL_SIZE
        _y += CELL_SIZE

    if not paused and tick_time + time_tick <= pygame.time.get_ticks():
        tick_time = pygame.time.get_ticks()

        update_cells()

    clock.tick(FRAMERATE)
    pygame.display.flip()
