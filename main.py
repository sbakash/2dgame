import pygame
import random
import player
import time

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
show_start_screen = True
game_active = False
show_end_screen = False
show_win_screen = False

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protect the family")

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

score = 0

font = pygame.font.SysFont(None, 36)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((20, 10))
        bullet_color = (0, 157, 242)
        self.image.fill(
            bullet_color)  # made the bullet as a plain color surface as of now will change it to a image later
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.x += 10  # Moves the bullet to the right by 10 pixels
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class MiniBoss(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.original_sheet = pygame.image.load("mini_boss_inverted.png")
        self.image = pygame.transform.smoothscale(self.original_sheet, (100, 100))
        self.rect = self.image.get_rect()
        self.hit_count = 0
        self.animation_time = 0
        self.current_time = 0
        self.velocity = 1  # Speed of enemy movement

        # Set initial position at the right end of the screen
        self.rect.x = 600
        self.rect.y = position[1]

    def update(self):
        # Move the miniboss leftward
        self.rect.x -= self.velocity

        # You can add conditions here to check if the miniboss has reached a certain point
        # or to change its velocity or direction if needed


class MainEnemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        # Load different images
        image1 = pygame.image.load("villian/mainvillain1final.png")
        image2 = pygame.image.load("villian/mainvillian2final.png")

        # Create subsurfaces from the loaded images
        frame1 = image1.subsurface(pygame.Rect(0, 0, 500, 500))
        frame2 = image2.subsurface(pygame.Rect(0, 0, 500, 500))

        # Scale the subsurfaces if necessary
        scaled_frame1 = pygame.transform.smoothscale(frame1, (200, 200))
        scaled_frame2 = pygame.transform.smoothscale(frame2, (200, 200))

        # Combine the frames into a list
        self.frames = [scaled_frame1, scaled_frame2]

        self.hit_count = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)

        self.frame = 0
        self.animation_time = 0
        self.current_time = 0
        self.velocity = 1
        self.moving_up = False
        self.isAlive = False
        self.shoot_duration = 4  # Time interval to shoot bullets (in seconds)
        self.shoot_cooldown = 7
        self.start_time = time.time()
        self.fire_mode = False
        self.fire_start_time = 0

    def spawn_mini_bosses(self):
        global mini_boss_group  # Access the global mini_boss_group
        # Create two new MiniBoss instances at the current position
        new_mini_boss1 = MiniBoss((self.rect.x, self.rect.y))
        mini_boss_group.add(new_mini_boss1)

    def animate(self):
        # Updating animation every 100 ms
        self.current_time += 0.9
        if self.current_time - self.animation_time > 100:
            self.animation_time = self.current_time
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0
            self.image = self.frames[self.frame]

    def move(self):
        if not self.fire_mode:
            if self.moving_up:
                self.rect.y += self.velocity
                if self.rect.y >= 375:
                    self.moving_up = False
            else:
                self.rect.y -= self.velocity
                if self.rect.y <= 75:
                    self.moving_up = True
            if time.time() - self.start_time > self.shoot_cooldown:
                self.fire_mode = True
                self.fire_start_time = time.time()

    def update(self):
        if self.fire_mode:
            self.animate()  # Play the animation during the shooting phase
            if time.time() - self.fire_start_time > self.shoot_duration:
                self.fire_mode = False
                self.start_time = time.time()  # Reset the timer to continue movement
                self.spawn_mini_bosses()
        else:
            self.move()  # Continue with the movement


class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        self.original_sheet = pygame.image.load("virus.png")
        self.frames = [self.original_sheet.subsurface(pygame.Rect(0, 20, 160, 235)),
                       self.original_sheet.subsurface(pygame.Rect(160, 20, 160, 235)),
                       self.original_sheet.subsurface(pygame.Rect(320, 20, 160, 235))]
        self.frames = [pygame.transform.smoothscale(img, (80, 110)) for img in self.frames]

        self.hit_count = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)

        self.frame = 0
        self.animation_time = 0
        self.current_time = 0

        self.velocity = 1  # the speed if enemy is defined

    def animate(self):
        # Updating animation every 100 ms
        self.current_time += 1
        if self.current_time - self.animation_time > 10:
            self.animation_time = self.current_time
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0
            self.image = self.frames[self.frame]

    def update(self):
        self.animate()  # Updating the frame
        self.rect.x -= self.velocity  # Moving the enemy


