import pygame
import time
import os

TILE_SIZE = 64
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FONT_SIZE = 24
BUTTON_HEIGHT = 40

# Load images once globally
def load_images():
    base_path = "images"
    return {
        "wall": pygame.image.load(os.path.join(base_path, "wall.png")),
        "goal": pygame.image.load(os.path.join(base_path, "goal.png")),
        "box": pygame.image.load(os.path.join(base_path, "box.png")),
        "box_on_goal": pygame.image.load(os.path.join(base_path, "box_on_goal.png")),
        "player": pygame.image.load(os.path.join(base_path, "player.png")),
        "floor": pygame.image.load(os.path.join(base_path, "floor.png")),
    }

def draw_state(screen, state, images, offset_x=0, offset_y=0):
    for y, row in enumerate(state.grid):
        for x, _ in enumerate(row):
            pos = (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE)

            screen.blit(images["floor"], pos)

            if state.is_wall(x, y):
                screen.blit(images["wall"], pos)
            elif (x, y) == state.player:
                player_image = images["player"]
                player_image_scaled = pygame.transform.scale(player_image, (64, 64))
                screen.blit(player_image_scaled, pos)
            elif (x, y) in state.goals and (x, y) in state.boxes:
                screen.blit(images["box_on_goal"], pos)
            elif (x, y) in state.goals:
                goal_offset = (16, 16)
                goal_pos = (pos[0] + goal_offset[0], pos[1] + goal_offset[1])
                screen.blit(images["goal"], goal_pos)
            elif (x, y) in state.boxes:
                screen.blit(images["box"], pos)


    pygame.display.flip()

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
    animation_delay = 300

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

        screen.blit(time_text, (10, 10))
        screen.blit(nodes_text, (10, 40))

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
                animation_timer = 0  # reset timer

        elif animation_running:
            # Animation finished
            animation_running = False

        pygame.display.flip()

    pygame.quit()
