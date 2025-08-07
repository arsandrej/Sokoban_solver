import pygame
from level_loader import load_images

_images = load_images()
_player_img = _images["player"]
_images = load_images()
player_img_scaled = pygame.transform.scale(_images["player"], (128, 128))

def you_win(screen, width, height):
    font_big = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 32)
    font_smaller = pygame.font.SysFont(None, 24)

    text = font_big.render("You Win!", True, (255, 255, 0))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 30))

    padding = 10
    player_rect_1 = player_img_scaled.get_rect()
    player_rect_1.midleft = (text_rect.right + padding, text_rect.centery)

    player_rect_2 = player_img_scaled.get_rect()
    player_rect_2.midright= (text_rect.left - padding, text_rect.centery)

    instruction = font_small.render("Press R to reset or ESC to quit", True, (200, 200, 200))
    instruction_rect = instruction.get_rect(center=(width // 2, height // 2 + 40))

    menu = font_smaller.render("Press M to return to main Menu", True, (255, 0, 0))
    menu_rect = instruction.get_rect(center=(width // 2 + 40, height // 2 + 80))


    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    screen.blit(player_img_scaled, player_rect_1)
    screen.blit(player_img_scaled, player_rect_2)
    screen.blit(instruction, instruction_rect)
    screen.blit(menu, menu_rect)
    pygame.display.flip()