# class Character(pygame.sprite.Sprite):
#     def __init__(self, position):
#         self.original_sheet = pygame.image.load("herorestposition.png")
#         self.image = pygame.transform.smoothscale(self.original_sheet, (100, 125))
#         self.rect = self.image.get_rect()
#
#         self.rect.topleft = position
#
#         self.max_y = 340  # Maximum y-coordinate the player can move to
#         self.min_y = 100
#
#     def update(self, direction):
#         current_x = self.rect.x
#         current_y = self.rect.y
#         if direction == 'left':
#             self.rect.x -= 20
#             self.rect.x = max(0, current_x - 20)
#         if direction == 'right':
#             self.rect.x += 20
#             self.rect.x = min(800 - self.rect.width, current_x + 20)
#
#         if direction == 'up':
#             self.rect.y = max(self.min_y, current_y - 60)  # Restricting movement within the specified range
#
#         if direction == 'down':
#             self.rect.y = min(self.max_y, current_y + 60)  # Restricting movement within the specified range
#
#     def handle_event(self, event):
#         if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_LEFT:
#                     self.update('left')
#                 if event.key == pygame.K_RIGHT:
#                     self.update('right')
#                 if event.key == pygame.K_UP:
#                     self.update('up')
#                 if event.key == pygame.K_DOWN:
#                     self.update('down')
#                 if event.key == pygame.K_SPACE:
#                     new_bullet = Bullet(self.rect.midright)
#                     bullet_group.add(new_bullet)
#
#         if event.type == pygame.KEYUP:
#             if event.key == pygame.K_LEFT:
#                 self.update('stand_left')
#             if event.key == pygame.K_RIGHT:
#                 self.update('stand_right')
class Character(pygame.sprite.Sprite):
    def __init__(self, position):

        # load image
        self.sheet = pygame.image.load("herocorrectsize.png")

        # defines area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 95, 205))

        # loads spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()

        # position image in the screen surface
        self.rect.topleft = position

        # variable for looping the frame sequence
        self.frame = 0

        self.rectWidth = 95
        self.rectHeight = 205
        self.max_y = 340  # Maximum y-coordinate the player can move to
        self.min_y = 100

        self.right_states = {
            0: (0, 0, self.rectWidth, self.rectHeight),
            1: (95, 0, self.rectWidth, self.rectHeight),
            2: (190, 0, self.rectWidth, self.rectHeight)
        }

        self.left_states = {
            0: (0, 0, self.rectWidth, self.rectHeight),
            1: (285, 0, self.rectWidth, self.rectHeight),
            2: (380, 0, self.rectWidth, self.rectHeight)

        }

    def get_frame(self, frame_set):
        # looping the sprite sequences.
        self.frame += 1

        # if loop index is higher that the size of the frame return to the first frame
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        # print(frame_set[self.frame])
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    # def update(self, direction):
    #     current_x = self.rect.x
    #     if direction == 'left':
    #         self.clip(self.left_states)
    #         # animate rect coordinates
    #         self.rect.x -= 5
    #         self.rect.x = max(0, current_x - 5)
    #     if direction == 'right':
    #         self.clip(self.right_states)
    #         self.rect.x += 5
    #         self.rect.x = min(800 - self.rect.width, current_x + 5)

    def update(self, direction):
        current_x = self.rect.x
        current_y = self.rect.y
        if direction == 'left':
            # self.rect.x -= 20
            # self.rect.x = max(0, current_x - 20)
            self.clip(self.right_states)
            self.rect.y = max(self.min_y, current_y - 60)  # Restricting movement within the specified range
        if direction == 'right':
            # self.rect.x += 20
            # self.rect.x = min(800 - self.rect.width, current_x + 20)
            self.clip(self.left_states)
            self.rect.y = min(self.max_y, current_y + 60)  # Restricting movement within the specified range

        if direction == 'stand_left':
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.clip(self.right_states[0])

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                self.update('left')
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_SPACE:
                new_bullet = Bullet(self.rect.midright)
                bullet_group.add(new_bullet)

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')


