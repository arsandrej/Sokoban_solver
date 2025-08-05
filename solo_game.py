import pygame
import time
from level_loader import load_images
from state_display import *


def run_solo_game(initial_state, astar_solver_func):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban Solo Play")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)

    images = load_images()
    offset_x = (SCREEN_WIDTH - initial_state.width * TILE_SIZE) // 2
    offset_y = (SCREEN_HEIGHT - initial_state.height * TILE_SIZE - 60) // 2

    current_state = initial_state
    move_stack = []
    redo_stack = []
    steps = 0

    start_time = time.time()
    player_time_running = True

    ai_solving = False
    ai_solution = ""
    ai_solution_index = 0
    ai_animation_delay = 300
    ai_animation_timer = 0
    ai_solve_time = 0

    while True:
        dt = clock.tick(60)
        ai_animation_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not ai_solving and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                if event.key in (pygame.K_UP, pygame.K_w):
                    move = 'U'
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    move = 'D'
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    move = 'L'
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    move = 'R'
                else:
                    move = None

                if move:
                    for direction, next_state in current_state.get_successors():
                        if direction == move:
                            move_stack.append(current_state)
                            redo_stack.clear()
                            current_state = next_state
                            steps += 1
                            break

                if event.key == pygame.K_a:
                    player_time_running = False
                    ai_solution, ai_stats = astar_solver_func(current_state)
                    ai_solve_time = ai_stats['execution_time'] if ai_stats else 0
                    if ai_solution:
                        ai_solving = True
                        ai_solution_index = 0
                        ai_animation_timer = 0

        screen.fill((0, 0, 0))
        draw_state(screen, current_state, images, offset_x, offset_y)

        steps_text = font.render(f"Steps: {steps}", True, (255, 255, 255))
        screen.blit(steps_text, (10, 10))

        if ai_solving:
            ai_time_text = font.render(f"AI solve time: {ai_solve_time:.4f} s", True, (255, 255, 255))
            screen.blit(ai_time_text, (10, 40))
        else:
            elapsed = time.time() - start_time if player_time_running else 0
            player_time_text = font.render(f"Player time: {elapsed:.2f} s", True, (255, 255, 255))
            screen.blit(player_time_text, (10, 40))

        if ai_solving and ai_solution:
            if ai_animation_timer >= ai_animation_delay and ai_solution_index < len(ai_solution):
                move = ai_solution[ai_solution_index]
                for direction, next_state in current_state.get_successors():
                    if direction == move:
                        current_state = next_state
                        ai_solution_index += 1
                        ai_animation_timer = 0
                        steps += 1
                        break
            elif ai_solution_index >= len(ai_solution):
                ai_solving = False
                player_time_running = False


        pygame.display.flip()
