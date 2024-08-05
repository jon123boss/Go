import pygame
import time

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
previous_boards = []
turn_timer = 30
start_time = time.time()

def draw_board():
    screen.fill(BOARD_COLOR)
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            if board[x][y] == 1:
                pygame.draw.circle(screen, BLACK, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            elif board[x][y] == 2:
                pygame.draw.circle(screen, WHITE, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)


def display_death_screen():
    font = pygame.font.Font(None, 72)
    if current_player == 1:
        winner_text = "White Wins!"
    else:
        winner_text = "Black Wins!"

    winner_surface = font.render(winner_text, True, BLACK)
    restart_surface = font.render("Click 'r' to start", True, BLACK)

    winner_rect = winner_surface.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 50))
    restart_rect = restart_surface.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 + 50))

    screen.fill(BOARD_COLOR)
    screen.blit(winner_surface, winner_rect)
    screen.blit(restart_surface, restart_rect)
    pygame.display.flip()
def draw_timer():
    global start_time, turn_timer

    elapsed_time = time.time() - start_time
    remaining_time = max(0, turn_timer - elapsed_time)

    font = pygame.font.Font(None, 36)
    timer_surface = font.render(f"Time Left: {int(remaining_time)}s", True, BLACK)
    screen.blit(timer_surface, (10, 10))

    if remaining_time <= 0:
        switch_player()

def handle_input(position):
    global current_player, start_time
    x, y = position
    grid_x = x // CELL_SIZE
    grid_y = y // CELL_SIZE
    if 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE and board[grid_x][grid_y] == 0:
        save_board_state()
        board[grid_x][grid_y] = current_player
        check_and_remove_captured_stones(current_player)
        switch_player()

def switch_player():
    global current_player, start_time
    current_player = 2 if current_player == 1 else 1
    start_time = time.time()

def save_board_state():
    global previous_boards
    previous_boards.append([row[:] for row in board])

def undo_move():
    global previous_boards, current_player
    if previous_boards:
        board[:] = previous_boards.pop()
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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            undo_move()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
            current_player = 1
            previous_boards = []
            start_time = time.time()

    draw_board()
    draw_timer()

    if len(previous_boards) >= BOARD_SIZE * BOARD_SIZE:
        display_death_screen()
        continue

    pygame.display.flip()

pygame.quit()