# character position
player = Character((170, 150))
enemy = Enemy(position=(750, 200))
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy)

main_villian = MainEnemy(position=(600, 200))

# mini_boss = MiniBoss(position=(0, 200))
mini_boss_group = pygame.sprite.Group()


# mini_boss_group.add(mini_boss)


def show_score():
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH - 200, 10))


def show_start_screen_text():
    text = font.render('Press SPACE to start the game', True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))


# Function to display the end game text
def show_end_game_text():
    text = font.render(f'GAME OVER! Your score is {score}.Press SPACE to restart', True, (255, 255, 255))
    screen.blit(text, (100, SCREEN_HEIGHT // 2))


def show_win_game_text():
    text = font.render(f'You Won! Your score is {score}.Press SPACE to restart', True, (255, 255, 255))
    screen.blit(text, (100, SCREEN_HEIGHT // 2))


def restart_game():
        global score, game_active, player, enemy, bullet_group, enemy_group, main_villian, mini_boss_group

        # Reset score and game state flags
        score = 0
        game_active = True
        show_end_screen = False
        show_win_screen = False

        # Reinitialize player
        player = Character((170, 150))

        # Reinitialize enemy
        enemy = Enemy(position=(750, 200))
        enemy_group = pygame.sprite.Group()
        enemy_group.add(enemy)

        # Reinitialize main villain
        main_villian = MainEnemy(position=(600, 200))
        main_villian.isAlive = False

        # Clear and reinitialize bullet group
        bullet_group = pygame.sprite.Group()

        # Clear and reinitialize mini-boss group
        mini_boss_group = pygame.sprite.Group()


run = True
while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if show_start_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    show_start_screen = False
        elif game_active:
            player.handle_event(event)
            main_villian.update()
        elif show_end_screen or show_win_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_game()

    screen.blit(background, (0, 0))  # Always draw the background

    if show_start_screen:
        show_start_screen_text()
    elif game_active:
        bullet_group.update()
        enemy_group.update()
        mini_boss_group.update()
        main_villian.update()

        for bullet in bullet_group:
            if pygame.sprite.collide_rect(bullet, enemy):
                bullet.kill()
                enemy.hit_count += 1
                if enemy.hit_count > 3:
                    enemy.kill()
                    score += 2  # Increase score
                    if score < 8:  # Generate new enemy if score is less than 20
                        enemy = Enemy(position=(750, random.choice([100, 200, 300, 400])))
                        enemy_group.add(enemy)

            if pygame.sprite.collide_rect(bullet, main_villian):
                bullet.kill()
                main_villian.hit_count += 1
                if main_villian.hit_count > 30:
                    main_villian.kill()
                    main_villian.isAlive = False
                    show_win_screen = True
                    game_active = False
                    score += 20

            collided_mini_bosses = pygame.sprite.spritecollide(bullet, mini_boss_group, False)
            if collided_mini_bosses:
                bullet.kill()  # Remove the bullet
                for mini_boss in collided_mini_bosses:
                    mini_boss.hit_count += 1
                    if mini_boss.hit_count > 2:  # Check if mini boss is defeated
                        mini_boss.kill()  # Remove the mini boss
                        score += 2  # Increase score

            if score >= 8 and not main_villian.isAlive:
                main_villian.isAlive = True

        for enemy in enemy_group:
            if enemy.rect.right < 230:
                game_active = False
                show_end_screen = True
                break

        for mini_boss in mini_boss_group:
            if mini_boss.rect.right < 230:
                game_active = False
                show_end_screen = True
                break

        bullet_group.draw(screen)
        screen.blit(player.image, player.rect)
        if main_villian.isAlive:
            screen.blit(main_villian.image, main_villian.rect)
            mini_boss_group.update()
            mini_boss_group.draw(screen)


        show_score()
        enemy_group.draw(screen)


    elif show_end_screen:
        show_end_game_text()
    elif show_win_screen:
        show_win_game_text()

    pygame.display.flip()

pygame.quit()
