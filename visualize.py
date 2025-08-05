import pygame
from level_loader import load_images
from state_display import *

def run_game(initial_state,
             astar_solution, astar_stats,
             bfs_solution, bfs_stats,
             dfs_solution, dfs_stats):
    current_stats = None

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban Solver Visualization")

    font = pygame.font.SysFont(None, FONT_SIZE)
    images = load_images()

    buttons = {
        "A*": pygame.Rect(10, SCREEN_HEIGHT - BUTTON_HEIGHT - 10, 80, BUTTON_HEIGHT),
        "BFS": pygame.Rect(100, SCREEN_HEIGHT - BUTTON_HEIGHT - 10, 80, BUTTON_HEIGHT),
        "DFS": pygame.Rect(190, SCREEN_HEIGHT - BUTTON_HEIGHT - 10, 80, BUTTON_HEIGHT),
    }

    offset_x = (SCREEN_WIDTH - initial_state.width * TILE_SIZE) // 2
    offset_y = (SCREEN_HEIGHT - initial_state.height * TILE_SIZE - 60) // 2

    clock = pygame.time.Clock()
    animation_running = False
    animation_solution = ""
    animation_index = 0
    current_state = initial_state
    animation_timer = 0
    animation_delay = 250

    def draw_buttons():
        for text, rect in buttons.items():
            pygame.draw.rect(screen, (180, 180, 180), rect)
            label = font.render(text, True, (0, 0, 0))
            screen.blit(label, (rect.x + 10, rect.y + 10))

    def draw_stats():
        if current_stats is None:
            return

        time_text = font.render(f"Time: {current_stats['execution_time']:.4f} s", True, (255, 255, 255))
        nodes_text = font.render(f"Explored Nodes: {current_stats['explored_nodes']}", True, (255, 255, 255))
        steps_text = font.render(f"Steps: {len(animation_solution)}", True, (255, 255, 255))

        screen.blit(time_text, (10, 10))
        screen.blit(nodes_text, (10, 50))
        screen.blit(steps_text, (10, 90))

    def draw_solution_banner():
        if not animation_solution:
            return

        chars_per_line = 70
        lines = [animation_solution[i:i + chars_per_line] for i in range(0, len(animation_solution), chars_per_line)]

        line_height = 36
        padding = 10
        banner_height = line_height * len(lines) + padding * 2

        banner_top = SCREEN_HEIGHT - BUTTON_HEIGHT - banner_height - 20
        banner_rect = pygame.Rect(0, banner_top, SCREEN_WIDTH, banner_height)
        pygame.draw.rect(screen, (200, 0, 0), banner_rect)

        for i, line in enumerate(lines):
            label = font.render(line, True, (255, 255, 255))
            label_rect = label.get_rect(
                center=(SCREEN_WIDTH // 2, banner_top + padding + i * line_height + line_height // 2))
            screen.blit(label, label_rect)

    running = True
    while running:
        dt = clock.tick(60)
        animation_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not animation_running:
                if buttons["A*"].collidepoint(event.pos):
                    current_stats = astar_stats
                    animation_solution = astar_solution
                    animation_running = True
                    animation_index = 0
                    current_state = initial_state
                    animation_timer = 0

                elif buttons["BFS"].collidepoint(event.pos):
                    current_stats = bfs_stats
                    animation_solution = bfs_solution
                    animation_running = True
                    animation_index = 0
                    current_state = initial_state
                    animation_timer = 0

                elif buttons["DFS"].collidepoint(event.pos):
                    current_stats = dfs_stats
                    animation_solution = dfs_solution
                    animation_running = True
                    animation_index = 0
                    current_state = initial_state
                    animation_timer = 0

        # Draw everything
        screen.fill((0, 0, 0))
        draw_state(screen, current_state, images, offset_x=offset_x, offset_y=offset_y)
        draw_buttons()
        draw_stats()
        draw_solution_banner()

        # Animate moves
        if animation_running and animation_index < len(animation_solution):
            if animation_timer >= animation_delay:
                move = animation_solution[animation_index]
                # Update current_state with next move
                for direction, next_state in current_state.get_successors():
                    if direction == move:
                        current_state = next_state
                        break

                animation_index += 1
                animation_timer = 0

        elif animation_running:
            animation_running = False

        pygame.display.flip()

    pygame.quit()
