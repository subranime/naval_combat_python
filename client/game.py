import shared
import math
import pygame


class Ship:
    def __init__(self, speed, position):
        self.position = position
        self.speed = speed

    def move(self):
        self.position[0] += self.speed

        if (self.position[0] - shared.SHIP_SPRITE.get_width() / 2 > shared.RESOLUTION[0] and self.speed > 0) or (
                self.position[0] + shared.SHIP_SPRITE.get_width() / 2 < 0 and self.speed < 0):
            self.speed *= -1


class Submarine:
    def __init__(self, position):
        self.position = position
        self.angle = 0
        self.rot_speed = 1
        self.max_angle = 23
        self.min_angle = -23

    def rotate(self, direction: int):
        self.angle += -direction * self.rot_speed
        if self.angle > self.max_angle:
            self.angle = self.max_angle
        elif self.angle < self.min_angle:
            self.angle = self.min_angle


class Torpedo:
    def __init__(self, position, angle):
        self.speed = 5
        self.position = position
        self.angle = angle

    def move(self):
        self.position[0] += math.cos(math.radians(self.angle + 90)
                                     ) * self.speed
        self.position[1] -= math.sin(math.radians(self.angle + 90)
                                     ) * self.speed


class Game:
    def __init__(self, ship_list):
        self.ship_list = ship_list
        self.submarine = Submarine(
            [shared.RESOLUTION[0]/2, shared.RESOLUTION[1] - shared.RESOLUTION[1]/4])
        self.torpedo = None
        self.torpedoes_left = 10

    def tick(self, right_press, left_press, fire_press):
        destroyed_ship_position = None

        if right_press:
            self.submarine.rotate(1)
        elif left_press:
            self.submarine.rotate(-1)

        if fire_press:
            if not self.torpedo and self.torpedoes_left:
                self.torpedo = Torpedo(
                    self.submarine.position.copy(), self.submarine.angle)
                self.torpedoes_left -= 1

        if self.torpedo:
            self.torpedo.move()

            ship_to_delete = None
            torpedo_rect = pygame.Rect(self.torpedo.position[0] -
                                       shared.TORPEDO_SIZE / 2,
                                       self.torpedo.position[1] -
                                       shared.TORPEDO_SIZE / 2, shared.TORPEDO_SIZE, shared.TORPEDO_SIZE)
            for ship in self.ship_list:
                ship_rect = pygame.Rect(ship.position[0] -
                                        shared.SHIP_SPRITE.get_width() / 2,
                                        ship.position[1] -
                                        shared.SHIP_SPRITE.get_height() / 2,
                                        shared.SHIP_SPRITE.get_width(),
                                        shared.SHIP_SPRITE.get_height())
                if ship_rect.colliderect(torpedo_rect):
                    ship_to_delete = ship
                    break

            if ship_to_delete:
                destroyed_ship_position = ship_to_delete.position.copy()
                self.ship_list.remove(ship_to_delete)
                self.torpedo = None
            elif not (0 < self.torpedo.position[0] < shared.RESOLUTION[0]) or not (0 < self.torpedo.position[1] < shared.RESOLUTION[1]):
                self.torpedo = None

        for ship in self.ship_list:
            ship.move()

        return {'destroyed_ship_position': destroyed_ship_position}
