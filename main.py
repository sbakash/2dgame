import pygame
import random
import player

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
show_start_screen =True
game_active = False
show_end_screen= False

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


class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        self.original_sheet = pygame.image.load("hero.png")
        self.image = pygame.transform.smoothscale(self.original_sheet, (100, 125))
        self.rect = self.image.get_rect()

        self.rect.topleft = position

        self.max_y = 340  # Maximum y-coordinate the player can move to
        self.min_y = 100

    def update(self, direction):
        current_x = self.rect.x
        current_y = self.rect.y
        if direction == 'left':
            self.rect.x -= 20
            self.rect.x = max(0, current_x - 20)
        if direction == 'right':
            self.rect.x += 20
            self.rect.x = min(800 - self.rect.width, current_x + 20)

        if direction == 'up':
            self.rect.y = max(self.min_y, current_y - 60)  # Restricting movement within the specified range

        if direction == 'down':
            self.rect.y = min(self.max_y, current_y + 60)  # Restricting movement within the specified range

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.update('left')
                if event.key == pygame.K_RIGHT:
                    self.update('right')
                if event.key == pygame.K_UP:
                    self.update('up')
                if event.key == pygame.K_DOWN:
                    self.update('down')
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


def restart_game():
    global score, game_active, player, enemy, bullet_group, enemy_group
    score = 0
    game_active = True

    player = Character((170, 150))
    enemy = Enemy(position=(750, 200))
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    enemy_group.add(enemy)

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
        elif show_end_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_game()

    screen.blit(background, (0, 0))  # Always draw the background

    if show_start_screen:
        show_start_screen_text()
    elif game_active:
        bullet_group.update()
        enemy_group.update()

        for bullet in bullet_group:
            if pygame.sprite.collide_rect(bullet, enemy):
                bullet.kill()
                enemy.hit_count += 1
                if enemy.hit_count > 3:
                    enemy.kill()
                    enemy = Enemy(position=(750, random.choice([100, 200, 300, 400])))
                    enemy_group.add(enemy)
                    score += 1

        for enemy in enemy_group:
            if enemy.rect.right < 230:
                game_active = False
                show_end_screen = True
                break

        bullet_group.draw(screen)
        screen.blit(player.image, player.rect)
        show_score()
        enemy_group.draw(screen)
    elif show_end_screen:
        show_end_game_text()

    pygame.display.flip()

pygame.quit()
