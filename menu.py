import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
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
                    return "solo"
                elif ai_solver_button.collidepoint(event.pos):
                    pygame.quit()
                    return "ai"

        # Draw buttons
        pygame.draw.rect(screen, (70, 130, 180), play_solo_button)
        pygame.draw.rect(screen, (180, 70, 70), ai_solver_button)

        # Draw button text
        play_text = font.render("Play Solo", True, (255, 255, 255))
        ai_text = font.render("AI Solver", True, (255, 255, 255))

        screen.blit(play_text, play_text.get_rect(center=play_solo_button.center))
        screen.blit(ai_text, ai_text.get_rect(center=ai_solver_button.center))

        pygame.display.flip()
        clock.tick(60)
