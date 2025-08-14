import csv
import numpy as np
import pygame

def statistics():
    with open('sokoban_stats_combined.csv', 'r') as file:
        switch = 0
        no_deadlock = ()
        yes_deadlock = ()
        differences_time = []
        differences_node = []
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if switch == 0:
                print("-------------------------")
                print("Algorthm ", row["algorithm"], " for level: ", row["level_num"])
            if row["deadlock_checked"] == "No":
                switch = 1
                print("Without deadlock:")
                print("Time: ",row["time_s"],"Explored nodes: ", row["explored_nodes"], "Steps: ", row["steps"])
                no_deadlock = (row["explored_nodes"], row["time_s"])
            else:
                switch = 0
                print("With deadlock:")
                print("Time: ",row["time_s"],"Explored nodes: ", row["explored_nodes"], "Steps: ", row["steps"])
                yes_deadlock = (row["explored_nodes"], row["time_s"])
                print("Differences with deadlock: ")
                print("Time difference: ", float(yes_deadlock[1]) - float(no_deadlock[1]))
                print("Explored Node difference: ", (float(yes_deadlock[0]) - float(no_deadlock[0])))
                differences_time.append(float(yes_deadlock[1]) - float(no_deadlock[1]))
                differences_node.append(float(yes_deadlock[0]) - float(no_deadlock[0]))
        print("-------------------------")
        print("Average Differences in Time: ", np.mean(differences_time))
        print("Average Differences in Explored Node: ", np.mean(differences_node))

