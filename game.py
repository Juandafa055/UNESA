import pygame
import sys
import os

pygame.init()


WIDTH = 800
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME UTS SEDERHANA SAJA")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 80, 80)
GREEN = (0, 200, 100)
BROWN = (139, 69, 19)
GRAY = (180, 180, 180)
SKY = (135, 206, 235)

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()


base_dir = os.path.dirname(__file__)
image_dir = os.path.join(base_dir, "IMAGE")


player_img = pygame.image.load(os.path.join(image_dir, "player.png"))
player_img = pygame.transform.scale(player_img, (40, 50))

enemy_img = pygame.image.load(os.path.join(image_dir, "enemy.png"))
enemy_img = pygame.transform.scale(enemy_img, (40, 30))

finish_img = pygame.image.load(os.path.join(image_dir, "finish.png"))
finish_img = pygame.transform.scale(finish_img, (50, 50))



class GameObject:
    def __init__(self, x, y, width, height, color, image=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.image = image

    def draw(self, surface):
        if self.image is not None:
            surface.blit(self.image, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)



class Character(GameObject):
    def __init__(self, x, y, width, height, color, image=None):
        super().__init__(x, y, width, height, color, image)
        self.vel_y = 0
        self.speed = 5
        self.on_ground = False

    def gravity(self):
        self.vel_y += 0.5
        self.rect.y += self.vel_y

    def jump(self):
        if self.on_ground:
            self.vel_y = -10
            self.on_ground = False


class Player(Character):
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed


class Enemy(Character):
    def __init__(self, x, y, width, height, color, left_bound, right_bound, image=None):
        super().__init__(x, y, width, height, color, image)
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.direction = 1
        self.speed = 1

    def move(self):
        self.rect.x += self.speed * self.direction

        if self.rect.x <= self.left_bound:
            self.direction = 1
        if self.rect.x + self.rect.width >= self.right_bound:
            self.direction = -1


class Platform(GameObject):
    pass


class Goal(GameObject):
    pass


def draw_background():
    screen.fill(SKY)

    pygame.draw.circle(screen, (255, 220, 0), (700, 80), 35)

  
    pygame.draw.rect(screen, (80, 200, 120), (0, 430, 800, 70))
    pygame.draw.rect(screen, (100, 170, 70), (0, 445, 800, 55))


def reset_game():
    player = Player(50, 380, 40, 50, BLUE, player_img)

    platforms = [
        Platform(0, 450, 800, 50, BROWN),
        Platform(120, 360, 120, 20, GRAY),
        Platform(300, 300, 120, 20, GRAY),
        Platform(500, 240, 120, 20, GRAY),
        Platform(650, 180, 100, 20, GRAY)
    ]

    enemy = Enemy(320, 270, 40, 30, RED, 300, 420, enemy_img)
    goal = Goal(700, 130, 50, 50, GREEN, finish_img)

    return player, platforms, enemy, goal


player, platforms, enemy, goal = reset_game()

game_over = False
win = False
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over and not win:
                if event.key == pygame.K_SPACE:
                    player.jump()

            if game_over or win:
                if event.key == pygame.K_b:
                    player, platforms, enemy, goal = reset_game()
                    game_over = False
                    win = False

    keys = pygame.key.get_pressed()

    if not game_over and not win:
        player.move(keys)

        if player.rect.x < 0:
            player.rect.x = 0
        if player.rect.x + player.rect.width > WIDTH:
            player.rect.x = WIDTH - player.rect.width

        player.gravity()
        player.on_ground = False

        for platform in platforms:
            if player.rect.colliderect(platform.rect):
                if player.vel_y > 0 and player.rect.bottom <= platform.rect.bottom:
                    player.rect.bottom = platform.rect.top
                    player.vel_y = 0
                    player.on_ground = True

        if player.rect.y > HEIGHT:
            game_over = True

        enemy.move()

        if player.rect.colliderect(enemy.rect):
            game_over = True

        if player.rect.colliderect(goal.rect):
            win = True

    draw_background()

    for platform in platforms:
        platform.draw(screen)

    goal.draw(screen)
    enemy.draw(screen)
    player.draw(screen)

    if game_over:
        text = font.render("GAME OVER", True, RED)
        text2 = small_font.render("KAMU KALAH, TEKAN B UNTUK MAIN LAGI", True, BLACK)
        screen.blit(text, (300, 200))
        screen.blit(text2, (310, 250))

    if win:
        text = font.render("KAMU MENANG", True, GREEN)
        text2 = small_font.render("KAMU MENANG, TEKAN B UNTUK MAIN LAGI", True, BLACK)
        screen.blit(text, (280, 200))
        screen.blit(text2, (280, 250))

    pygame.display.update()

pygame.quit()
sys.exit()