# the creator of the code below is Aaditey Nair, thanks to this peer for sharing his works.

import time
import pygame
from sys import exit

BLACK = (5, 0, 43)
WHITE = (255, 255, 255)

PLAYER_VELOCITY = 4

WIDTH = 840
HEIGHT = 540

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")

# laser = pygame.mixer.Sound("assets/laser.mp3")
# explosion = pygame.mixer.Sound("assets/hit.mp3")

font = pygame.font.Font("assets/Pixeltype.ttf", 72)
small_font = pygame.font.Font("assets/Pixeltype.ttf", 24)

player_img = pygame.image.load("assets/player.png").convert_alpha()
player = pygame.transform.rotozoom(player_img, 180, 0.15)
player_rect = player.get_rect(midbottom=(420, 500))

intro_text = font.render("Space Invaders", False, WHITE)
intro_text_rect = intro_text.get_rect(center=(WIDTH / 2, HEIGHT / 2))

instruction_text = small_font.render("Press Space to Start", False, WHITE)
instruction_text_rect = instruction_text.get_rect(midtop=intro_text_rect.midbottom)

end_message_win = font.render("You Win!", False, WHITE)
end_message_win_rect = end_message_win.get_rect(center=(WIDTH / 2, HEIGHT / 2))

end_message_lose = font.render("You Lose!", False, WHITE)
end_message_lose_rect = end_message_lose.get_rect(center=(WIDTH / 2, HEIGHT / 2))

end_instructions = small_font.render("Press 'R' to restart or 'Q' to exit", False, WHITE)
end_instructions_rect = end_instructions.get_rect(midtop=end_message_win_rect.midbottom)

enemy = pygame.image.load("assets/enemy.png").convert_alpha()
enemy = pygame.transform.rotozoom(enemy, 180, 0.09)
enemies = []

bullet = pygame.surface.Surface((5, 15))
bullet.fill(WHITE)
bullets = []


def initialize_enemies():
    for i in range(3):
        for j in range(10):
            enemy_rect = enemy.get_rect(midtop=(100 + j * 60, i * 60))
            enemy_rect.centerx += 50
            enemies.append(enemy_rect)


def main():
    global enemies

    go_left = True
    running = False
    won = "undefined"

    initialize_enemies()

    enemy_group_width = (WIDTH - enemies[0].left) - (WIDTH - enemies[-1].right)
    enemy_group = pygame.rect.Rect(enemies[0].left, 0, enemy_group_width, 160)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not running:
                    running = True
                if not enemies:
                    if event.key == pygame.K_r:
                        main()
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

        screen.fill(BLACK)
        if running:
            screen.blit(player, player_rect)

            enemy_down_velocity = 0

            if enemies:
                keys = pygame.key.get_pressed()

                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    if player_rect.right < 840:
                        player_rect.x += PLAYER_VELOCITY

                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    if player_rect.left > 0:
                        player_rect.x -= PLAYER_VELOCITY

                if keys[pygame.K_SPACE]:
                    if not bullets:
                        bullets.append(bullet.get_rect(midbottom=(player_rect.centerx, player_rect.top - 25)))
                        # laser.play()

                if enemy_group.left >= 0 and go_left:
                    enemy_velocity = PLAYER_VELOCITY
                    if enemy_group.left < 4:
                        enemy_down_velocity = 10
                else:
                    go_left = enemy_group.right > WIDTH
                    enemy_velocity = -PLAYER_VELOCITY
                    if go_left:
                        enemy_down_velocity = 10

                for enemy_rect in enemies:
                    enemy_rect.x -= enemy_velocity
                    enemy_rect.bottom += enemy_down_velocity
                    screen.blit(enemy, enemy_rect)
                enemy_group.x -= enemy_velocity
                enemy_group.bottom += enemy_down_velocity

                if enemies[-1].bottom > player_rect.top:
                    # explosion.play()
                    won = False
                    enemies = []

                for bullet_rect in bullets:
                    bullet_rect.y -= 10
                    if bullet_rect.top < 0:
                        bullets.remove(bullet_rect)
                        continue

                    for enemy_rect in enemies:
                        if bullet_rect.colliderect(enemy_rect):
                            enemies.remove(enemy_rect)
                            bullets.remove(bullet_rect)
                            # explosion.play()
                            break

                    screen.blit(bullet, bullet_rect)
            else:
                if won == "undefined":
                    won = True

            if won != "undefined":
                screen.fill(BLACK)
                if won:
                    screen.blit(end_message_win, end_message_win_rect)
                    screen.blit(end_instructions, end_instructions_rect)
                else:
                    screen.blit(end_message_lose, end_message_lose_rect)
                    screen.blit(end_instructions, end_instructions_rect)

        else:
            screen.blit(intro_text, intro_text_rect)
            screen.blit(instruction_text, instruction_text_rect)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()