def load_statistics_data():
    data = {}
    with open('sokoban_stats_combined.csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            level_num = int(row["level_num"])
            algorithm = row["algorithm"]
            deadlock = row["deadlock_checked"]

            if level_num not in data:
                data[level_num] = {}

            if algorithm not in data[level_num]:
                data[level_num][algorithm] = {}

            data[level_num][algorithm][deadlock] = {
                "time": float(row["time_s"]),
                "nodes": int(row["explored_nodes"]),
                "steps": int(row["steps"])
            }
    return data


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HEADER_HEIGHT = 80
FOOTER_HEIGHT = 60
COLUMN_WIDTH = 170
ROW_HEIGHT = 30
PADDING = 15

# Colors
COLORS = {
    "background": (30, 30, 30),
    "header": (30, 35, 42),
    "text": (220, 220, 220),
    "highlight": (97, 175, 239),
    "a_star": (152, 195, 121),
    "bfs": (229, 192, 123),
    "dfs": (198, 120, 221),
    "grid": (60, 64, 72),
    "deadlock_yes": (86, 182, 194),
    "deadlock_no": (224, 108, 117),
    "level_button": (70, 130, 180),
    "level_button_hover": (100, 160, 210),
    "level_button_text": (240, 240, 240),
    "back_button": (180, 70, 70),
    "back_button_hover": (210, 100, 100),
}


def load_statistics_data():
    data = {}
    try:
        with open('sokoban_stats_combined.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                level_num = int(row["level_num"])
                algorithm = row["algorithm"]
                deadlock = row["deadlock_checked"]

                if level_num not in data:
                    data[level_num] = {}

                if algorithm not in data[level_num]:
                    data[level_num][algorithm] = {}

                data[level_num][algorithm][deadlock] = {
                    "time": float(row["time_s"]),
                    "nodes": int(row["explored_nodes"]),
                    "steps": int(row["steps"])
                }
    except FileNotFoundError:
        print("Statistics file not found!")
    return data


def draw_level_selection(screen, levels):
    screen.fill(COLORS["background"])

    title_font = pygame.font.SysFont(None, 48)
    level_font = pygame.font.SysFont(None, 32)
    info_font = pygame.font.SysFont(None, 24)

    title = title_font.render("Sokoban Statistics - Select Level", True, COLORS["text"])
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    button_width = 80
    button_height = 60
    horizontal_spacing = 100
    vertical_spacing = 80
    start_x = (SCREEN_WIDTH - (5 * horizontal_spacing)) // 2
    start_y = 100

    level_buttons = []

    for i, level_num in enumerate(sorted(levels.keys())):
        row = i // 5
        col = i % 5
        x = start_x + col * horizontal_spacing
        y = start_y + row * vertical_spacing

        button_rect = pygame.Rect(x, y, button_width, button_height)
        level_buttons.append((button_rect, level_num))

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            color = COLORS["level_button_hover"]
        else:
            color = COLORS["level_button"]

        pygame.draw.rect(screen, color, button_rect, border_radius=5)
        pygame.draw.rect(screen, COLORS["grid"], button_rect, 2, border_radius=5)

        level_text = level_font.render(str(level_num), True, COLORS["level_button_text"])
        screen.blit(level_text, (x + button_width // 2 - level_text.get_width() // 2,
                                 y + button_height // 2 - level_text.get_height() // 2))

    footer_text = info_font.render("Click on a level to view its statistics | ESC to return to menu",
                                   True, COLORS["text"])
    screen.blit(footer_text, (SCREEN_WIDTH // 2 - footer_text.get_width() // 2,
                              SCREEN_HEIGHT - 40))

    return level_buttons


def draw_statistics_screen(screen, level_data, level_num):
    screen.fill(COLORS["background"])

    title_font = pygame.font.SysFont(None, 48)
    header_font = pygame.font.SysFont(None, 28)
    data_font = pygame.font.SysFont(None, 24)

    title = title_font.render(f"Statistics for Level {level_num}", True, COLORS["text"])
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

    back_button = pygame.Rect(20, 20, 120, 40)
    mouse_pos = pygame.mouse.get_pos()
    if back_button.collidepoint(mouse_pos):
        pygame.draw.rect(screen, COLORS["back_button_hover"], back_button, border_radius=5)
    else:
        pygame.draw.rect(screen, COLORS["back_button"], back_button, border_radius=5)

    back_text = data_font.render("Back", True, COLORS["text"])
    screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2,
                            back_button.centery - back_text.get_height() // 2))

    headers = ["Algorithm", "Deadlock", "Time (s)", "Nodes", "Steps"]
    header_y = HEADER_HEIGHT

    for i, header in enumerate(headers):
        text = header_font.render(header, True, COLORS["highlight"])
        x = PADDING + i * COLUMN_WIDTH
        screen.blit(text, (x, header_y))

    y = HEADER_HEIGHT + ROW_HEIGHT
    algorithms = ["A* Search", "BFS", "DFS"]

    for algo in algorithms:
        if algo not in level_data:
            continue

        algo_color = COLORS["a_star"] if "A*" in algo else COLORS["bfs"] if "BFS" in algo else COLORS["dfs"]
        text = data_font.render(algo, True, algo_color)
        screen.blit(text, (PADDING, y + 5))

        for deadlock in ["No", "Yes"]:
            if deadlock not in level_data[algo]:
                continue
            #Draw all the data
            data = level_data[algo][deadlock]
            deadlock_color = COLORS["deadlock_no"] if deadlock == "No" else COLORS["deadlock_yes"]

            deadlock_text = data_font.render(deadlock, True, deadlock_color)
            screen.blit(deadlock_text, (PADDING + COLUMN_WIDTH, y + 5))

            time_text = data_font.render(f"{data['time']:.4f}", True, COLORS["text"])
            screen.blit(time_text, (PADDING + 2 * COLUMN_WIDTH, y + 5))

            nodes_text = data_font.render(f"{data['nodes']:,}", True, COLORS["text"])
            screen.blit(nodes_text, (PADDING + 3 * COLUMN_WIDTH, y + 5))

            steps_text = data_font.render(str(data['steps']), True, COLORS["text"])
            screen.blit(steps_text, (PADDING + 4 * COLUMN_WIDTH, y + 5))

            pygame.draw.line(screen, COLORS["grid"], (PADDING, y + ROW_HEIGHT),
                             (SCREEN_WIDTH - PADDING, y + ROW_HEIGHT), 1)
            y += ROW_HEIGHT

    for i in range(6):
        x = PADDING + i * COLUMN_WIDTH - 30
        pygame.draw.line(screen, COLORS["grid"], (x, HEADER_HEIGHT),
                         (x, SCREEN_HEIGHT - FOOTER_HEIGHT), 1)

    footer_font = pygame.font.SysFont(None, 24)
    footer_text = footer_font.render("Press ESC to return to menu", True, COLORS["text"])
    screen.blit(footer_text, (SCREEN_WIDTH // 2 - footer_text.get_width() // 2,
                              SCREEN_HEIGHT - FOOTER_HEIGHT + 20))

    return back_button


def visualize_statistics():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban Statistics")

    data = load_statistics_data()

    current_screen = "level_selection"
    selected_level = None

    clock = pygame.time.Clock()

    running = True
    while running:
        if current_screen == "level_selection":
            level_buttons = draw_level_selection(screen, data)
        elif current_screen == "level_stats" and selected_level is not None:
            back_button = draw_statistics_screen(screen, data[selected_level], selected_level)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if current_screen == "level_stats":
                        current_screen = "level_selection"
                    else:
                        running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()

                    if current_screen == "level_selection":
                        for button_rect, level_num in level_buttons:
                            if button_rect.collidepoint(mouse_pos):
                                selected_level = level_num
                                current_screen = "level_stats"
                                break

                    elif current_screen == "level_stats":
                        if back_button.collidepoint(mouse_pos):
                            current_screen = "level_selection"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
