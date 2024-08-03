import pygame

pygame.init()

BOARD_SIZE = 19
CELL_SIZE = 30

board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

WINDOW_SIZE = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chinese Go")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (200, 150, 100)

def draw_board():
    screen.fill(BOARD_COLOR)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board()

    pygame.display.flip()

pygame.quit()