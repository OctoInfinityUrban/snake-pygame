import pygame
import sys
import time
import random

# Difficulty settings
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Initialize Pygame
def init_game(frame_size_x, frame_size_y):
    check_errors = pygame.init()
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initializing game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialized')
    pygame.display.set_caption('Snake Eater')
    return pygame.display.set_mode((frame_size_x, frame_size_y))

# Title Screen
def title_screen(game_window, frame_size_x, frame_size_y):
    title_font = pygame.font.SysFont('times new roman', 90)
    title_surface = title_font.render('Snake Eater', True, green)
    title_rect = title_surface.get_rect()
    title_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(title_surface, title_rect)

    # Start button
    start_button = pygame.Rect(frame_size_x / 2 - 50, frame_size_y / 2, 100, 50)
    pygame.draw.rect(game_window, green, start_button)
    start_font = pygame.font.SysFont('times new roman', 30)
    start_surface = start_font.render('Start', True, black)
    start_rect = start_surface.get_rect(center=start_button.center)
    game_window.blit(start_surface, start_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    waiting = False

# Game Over
def game_over(game_window, score, frame_size_x, frame_size_y):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(game_window, score, 0, red, 'times', 20, frame_size_x, frame_size_y)

    # Restart button
    restart_button = pygame.Rect(frame_size_x / 2 - 50, frame_size_y / 2, 100, 50)
    pygame.draw.rect(game_window, green, restart_button)
    restart_font = pygame.font.SysFont('times new roman', 30)
    restart_surface = restart_font.render('Restart', True, black)
    restart_rect = restart_surface.get_rect(center=restart_button.center)
    game_window.blit(restart_surface, restart_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    waiting = False
                    main()

# Show Score
def show_score(game_window, score, choice, color, font, size, frame_size_x, frame_size_y):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Main game loop
def main():
    game_window = init_game(frame_size_x, frame_size_y)
    fps_controller = pygame.time.Clock()

    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
    food_spawn = True
    direction = 'RIGHT'
    change_to = direction
    score = 0

    title_screen(game_window, frame_size_x, frame_size_y)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, ord('w')]:
                    change_to = 'UP'
                if event.key in [pygame.K_DOWN, ord('s')]:
                    change_to = 'DOWN'
                if event.key in [pygame.K_LEFT, ord('a')]:
                    change_to = 'LEFT'
                if event.key in [pygame.K_RIGHT, ord('d')]:
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        food_spawn = True

        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10 or snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10:
            game_over(game_window, score, frame_size_x, frame_size_y)
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(game_window, score, frame_size_x, frame_size_y)

        show_score(game_window, score, 1, white, 'consolas', 20, frame_size_x, frame_size_y)
        pygame.display.update()
        fps_controller.tick(difficulty)

if __name__ == '__main__':
    main()
    