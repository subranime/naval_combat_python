import shared
import pygame
import game
import math
import connector

connector.req_connect()
ships = connector.wait_for_data('ships')

connector.req_scores()
text = connector.wait_for_data('scores')
print(f'Список очков:\r\n{text}')

starting_number = len(ships)

current_game = game.Game(ships)

right_press = False
left_press = False
fire_press = False

clock = pygame.time.Clock()


explosion_timer = 0
explosion_dest = None

score = 0


def rotate_draw(sprite, dest, angle):
    sprite_rot = pygame.transform.rotate(
        sprite, angle)
    sprite_rect = sprite_rot.get_rect(
        center=sprite.get_rect().center)
    sprite_dest = (
        dest[0] - sprite.get_width()/2, dest[1] - sprite.get_height()/2)

    shared.WINDOW.blit(
        sprite_rot, (sprite_rect.topleft[0] + sprite_dest[0], sprite_rect.topleft[1] + sprite_dest[1]))


while True:
    shared.WINDOW.fill((0, 0, 0))

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            quit()

        if shared.CURRENT_STATE == 'game':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right_press = True
                if event.key == pygame.K_LEFT:
                    left_press = True
                if event.key == pygame.K_SPACE:
                    fire_press = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right_press = False
                if event.key == pygame.K_LEFT:
                    left_press = False
                if event.key == pygame.K_SPACE:
                    fire_press = False

    if shared.CURRENT_STATE == 'game':
        for i in range(math.ceil(shared.RESOLUTION[0] / shared.WATER_SPRITE.get_width())):
            for j in range(math.ceil(shared.RESOLUTION[1] / shared.WATER_SPRITE.get_height())):
                shared.WINDOW.blit(
                    shared.WATER_SPRITE, (i * shared.WATER_SPRITE.get_width(), j * shared.WATER_SPRITE.get_height()))

        if current_game.torpedo:
            rotate_draw(shared.TORPEDO_SPRITE,
                        current_game.torpedo.position, current_game.torpedo.angle)

        rotate_draw(shared.SUBMARINE_SPRITE,
                    current_game.submarine.position, current_game.submarine.angle)

        for ship in current_game.ship_list:
            ship_dest = [ship.position[0] - shared.SHIP_SPRITE.get_width() /
                         2, ship.position[1] - shared.SHIP_SPRITE.get_height() / 2]
            sprite = shared.SHIP_SPRITE
            if ship.speed < 0:
                sprite = pygame.transform.flip(shared.SHIP_SPRITE, 1, 0)
            shared.WINDOW.blit(sprite, ship_dest)

        tick_report = current_game.tick(right_press, left_press, fire_press)

        if tick_report['destroyed_ship_position']:
            pygame.mixer.Sound.play(shared.EXPLOSION_SOUND)
            explosion_dest = tick_report['destroyed_ship_position']
            explosion_timer = 10

        if explosion_timer > 0:
            explosion_timer -= 1
            shared.WINDOW.blit(
                shared.EXPLOSION_SPRITE,
                (explosion_dest[0] - shared.EXPLOSION_SPRITE.get_width() / 2,
                 explosion_dest[1] - shared.EXPLOSION_SPRITE.get_height() / 2))

        text_surface, rect = shared.GAME_FONT.render(
            f'Осталось торпед: {current_game.torpedoes_left}', (0, 0, 0))
        shared.WINDOW.blit(
            text_surface, (rect[0] + (shared.RESOLUTION[0] - text_surface.get_width()) / 2,
                           shared.RESOLUTION[1] * (7/8)))

    clock.tick(shared.FPS)
    pygame.display.flip()

    if (current_game.torpedoes_left == 0 and not current_game.torpedo) or not any(current_game.ship_list):
        score = starting_number - len(current_game.ship_list)
        name = input('Введите ваше имя: ').replace(' ', '_')
        connector.send_score(name, score)
        connector.req_scores()
        text = connector.wait_for_data('scores')
        print(f'Список очков:\r\n{text}')
        quit()
