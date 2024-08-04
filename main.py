import pygame

pygame.init()

WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chinese Go")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (200, 150, 100)

BOARD_SIZE = 19
CELL_SIZE = 30

board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 1

def draw_board():
    screen.fill(BOARD_COLOR)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if board[x][y] == 1:
                pygame.draw.circle(screen, BLACK, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            elif board[x][y] == 2:
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)

def handle_input(position):
    global current_player
    x, y = position
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE and board[grid_x][grid_y] == 0:
        board[grid_x][grid_y] = current_player
        current_player = 2 if current_player == 1 else 1

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_input(event.pos)

    draw_board()

    pygame.display.flip()

pygame.quit()