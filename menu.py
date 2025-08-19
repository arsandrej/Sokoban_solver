import pygame
import os
import re
from stats_analysis import statistics, visualize_statistics

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
FONT_SIZE = 36
global THEME
THEME = "blue"

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

def run_menu():
    global THEME
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban Main Menu")

    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    play_solo_button = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 120), (BUTTON_WIDTH, BUTTON_HEIGHT))
    ai_solver_button = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 240), (BUTTON_WIDTH, BUTTON_HEIGHT))
    settings_button = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 360), (BUTTON_WIDTH, BUTTON_HEIGHT))
    stats_button = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 480), (BUTTON_WIDTH, BUTTON_HEIGHT))

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, None  # User closed window

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_solo_button.collidepoint(event.pos):
                    pygame.quit()
                    return "solo", None, THEME
                elif ai_solver_button.collidepoint(event.pos):
                    pygame.quit()
                    return "ai", None, THEME
                elif settings_button.collidepoint(event.pos):
                    path = run_settings_menu()
                    return "settings", path, THEME
                elif stats_button.collidepoint(event.pos):
                    # statistics()
                    res = visualize_statistics()
                    if res == "quit":
                        return res, None, None
                    return run_menu()

        # Draw buttons
        pygame.draw.rect(screen, (70, 130, 180), play_solo_button)
        pygame.draw.rect(screen, (180, 70, 70), ai_solver_button)
        pygame.draw.rect(screen, (100, 100, 180), settings_button)
        pygame.draw.rect(screen, (255,64,0), stats_button)

        # Draw button text
        play_text = font.render("Play Solo", True, (255, 255, 255))
        ai_text = font.render("AI Solver", True, (255, 255, 255))
        settings_text = font.render("Settings", True, (255, 255, 255))
        stats_text = font.render("Statistics", True, (255, 255, 255))

        screen.blit(play_text, play_text.get_rect(center=play_solo_button.center))
        screen.blit(ai_text, ai_text.get_rect(center=ai_solver_button.center))
        screen.blit(settings_text, settings_text.get_rect(center=settings_button.center))
        screen.blit(stats_text, stats_text.get_rect(center=stats_button.center))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return None, None, None

def run_settings_menu():
    global THEME
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Settings")

    font = pygame.font.SysFont(None, 32)
    clock = pygame.time.Clock()

    select_level_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 150, 200, 60)
    change_theme_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 60)

    while True:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if select_level_button.collidepoint(event.pos):
                    selected = level_selector()
                    return selected  # Return the selected level
                elif change_theme_button.collidepoint(event.pos):
                    new_theme = change_theme()
                    THEME = new_theme
                    if new_theme is None:
                        THEME = "blue"
                        new_theme = "didnt work"
                    print(f"Change Theme clicked THEME: {THEME}")
                    print(f"Change Theme clicked new_theme: {new_theme}")
                    return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return None #Back to the menu

        pygame.draw.rect(screen, (70, 130, 180), select_level_button)
        pygame.draw.rect(screen, (180, 130, 70), change_theme_button)

        level_text = font.render("Select Level", True, (255, 255, 255))
        theme_text = font.render("Change Theme", True, (255, 255, 255))
        instr_text = font.render("Press M to return to menu", True, (200, 200, 200))

        screen.blit(instr_text, (20, 20))
        screen.blit(level_text, level_text.get_rect(center=select_level_button.center))
        screen.blit(theme_text, theme_text.get_rect(center=change_theme_button.center))

        pygame.display.flip()
        clock.tick(60)


def level_selector():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Select Level")

    font = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()

    level_files = [f for f in os.listdir("levels") if f.endswith(".txt")]
    level_files = sorted(level_files, key=extract_number)
    row_height = 28
    padding = 5
    scroll_offset = 0
    scroll_speed = row_height + padding

    max_visible_rows = SCREEN_HEIGHT // (row_height + padding)

    while True:
        screen.fill((40, 40, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # scroll up
                    scroll_offset = max(0, scroll_offset - scroll_speed)
                elif event.button == 5:  # scroll down
                    max_scroll = max(0, (len(level_files) - max_visible_rows) * (row_height + padding))
                    scroll_offset = min(max_scroll, scroll_offset + scroll_speed)
                else:
                    # Check if clicked on level
                    for i, level_file in enumerate(level_files):
                        y = 50 + i * (row_height + padding) - scroll_offset
                        rect = pygame.Rect(50, y, 500, row_height)
                        if 0 <= y <= SCREEN_HEIGHT and rect.collidepoint(event.pos):
                            return f"levels/{level_file}"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scroll_offset = max(0, scroll_offset - scroll_speed)
                elif event.key == pygame.K_DOWN:
                    max_scroll = max(0, (len(level_files) - max_visible_rows) * (row_height + padding))
                    scroll_offset = min(max_scroll, scroll_offset + scroll_speed)

        # Draw title
        title_font = pygame.font.SysFont(None, 36)
        title_text = title_font.render("Select Level:", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(title_text, title_rect)

        # Draw level list
        rect_width = 300
        rect_x = (SCREEN_WIDTH - rect_width) // 2


        for i, level_file in enumerate(level_files):
            y = 50 + i * (row_height + padding) - scroll_offset
            if -row_height < y < SCREEN_HEIGHT:
                rect = pygame.Rect(rect_x, y, rect_width, row_height)
                pygame.draw.rect(screen, (70, 130, 180), rect)

                text = font.render(level_file, True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

def change_theme():
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    themes = ["blue", "red", "brown", "gray"]  # 4 theme choices
    cols = len(themes)

    padding = 24
    button_w = 140
    button_h = 56
    image_size = 64

    total_width = cols * button_w + (cols + 1) * padding
    start_x = max(padding, (SCREEN_WIDTH - total_width) // 2 + padding)

    # Set image position
    buttons = []
    y_button = SCREEN_HEIGHT - padding - button_h - 250
    y_image = y_button - padding - image_size
    for i, theme in enumerate(themes):
        x = start_x + i * (button_w + padding)
        rect = pygame.Rect(x, y_button, button_w, button_h)
        img_pos = (x + (button_w - image_size) // 2, y_image)
        buttons.append((rect, theme, img_pos))

    # Preload themed thumbnails
    thumbs = {}
    for _, theme, _ in buttons:
        theme_path = os.path.join("images", theme, "box_on_goal.png")
        shared = os.path.join("images", "box_on_goal.png")
        img = None
        for p in (theme_path, shared):
            try:
                img = pygame.image.load(p).convert_alpha()
                img = pygame.transform.smoothscale(img, (image_size, image_size))
                break
            except Exception:
                img = None
        if img is None: #No image found
            surf = pygame.Surface((image_size, image_size), pygame.SRCALPHA)
            surf.fill((150, 0, 150, 200))
            img = surf
        thumbs[theme] = img

    selected = None
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                selected = None
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                selected = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        screen.fill((30, 30, 30))

        instr = font.render("Choose box color theme (Esc to cancel)", True, (200, 200, 200))
        screen.blit(instr, (20, 20))

        # Draw Buttons and Thumbnail
        for rect, theme, img_pos in buttons:
            if rect.collidepoint((mx, my)):
                pygame.draw.rect(screen, (100, 180, 140), rect, border_radius=6) #On hover
                if clicked:
                    selected = theme
                    running = False
            else:
                pygame.draw.rect(screen, (70, 130, 180), rect, border_radius=6)

            screen.blit(thumbs[theme], img_pos)

            label = font.render(theme.capitalize(), True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=rect.center))

        pygame.display.flip()
        clock.tick(60)

    return selected
