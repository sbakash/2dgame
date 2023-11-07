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
        self.rect.x += 10  # Move the bullet to the right by 10 pixels
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        self.original_sheet = pygame.image.load("hero.png")
        self.image = pygame.transform.smoothscale(self.original_sheet, (100, 125))
        self.rect = self.image.get_rect()  # Use the scaled image directly

        # position image on the screen surface
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

    # Draw everything
    screen.blit(background, (0, 0))  # Draw the background
    bullet_group.draw(screen)  # Draw all the bullets
    screen.blit(player.image, player.rect)  # Draw the player

    # Update the display
    pygame.display.flip()

pygame.quit()
