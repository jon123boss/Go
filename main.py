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
captured_stones = [0, 0]

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
    global current_player, captured_stones
    x, y = position
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE and board[grid_x][grid_y] == 0:
        if is_legal_move(grid_x, grid_y, current_player):
            board[grid_x][grid_y] = current_player
            captured = capture_stones(grid_x, grid_y, current_player)
            captured_stones[current_player - 1] += captured
            current_player = 2 if current_player == 1 else 1

def is_legal_move(x, y, player):

    if is_suicide(x, y, player):
        return False
    return True

def capture_stones(x, y, player):
    opponent = 2 if player == 1 else 1
    captured = 0
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE and board[new_x][new_y] == opponent:
            if not has_liberty(new_x, new_y, opponent):
                captured += remove_group(new_x, new_y, opponent)
    return captured

def has_liberty(x, y, player):
    visited = set()
    queue = [(x, y)]
    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if board[x][y] == 0:
            return True
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE and board[new_x][new_y] == player:
                queue.append((new_x, new_y))
    return False

def remove_group(x, y, player):
    visited = set()
    queue = [(x, y)]
    captured = 0
    while queue:
        x, y = queue.pop(0)
        if (x, y) in visited:
            continue
        visited.add((x, y))
        if board[x][y] == player:
            board[x][y] = 0
            captured += 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE and board[new_x][new_y] == player:
                queue.append((new_x, new_y))
    return captured

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
