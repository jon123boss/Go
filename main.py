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
        check_and_remove_captured_stones(current_player)
        current_player = 2 if current_player == 1 else 1

def get_neighbors(x, y):
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y))
    if x < BOARD_SIZE - 1:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < BOARD_SIZE - 1:
        neighbors.append((x, y+1))
    return neighbors

def find_group(x, y, player):
    group = [(x, y)]
    queue = [(x, y)]
    visited = set(group)

    while queue:
        cx, cy = queue.pop(0)
        for nx, ny in get_neighbors(cx, cy):
            if (nx, ny) not in visited and board[nx][ny] == player:
                visited.add((nx, ny))
                group.append((nx, ny))
                queue.append((nx, ny))
    return group

def has_liberty(group):
    for x, y in group:
        for nx, ny in get_neighbors(x, y):
            if board[nx][ny] == 0:
                return True
    return False

def check_and_remove_captured_stones(player):
    opponent = 2 if player == 1 else 1
    to_remove = []

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == opponent:
                group = find_group(x, y, opponent)
                if not has_liberty(group):
                    to_remove.extend(group)

    for x, y in to_remove:
        board[x][y] = 0

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
