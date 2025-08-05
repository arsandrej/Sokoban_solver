import pygame

TILE_SIZE = 64
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
FONT_SIZE = 24
BUTTON_HEIGHT = 40

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
