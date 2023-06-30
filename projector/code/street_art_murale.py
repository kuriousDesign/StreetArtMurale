import pygame
import sys
import time
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint
from laser import Laser
from asteroid import Asteroid
import os
script_dir = sys.path[0]
player_img_path = os.path.join(script_dir, '../graphics/player.png')
laser_wave_path = os.path.join(script_dir, '../audio/laser.wav')
font_path = os.path.join(script_dir, '../font/Pixeled.ttf')
explosion_wave_path = os.path.join(script_dir, '../audio/explosion.wav')
music_wave_path = os.path.join(script_dir, '../audio/music.wav')
graphics_path = os.path.join(script_dir, '../graphics/')

# Screen parameters
screen_width = 600*2
screen_height = round(600.0*330.0/495.0)*2
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
alien_rows = 2
alien_cols = 8


class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player(
            (screen_width, screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.quit_req = False
        self.end_msg = ""
        self.lives = 3
        self.live_surf = pygame.image.load(
            player_img_path).convert_alpha()
        self.live_x_start_pos = screen_width - \
            (self.live_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font(font_path, 20)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 2
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [
            num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(
            *self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=alien_rows, cols=alien_cols)
        self.alien_direction = 1

        # Asteroids setup
        self.asteroids = pygame.sprite.Group()

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

        # Audio
        music = pygame.mixer.Sound(music_wave_path)
        music.set_volume(0.2)
        music.play(loops=-1)
        self.laser_sound = pygame.mixer.Sound(laser_wave_path)
        self.laser_sound.set_volume(0.5)
        self.explosion_sound = pygame.mixer.Sound(explosion_wave_path)
        self.explosion_sound.set_volume(0.3)

        # CRT
        self.crt = CRT()

    def display_end_msg(self):
        self.end_msg = self.end_msg.upper()
        print("displaying end msg: " + self.end_msg)
        victory_surf = self.font.render(self.end_msg, False, 'white')
        victory_rect = victory_surf.get_rect(
            center=(screen_width / 2, screen_height / 2))
        screen.blit(victory_surf, victory_rect)
        pygame.display.flip()

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(
                        self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def alien_setup(self, rows, cols, x_distance=60, y_distance=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0:
                    alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien('green', x, y)
                else:
                    alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            # print(type(random_alien.rect.center))
            # print(random_alien.rect.center)
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def asteroid_drop(self):
        random_x = int(choice(range(1, screen_width)))
        print(random_x)
        asteroid_sprite = Asteroid((random_x, 50), 6, screen_height)
        self.asteroids.add(asteroid_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400, 800)

    def collision_checks(self):

        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                # alien collisions
                aliens_hit = pygame.sprite.spritecollide(
                    laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    self.explosion_sound.play()

                # extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()

        # alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    print("lives: " + str(self.lives))

                    if self.lives <= 0:
                        self.end_msg = "You Lose! no more lives"
                        self.quit_req = True
                        # pygame.quit()
                        # sys.exit()

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)

                if pygame.sprite.spritecollide(alien, self.player, False):
                    self.end_msg = "You lose! Alien collision"
                    self.quit_req = True

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + \
                (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf, (x, 8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, -10))
        screen.blit(score_surf, score_rect)

    def check_for_remaining_aliens(self):
        if not self.aliens.sprites():
            self.end_msg = 'You won!'
            self.quit_req = True

    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.asteroids.update()
        self.extra.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.asteroids.draw(screen)
        self.extra.draw(screen)
        self.display_lives()
        self.display_score()
        self.check_for_remaining_aliens()
        self.crt.draw()


class StreetArtMurale():

    def __init__(self):
        pass

    def start(self):
        pygame.init()
        game = Game()

        ALIENLASER = pygame.USEREVENT + 1
        ASTEROID = pygame.USEREVENT + 2
        pygame.time.set_timer(ALIENLASER, 600)
        pygame.time.set_timer(ASTEROID, 1000)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("user closed the gameplay screen")
                    pygame.quit()
                    sys.exit()
                if event.type == ALIENLASER:
                    game.alien_shoot()
                if event.type == ASTEROID:
                    game.asteroid_drop()

            screen.fill((30, 30, 30))
            game.run()

            pygame.display.flip()
            clock.tick(60)
            if game.quit_req:
                game.display_end_msg()
                time.sleep(2.0)
                pygame.quit()
                sys.exit()


class CRT:
    def __init__(self):
        self.tv = pygame.image.load(graphics_path + 'tv.png').convert_alpha()
        self.tv = pygame.transform.scale(
            self.tv, (screen_width, screen_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos),
                             (screen_width, y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        screen.blit(self.tv, (0, 0))


if __name__ == '__main__':
    street_art_murale = StreetArtMurale()
    street_art_murale.start()
