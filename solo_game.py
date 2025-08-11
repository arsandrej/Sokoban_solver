import time
from level_loader import load_images
from state_display import *
from you_win import you_win

def run_solo_game(initial_state, astar_solver_func, theme):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban Solo Play")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)

    images = load_images(theme)
    offset_x = (SCREEN_WIDTH - initial_state.width * TILE_SIZE) // 2
    offset_y = (SCREEN_HEIGHT - initial_state.height * TILE_SIZE - 60) // 2

    current_state = initial_state.clone()
    move_stack = []
    redo_stack = []
    steps = 0

    start_time = time.time()
    player_time_running = True
    player_won = False

    ai_solving = False
    ai_solution = ""
    ai_solution_index = 0
    ai_animation_delay = 300
    base_ai_delay = ai_animation_delay
    ai_speed_fast = False
    ai_animation_timer = 0
    ai_solve_time = 0
    ai_failed_to_solve = False

    win_delay_timer = 0
    win_delay_duration = 1000  # milliseconds delay after finishes moves

    button_width = 160
    button_height = 40
    button_x = SCREEN_WIDTH - button_width - 20
    button_y = 20
    ai_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    reset_button_rect = pygame.Rect(SCREEN_WIDTH - button_width - 20, 70, button_width, button_height)
    undo_button_rect = pygame.Rect(SCREEN_WIDTH - button_width - 20, 120, button_width, button_height)
    speed_button_rect = pygame.Rect(SCREEN_WIDTH - button_width - 20, 170, button_width, button_height)

    waiting_for_input = False  # Waiting after win

    while True:
        dt = clock.tick(60)
        ai_animation_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if waiting_for_input:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        return "Menu"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return None
                    elif event.key == pygame.K_r:  # Reset game after win
                        current_state = initial_state.clone()
                        move_stack.clear()
                        redo_stack.clear()
                        steps = 0
                        start_time = time.time()
                        player_time_running = True
                        ai_solving = False
                        ai_solution = ""
                        ai_solution_index = 0
                        ai_solve_time = 0
                        ai_failed_to_solve = False
                        win_delay_timer = 0
                        waiting_for_input = False
                        player_won = False

            elif event.type == pygame.KEYDOWN and not ai_solving and not waiting_for_input:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return None

                if event.key == pygame.K_r and ai_failed_to_solve:
                    current_state = initial_state.clone()
                    move_stack.clear()
                    redo_stack.clear()
                    steps = 0
                    start_time = time.time()
                    player_time_running = True
                    ai_solving = False
                    ai_solution = ""
                    ai_solution_index = 0
                    ai_solve_time = 0
                    ai_failed_to_solve = False
                    win_delay_timer = 0
                    waiting_for_input = False
                    player_won = False

                if not ai_failed_to_solve:
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
                        for direction, next_state in current_state.get_successors(skip_deadlock_check=True):
                            if direction == move:
                                move_stack.append(current_state)
                                redo_stack.clear()
                                current_state = next_state
                                steps += 1
                                if current_state.is_goal():
                                    player_time_running = False
                                    win_delay_timer = 0
                                    player_won = True
                                    waiting_for_input = False

                                break

            elif event.type == pygame.MOUSEBUTTONDOWN and not waiting_for_input:
                if ai_button_rect.collidepoint(event.pos):  # Solve with AI
                    player_time_running = False
                    ai_solution, ai_stats = astar_solver_func(current_state)
                    ai_solve_time = ai_stats['execution_time'] if ai_stats else 0
                    if ai_solution:
                        ai_solving = True
                        ai_solution_index = 0
                        ai_animation_timer = 0
                        win_delay_timer = 0
                        ai_failed_to_solve = False
                    else:
                        ai_failed_to_solve = True
                        player_time_running = False

                elif reset_button_rect.collidepoint(event.pos):  # Reset game
                    current_state = initial_state.clone()
                    move_stack.clear()
                    redo_stack.clear()
                    steps = 0
                    ai_solving = False
                    ai_solution = ""
                    ai_solution_index = 0
                    ai_solve_time = 0
                    start_time = time.time()
                    player_time_running = True
                    ai_failed_to_solve = False
                    win_delay_timer = 0
                    waiting_for_input = False

                elif undo_button_rect.collidepoint(event.pos) and not ai_solving:  # Undo
                    if move_stack:
                        current_state = move_stack.pop()
                        steps = max(steps - 1, 0)

                elif speed_button_rect.collidepoint(event.pos):  # Toggle Speed
                    ai_speed_fast = not ai_speed_fast
                    ai_animation_delay = base_ai_delay // 2 if ai_speed_fast else base_ai_delay
                    ai_animation_timer = 0

        screen.fill((0, 0, 0))
        draw_state(screen, current_state, images, offset_x, offset_y)

        # Draw step and time text
        steps_text = font.render(f"Steps: {steps}", True, (255, 255, 255))
        screen.blit(steps_text, (10, 10))

        if ai_solving:
            ai_time_text = font.render(f"AI solve time: {ai_solve_time:.4f} s", True, (255, 255, 255))
            screen.blit(ai_time_text, (10, 40))
        else:
            elapsed = time.time() - start_time if player_time_running else 0
            player_time_text = font.render(f"Player time: {elapsed:.2f} s", True, (255, 255, 255))
            screen.blit(player_time_text, (10, 40))

        # Draw buttons
        pygame.draw.rect(screen, (70, 130, 180), ai_button_rect)
        button_text = font.render("Solve with AI", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=ai_button_rect.center)
        screen.blit(button_text, text_rect)

        pygame.draw.rect(screen, (180, 70, 70), reset_button_rect)
        reset_text = font.render("Reset", True, (255, 255, 255))
        reset_text_rect = reset_text.get_rect(center=reset_button_rect.center)
        screen.blit(reset_text, reset_text_rect)

        pygame.draw.rect(screen, (100, 180, 100), undo_button_rect)
        undo_text = font.render("Undo", True, (255, 255, 255))
        undo_text_rect = undo_text.get_rect(center=undo_button_rect.center)
        screen.blit(undo_text, undo_text_rect)

        pygame.draw.rect(screen, (140, 100, 200), speed_button_rect)
        speed_label = "2x Speed: ON" if ai_speed_fast else "2x Speed: OFF"
        speed_text = font.render(speed_label, True, (255, 255, 255))
        speed_text_rect = speed_text.get_rect(center=speed_button_rect.center)
        screen.blit(speed_text, speed_text_rect)

        if player_won and not waiting_for_input:
            win_delay_timer += dt
            if win_delay_timer >= win_delay_duration:
                waiting_for_input = True

        # AI animation
        if ai_solving and ai_solution:
            if ai_solution_index < len(ai_solution):
                if ai_animation_timer >= ai_animation_delay:
                    move = ai_solution[ai_solution_index]
                    for direction, next_state in current_state.get_successors():
                        if direction == move:
                            current_state = next_state
                            ai_solution_index += 1
                            ai_animation_timer = 0
                            steps += 1
                            break
            else:
                if current_state.is_goal():
                    win_delay_timer += dt
                    if win_delay_timer >= win_delay_duration:
                        ai_solving = False
                        player_time_running = False
                        waiting_for_input = True
                else:
                    ai_solving = False

        if waiting_for_input:
            you_win(screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        if ai_failed_to_solve:
            # Draw popup
            popup_w, popup_h = 400, 120
            popup_x = (SCREEN_WIDTH - popup_w) // 2
            popup_y = (SCREEN_HEIGHT - popup_h) // 2
            pygame.draw.rect(screen, (30, 30, 30), (popup_x, popup_y, popup_w, popup_h))
            pygame.draw.rect(screen, (255, 255, 0), (popup_x, popup_y, popup_w, popup_h), 4)

            warning_text = font.render("Can't be solved!", True, (255, 255, 0))
            instr_text = font.render("Press R to reset or ESC to quit", True, (255, 255, 255))
            screen.blit(warning_text, warning_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 40)))
            screen.blit(instr_text, instr_text.get_rect(center=(SCREEN_WIDTH // 2, popup_y + 80)))

        pygame.display.flip()
