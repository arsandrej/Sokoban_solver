import pygame
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 80
FONT_SIZE = 36

def run_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sokoban Main Menu")

    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    play_solo_button = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 120), (BUTTON_WIDTH, BUTTON_HEIGHT))
    ai_solver_button = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 240), (BUTTON_WIDTH, BUTTON_HEIGHT))
    settings_button = pygame.Rect((SCREEN_WIDTH // 2 - BUTTON_WIDTH // 2, 360), (BUTTON_WIDTH, BUTTON_HEIGHT))

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # User closed window

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_solo_button.collidepoint(event.pos):
                    pygame.quit()
                    return "solo", None
                elif ai_solver_button.collidepoint(event.pos):
                    pygame.quit()
                    return "ai", None
                elif settings_button.collidepoint(event.pos):
                    path = run_settings_menu()
                    return "settings", path

        # Draw buttons
        pygame.draw.rect(screen, (70, 130, 180), play_solo_button)
        pygame.draw.rect(screen, (180, 70, 70), ai_solver_button)
        pygame.draw.rect(screen, (100, 100, 180), settings_button)

        # Draw button text
        play_text = font.render("Play Solo", True, (255, 255, 255))
        ai_text = font.render("AI Solver", True, (255, 255, 255))
        settings_text = font.render("Settings", True, (255, 255, 255))

        screen.blit(play_text, play_text.get_rect(center=play_solo_button.center))
        screen.blit(ai_text, ai_text.get_rect(center=ai_solver_button.center))
        screen.blit(settings_text, settings_text.get_rect(center=settings_button.center))

        pygame.display.flip()
        clock.tick(60)

def run_settings_menu():
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
                    print(selected)
                    return selected  # Return the selected level
                elif change_theme_button.collidepoint(event.pos):
                    print("Change Theme clicked")

        pygame.draw.rect(screen, (70, 130, 180), select_level_button)
        pygame.draw.rect(screen, (180, 130, 70), change_theme_button)

        level_text = font.render("Select Level", True, (255, 255, 255))
        theme_text = font.render("Change Theme", True, (255, 255, 255))

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
                pygame.draw.rect(screen, (100, 100, 100), rect)

                text = font.render(level_file, True, (255, 255, 255))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)
