import pygame
import player

pygame.init()

clock = pygame.time.Clock()

FPS = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Protect the family")

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((20, 10))  # Create a surface for the bullet
        self.image.fill(("#009df2"))  # Fill the bullet with red color for visibility
        self.rect = self.image.get_rect(center=position)

    def update(self):
        self.rect.x += 10  # Moves the bullet to the right by 10 pixels
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):

        self.original_sheet = pygame.image.load("virus.png")
        self.frames = [self.original_sheet.subsurface(pygame.Rect(0, 20, 160, 235)),
                       self.original_sheet.subsurface(pygame.Rect(160, 20, 160, 235)),
                       self.original_sheet.subsurface(pygame.Rect(320, 20, 160, 235))]
        self.frames = [pygame.transform.smoothscale(img, (80, 110)) for img in self.frames]

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=position)

        self.frame = 0
        self.animation_time = 0
        self.current_time = 0

        self.velocity = 1  # Define the speed of the movement

    def animate(self):
        # Update animation every 100 ms
        self.current_time += 1
        if self.current_time - self.animation_time > 10:
            self.animation_time = self.current_time
            self.frame += 1
            if self.frame >= len(self.frames):
                self.frame = 0
            self.image = self.frames[self.frame]

    def update(self):
        self.animate()  # Update the frame
        self.rect.x -= self.velocity  # Move the enemy
        if self.rect.right < 230:
            self.rect.left = SCREEN_WIDTH
class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        self.original_sheet = pygame.image.load("hero.png")
        self.image = pygame.transform.smoothscale(self.original_sheet, (100, 125))
        self.rect = self.image.get_rect()  # Use the scaled image directly

        # position image on the screen surface
        self.rect.topleft = position

        self.max_y = 340  # Maximum y-coordinate the player can move to
        self.min_y = 100


        # self.original_sheet = pygame.image.load("virus.png")
        # self.sheet.set_clip(pygame.Rect(0, 20, 160, 235))
        #
        # # loads spritesheet images
        # self.image = self.sheet.subsurface(self.sheet.get_clip())
        # self.rect = self.image.get_rect()
        #
        # # position image in the screen surface
        # self.rect.topleft = position
        #
        # # variable for looping the frame sequence
        # self.frame = 0
        #
        # self.rectWidth = 160
        # self.rectHeight = 235
        #
        # self.right_states = {
        #     1: (0, 20, self.rectWidth, self.rectHeight),
        #     2: (160, 20, self.rectWidth, self.rectHeight),
        #     3: (320, 20, self.rectWidth, self.rectHeight)}



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
            self.rect.y = max(self.min_y, current_y - 60)  # Restrict movement within the specified range

        if direction == 'down':
            self.rect.y = min(self.max_y, current_y + 60)  # Restrict movement within the specified range

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

#character position
player = Character((170, 150))
enemy = Enemy(position=(750, 200))
bullet_group = pygame.sprite.Group()

run = True
while run:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        player.handle_event(event)

    # Update
    bullet_group.update()  # This updates the position of the bullets every frame
    enemy.update()

    # Draw everything
    screen.blit(background, (0, 0))  # Draw the background
    bullet_group.draw(screen)  # Draw all the bullets
    screen.blit(player.image, player.rect)  # Draw the player
    screen.blit(enemy.image, enemy.rect)

    # Update the display
    pygame.display.flip()

pygame.quit()
