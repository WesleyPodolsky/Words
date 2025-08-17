import pygame
import math
import random
from config import *


class Lander(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self._original_image = pygame.image.load('resources/lander.png')
        self.image = self._original_image
        self.rect = self.image.get_rect()
        self.rect.center = (600, 60)
        self._veloc_x = random.uniform(-1, 1)
        self._veloc_y = random.uniform(0, 1)
        self._rotation = 0
        self._fuel = START_FUEL
        self._damage = 0
        self._crashed = False
        self._controllable = True
        self._altitude = 660
        self._no_collision_duration = 0
        self._x_pixels_to_move = 0
        self._y_pixels_to_move = 0

    def rotate_right(self):
        """Rotates lander 1° clockwise."""
        self._rotation -= 1
        self.image = pygame.transform.rotozoom(self._original_image, self._rotation, 1)

    def rotate_left(self):
        """Rotates lander 1° counterclockwise."""
        self._rotation += 1
        self.image = pygame.transform.rotozoom(self._original_image, self._rotation, 1)

    def get_rotation(self):
        """Returns lander's current rotation in degrees."""
        return self._rotation

    def thrust(self):
        """Propels the lander if it has sufficient fuel."""
        if self._fuel >= THRUST_COST:
            sin = math.sin(math.radians(self._rotation))
            cos = math.cos(math.radians(self._rotation))
            self._veloc_x += 0.33 * -sin
            self._veloc_y -= 0.33 * cos
            self._fuel -= THRUST_COST
            return True
        return False

    def has_safe_landing_speed(self):
        """Returns True if the lander's current velocities are within the predefined range"""
        return self._veloc_x < SAFE_LANDING_SPEED and self._veloc_y < SAFE_LANDING_SPEED

    def is_horizontal(self):
        """Returns True if the lander is rotated horizontally. Allows for small variance in rotation
           so the lander can be reasonably tilted when landing. Makes the game less strict."""
        return -5 < self._rotation < 5

    def current_altitude(self):
        """Returns lander's current altitude."""
        return self._altitude

    def current_damage(self):
        """Returns lander's current damage."""
        return self._damage

    def current_fuel(self):
        """Returns lander's current fuel."""
        return self._fuel

    def current_veloc_x(self):
        """Returns lander's current horizontal velocity formatted with two decimal digits."""
        return float("{0:.2f}".format(self._veloc_x))

    def current_veloc_y(self):
        """Returns lander's current vertical velocity formatted with two decimal digits."""
        return float("{0:.2f}".format(self._veloc_y))

    def is_crashed(self):
        """Returns True if the lander is crashed. In this game it means the lander has hit the screen's lower bound."""
        return self._crashed

    def deal_damage(self, amount):
        """Inflict a given amount of damage. Maximum damage lander can reach is 100%."""
        self._damage += amount
        if self._damage > 100:
            self._damage = 100

    def set_no_collision_duration(self, duration):
        """Sets number of ticks for which the lander is immune to collisions with objects/meteors."""
        self._no_collision_duration = duration

    def decrease_no_collision_duration(self):
        """Removes one tick of immunity to collisions."""
        if self._no_collision_duration > 0:
            self._no_collision_duration -= 1

    def can_collide(self):
        """Returns True if the lander has no ticks of immunity to collisions."""
        return not self._no_collision_duration

    def is_controllable(self):
        """Returns True if it's possible to control the lander."""
        return self._controllable

    def count_for_air_resistance(self):
        """Reduces lander's horizontal speed by the value specified in AIR_RESISTANCE."""
        if self._veloc_x > AIR_RESISTANCE:
            self._veloc_x -= AIR_RESISTANCE
        elif self._veloc_x < -AIR_RESISTANCE:
            self._veloc_x += AIR_RESISTANCE

    def count_for_gravity(self):
        """Increases lander's vertical speed by the value specified in GRAVITY"""
        self._veloc_y += GRAVITY

    def move(self):
        """X and Y velocities are added up on every tick. Once they are greater than 1.0 or less than -1.0
           - ergo one pixel on screen, the lander moves by an integer in the appropriate direction."""
        self._x_pixels_to_move += self._veloc_x
        self._y_pixels_to_move += self._veloc_y

        # move right
        if self._x_pixels_to_move > 1:
            self.rect.move_ip(self._x_pixels_to_move, 0)
            self._x_pixels_to_move -= int(self._x_pixels_to_move)
        # move left
        elif self._x_pixels_to_move < -1:
            self.rect.move_ip(self._x_pixels_to_move, 0)
            self._x_pixels_to_move += int(abs(self._x_pixels_to_move))

        # move down
        if self._y_pixels_to_move > 1:
            self.rect.move_ip(0, self._y_pixels_to_move)
            self._y_pixels_to_move -= int(self._y_pixels_to_move)
        # move up
        elif self._y_pixels_to_move < -1:
            self.rect.move_ip(0, self._y_pixels_to_move)
            self._y_pixels_to_move += int(abs(self._y_pixels_to_move))

    def update(self):
        """Operations executed on every tick."""
        self.count_for_air_resistance()
        self.count_for_gravity()
        self.move()

        self._altitude = HEIGHT - self.rect.bottom

        # If the lander tries to fly off the top of the screen:
        # keeps it in place, deals damage, sets Y velocity to random value
        if self.rect.top < 0:
            self.rect.top = 1
            self._damage += 5
            self._veloc_y = random.uniform(0, 1)
        # Marks the lander as crashed if it hits the bottom of the screen
        elif self.rect.bottom > HEIGHT:
            self._crashed = True

        # Wraps the lander around left and right edges
        if self.rect.left < 0:
            self.rect.right = WIDTH
        elif self.rect.right > WIDTH:
            self.rect.left = 0

        # Marks the lander as uncontrollable if damage is at least 100
        if self._damage >= 100:
            self._controllable = False
