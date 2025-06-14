import pygame
import random 

SCREEN_WIDTH, SCREEN_HIGHT = 500, 400
MOVEMENT_SPEED = 5
FONT_SIZE = 72

pygame.init()

score = 0

clock = pygame.time.Clock()

font = pygame.font.SysFont('Times New Roman', FONT_SIZE)

class Sprite(pygame.sprite.Sprite):
    def __init__(self,color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(pygame.Color('dodgerblue'))
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))
        self.rect = self.image.get_rect()


    def move(self, xchange, ychange):
        self.rect.x = max(0, min(self.rect.x + xchange,
                      SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y + ychange,
                      SCREEN_HIGHT - self.rect.height))


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
screen.fill('blue')
all_sprites = pygame.sprite.Group()
pygame.display.set_caption('Project')

sp1 = Sprite(pygame.Color('black'), 20, 30)
sp1.rect.x, sp1.rect.y = random.randint(0, SCREEN_WIDTH - sp1.rect.width), random.randint(0, SCREEN_HIGHT - sp1.rect.height)
all_sprites.add(sp1)

enemies = []
enemy_group = pygame.sprite.Group()
for _ in range(7):
    enemy = Sprite(pygame.Color('red'), 20, 30)
    enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.width)
    enemy.rect.y = random.randint(0, SCREEN_HIGHT - enemy.rect.height)
    enemies.append(enemy)
    enemy_group.add(enemy)

running, won = True, False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not won:
        keys = pygame.key.get_pressed()
        xchange = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * MOVEMENT_SPEED
        ychange = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * MOVEMENT_SPEED
        sp1.move(xchange, ychange)

        # Collision detection using colliderect
        for enemy in enemies[:]:
            if sp1.rect.colliderect(enemy.rect):
                enemies.remove(enemy)
                enemy_group.remove(enemy)  # Also remove from group!
                score += 1

        if score == 7:
            won = True

    # Clear screen every frame
    screen.fill(pygame.Color('blue'))

    # Draw sprites
    all_sprites.draw(screen)
    enemy_group.draw(screen)

    # Draw score
    score_text = font.render('Score : ' + str(score),
                             True, pygame.Color('black'))
    screen.blit(score_text, (10, 10))

    if won:
        win_text = font.render('You Won!', True, pygame.Color('black'))
        screen.blit(win_text, ((SCREEN_WIDTH - win_text.get_width()) //
                    2, (SCREEN_HIGHT - win_text.get_height()) // 2))

    pygame.display.flip()
    clock.tick(90)

pygame.quit()
