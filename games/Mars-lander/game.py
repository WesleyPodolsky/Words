import sys
from lander import *
from pad import *
from obstacle import *
from meteor import *
from config import *


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Mars Lander')
        self.ticks, self.time, self.score, self.failure_ticks, self.non_collision_ticks, self.failure = 0, 0, 0, 0, 0, 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background_image = pygame.image.load("resources/mars_background.png")
        self.instruments = pygame.image.load("resources/instruments.png")
        self.alert_instruments = pygame.image.load("resources/instruments_alert.png")
        # I made the thrust_image same resolution as lander image. As a result,
        # they rotate around the same axis and the flame is always where it should be.
        self.thrust_image_original = pygame.image.load('resources/thrust.png')
        self.pad_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.meteor_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.GroupSingle()
        self.lander = Lander()
        self.lander_lives = 0
        self.player_sprite.add(self.lander)

    def spawn_pads(self):
        """NUMBER_OF_PADS times spawns a pad randomly on the screen. The pad may be tall or regular.
           It does not overlap with previously spawned pads."""
        self.pad_sprites.empty()
        while len(self.pad_sprites) < NUMBER_OF_PADS:
            tall = random.choice([True, False])
            pad = Pad(random.randrange(79, WIDTH - 79), random.randrange(HEIGHT - 200, HEIGHT), tall=tall)
            pad_collision = pygame.sprite.spritecollide(pad, self.pad_sprites, False)
            if not pad_collision:
                self.pad_sprites.add(pad)

    def spawn_obstacles(self):
        """NUMBER_OF_OBSTACLES times spawns an obstacle randomly on screen.
           It does not overlap with previously spawned obstacles."""
        self.obstacle_sprites.empty()
        number_of_obstacles = random.randint(MIN_OBSTACLES, MAX_OBSTACLES)
        while len(self.obstacle_sprites) < number_of_obstacles:
            obstacle = Obstacle(random.randrange(0, WIDTH), random.randrange(HEIGHT - 500, HEIGHT))
            obstacle_collision = pygame.sprite.spritecollide(obstacle, self.obstacle_sprites, False)
            if not obstacle_collision:
                self.obstacle_sprites.add(obstacle)

    def spawn_meteors(self, count=random.randint(MIN_METEORS, MAX_METEORS), random_height=False):
        """Spawns a number of meteors, defaultsto a random number between MIN_METEORS and MAX_METEORS.
           These spawn on top of the screen, unless random_height is True. The only time random_height is true
           in this game is at the beginning of each mission, so the game looks more naturally with the meteors already
           flying on the screen."""
        for _ in range(count):
            new_meteor = Meteor(random.randrange(0, WIDTH), random.randrange(0, HEIGHT - 400) if random_height else 0)
            self.meteor_sprites.add(new_meteor)

    def replace_off_screen_meteors(self):
        """Deletes a meteor once it flies off the screen, replaces it with a new one."""
        for meteor in self.meteor_sprites:
            if meteor.is_off_screen():
                meteor.kill()
                self.spawn_meteors(1)
                del meteor

    def lander_has_both_legs_on_pad(self, pad_list):
        """Returns True if the lander has both legs on the pad it has landed on and False otherwise."""
        pad = pad_list[0]
        if pad.rect.left <= self.lander.rect.left and pad.rect.right >= self.lander.rect.right:
            return True
        return False

    def successful_landing(self):
        """If the lander has landed successfully, increases the score, displays a message, and starts a new mission.
           The less damage the lander has, the more score is awarded."""
        self.score += 150 - self.lander.current_damage()
        self.reset_lander("Nice landing!")

    def unsuccessful_landing(self):
        """If the lander has landed unsuccessfully, decreases lives, displays a message, and starts a new mission."""
        self.lander_lives -= 1
        self.reset_lander('Unsuccessful landing!')

    def lander_crashed(self):
        """If the lander has crashed, decreases lives, displays a message, and starts a new mission."""
        self.lander_lives -= 1
        self.reset_lander("Lander crashed!")

    def reset_lander(self, msg=""):
        """Destroys the current lander object, creates a new instance of lander, pauses the game."""
        self.player_sprite.remove(self.lander)
        self.lander = Lander()
        self.player_sprite.add(self.lander)
        self.pause(msg)

    def lander_failure(self):
        """Unless the lander has already a failure, there is a FAILURE_CHANCE that the lander will suffer a failure
           of a random component from features_list for FAILURE_DURATION. Otherwise decreases the duration of
           current failure."""
        failures_list = ["Right Rotation",
                         "Left Rotation",
                         "Thrust"
                         ]
        if self.failure_ticks == 0:
            self.failure = 0
            if random.uniform(0, 1) < FAILURE_CHANCE:
                self.failure_ticks += FAILURE_DURATION
                self.failure = random.choice(failures_list)
            return False
        else:
            self.failure_ticks -= 1
            return True

    def update_lander_meters(self):
        """Variables stored in hud_components_locations are reassigned to represent actual values
           and then displayed on the screen at their respective coordinates."""
        hud_components_locations = [
            [int(self.time), (72, 10)],
            [self.lander.current_fuel(), (72, 32)],
            [self.lander.current_damage(), (94, 54)],
            [self.lander.current_altitude(), (258, 10)],
            [self.lander.current_veloc_x(), (278, 32)],
            [self.lander.current_veloc_y(), (278, 54)],
            [self.score, (75, 82)],
            ["Lives: " + str(self.lander_lives), (1110, 10)],
            ["Meteors: " + str(len(self.meteor_sprites)), (1110, 32)]
        ]
        for instrument in hud_components_locations:
            self.show_on_screen(instrument[0], instrument[1])

    def show_on_screen(self, string, location, font='Arial', font_size=20, colour=WHITE):
        """Shortcut do display a string on a location, with the possibility
           to modify font-face, font-size, and colour."""
        msg = pygame.font.SysFont(font, font_size).render(str(string), True, colour)
        self.screen.blit(msg, location)

    def update_all_elements(self):
        """Renders background image, draws every group of sprites on the screen and calls update method where necessary.
           If the lander is faulty or uncontrollable, an error message is displayed and red instrument panel
           is rendered. If the lander is fully functional, the panel is grey. Finally, all instruments are displayed."""
        self.screen.blit(self.background_image, (0, 0))
        self.pad_sprites.draw(self.screen)
        self.obstacle_sprites.draw(self.screen)
        self.meteor_sprites.update()
        self.meteor_sprites.draw(self.screen)
        self.player_sprite.update()
        self.player_sprite.draw(self.screen)
        if not self.lander.is_controllable():
            self.screen.blit(self.alert_instruments, (0, 0))
            self.show_on_screen("UNCONTROLLABLE", (120, 82))
        elif self.lander_failure():
            self.screen.blit(self.alert_instruments, (0, 0))
            self.show_on_screen("Failure of " + str(self.failure), (120, 82))
        else:
            self.screen.blit(self.instruments, (0, 0))
        self.update_lander_meters()

    def pause(self, msg=""):
        """Pauses the game. A small 'menu' is displayed on a transparent overlay. The player has two options:
           press Enter to continue the game, or press ESC to end the current session."""
        pygame.event.clear()
        self.update_all_elements()

        # transparent overlay
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((255, 255, 255, 128))
        self.screen.blit(s, (0, 0))

        self.show_on_screen(msg, (400, 360), font_size=60, colour=RED)
        self.show_on_screen("PAUSED", (500, 600), font_size=50)
        self.show_on_screen("Press Enter to continue", (500, 650), font_size=30)
        self.show_on_screen("Press ESC to finish game", (500, 680), font_size=30)

        pygame.display.flip()
        while True:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN or e.key == pygame.K_KP_ENTER:
                    break
                elif e.key == pygame.K_ESCAPE:
                    self.end_game()

    def end_game(self):
        """A menu with black background displayed when the player ends the game manually from pause menu or loses every
           life. Previous score is displayed along with a menu which allows the player to start a new game or exit
           the game completely."""
        pygame.event.clear()
        self.screen.fill(BLACK)
        self.show_on_screen("GAME OVER", (500, 600), font_size=50)
        self.show_on_screen("Press \"N\" to start a new game", (500, 650), font_size=30)
        self.show_on_screen("Press \"ESC\" to exit", (500, 710), font_size=30)
        self.show_on_screen("SCORE: " + str(self.score), (500, 560), font_size=50)
        pygame.display.flip()

        # clears previously pressed key
        pygame.event.wait()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_n:
                    self.reset_lander()
                    self.play()

    def lander_collided(self, dmg):
        """Deals damage to the lander and makes it immune to environmental collisions for NO_COLLISION_DURATION."""
        self.lander.deal_damage(dmg)
        self.lander.set_no_collision_duration(NO_COLLISION_DURATION)

    def play(self):
        """"Main game loop."""

        # set player lives to LANDER_LIVES_START
        self.lander_lives = LANDER_LIVES_START
        # game runs while the player has at least on life.
        while self.lander_lives > 0:
            # Spawn static sprites and a set of meteors. The game is paused, a message is displayed.
            self.spawn_pads()
            self.spawn_obstacles()
            self.meteor_sprites.empty()
            self.spawn_meteors(random_height=True)
            self.pause("New game")
            while True:
                # This block denotes one tick of a game.
                self.update_all_elements()
                self.replace_off_screen_meteors()

                # when meteor collides with a landing pad, the meteor gets destroyed and replaced.
                self.spawn_meteors(len(pygame.sprite.groupcollide(self.pad_sprites, self.meteor_sprites, False, True)))
                # when meteor collides with an obstacle, the meteor gets destroyed and replaced.
                self.spawn_meteors(
                    len(pygame.sprite.groupcollide(self.obstacle_sprites, self.meteor_sprites, False, True)))

                # checks for pressed keys
                pygame.event.pump()
                key = pygame.key.get_pressed()
                if key[pygame.K_p]:
                    self.pause()
                # right rotation
                if key[pygame.K_RIGHT] and self.lander.is_controllable() and self.failure != "Right Rotation":
                    self.lander.rotate_right()
                # left rotation
                if key[pygame.K_LEFT] and self.lander.is_controllable() and self.failure != "Left Rotation":
                    self.lander.rotate_left()
                # thrust
                if key[pygame.K_SPACE] and self.lander.is_controllable() and self.failure != "Thrust" \
                        and self.lander.current_fuel() >= THRUST_COST:
                    self.lander.thrust()
                    # rotates thrust_image so it corresponds to lander sprite, then displays it.
                    thrust_image = pygame.transform.rotozoom(self.thrust_image_original, self.lander.get_rotation(), 1)
                    self.screen.blit(thrust_image, (self.lander.rect.x, self.lander.rect.y))
                # checks for exit command
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                # check whether the lander has collided with an obstacle
                if self.lander.can_collide():
                    # if lander collides with an environmental object: destroys the obstacle/meteor hit,
                    # deals damage, makes lander briefly invincible
                    obstacle_collision = pygame.sprite.spritecollide(self.lander, self.obstacle_sprites, True)
                    if obstacle_collision:
                        # 10 damage for obstacle collision
                        self.lander_collided(10)
                    # If a meteor is hit by the player, it is not replaced.
                    # This is done on purpose as it lowers the game's difficulty
                    # as the lander gets damaged. Otherwise it was too complicated to land safely.
                    meteor_collision = pygame.sprite.spritecollide(self.lander, self.meteor_sprites, True)
                    if meteor_collision:
                        # 25 damage for meteor collision
                        self.lander_collided(25)
                else:
                    # decrease lander's invincibility ticks.
                    self.lander.decrease_no_collision_duration()

                # Displays 'NOCOL' on the instruments panel if the lander has recently hit an object
                # and is still immune to collisions.
                if not self.lander.can_collide() and self.lander.is_controllable():
                    self.show_on_screen("NOCOL", (290, 10), colour=GREEN)

                # checks whether the lander has landed
                landed = pygame.sprite.spritecollide(self.lander, self.pad_sprites, False)
                if landed:
                    if self.lander.has_safe_landing_speed() and self.lander.is_horizontal() \
                            and self.lander_has_both_legs_on_pad(landed):
                        self.successful_landing()
                    else:
                        self.unsuccessful_landing()
                    break
                # Check if lander has hit lower bound of the screen.
                elif self.lander.is_crashed():
                    self.lander_crashed()
                    break

                # Significantly increases gravity once the lander has reached 100% damage. This is done so the
                # player doesn't have to wait ages for a new mission once their lander has been destroyed.
                if not self.lander.is_controllable():
                    for _ in range(3):
                        self.lander.count_for_gravity()

                # Update the displayed image, increase ticks counter and update time counter which is based on it.
                pygame.display.flip()
                self.ticks += 1
                self.time = self.ticks / 30
        # conclude game
        self.end_game()
