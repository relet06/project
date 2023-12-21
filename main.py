import pygame
import time
import random
pygame.font.init()

# window settings
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stars")
BG = pygame.transform.scale(pygame.image.load("images/joseph-r-tlP3nrAQ4n0-unsplash.jpg"), (WIDTH, HEIGHT))
PLAYER_WIDTH = 10
PLAYER_HEIGHT = 60
PLAYER_VEL = 10
FONT = pygame.font.SysFont("comicsans", 30)
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3
ACCELERATED_STAR_VEL = 5
last_speed_change = pygame.time.get_ticks()
accelerated = False
wait_timer = True
wait_timer2 = False
def draw(player, elapsed_time, stars):
    global wait_timer
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, " white")
    left_text = FONT.render(f"Move left: ARROW LEFT", 1, "white")
    right_text = FONT.render(f"Move right: ARROW RIGHT", 1, "white")
    # TIPS RENDER
    if wait_timer:
        WIN.blit(left_text, (WIDTH/2 - left_text.get_width()/2, HEIGHT/2 - left_text.get_width()/2))
        WIN.blit(right_text, (WIDTH/2 - right_text.get_width()/2, HEIGHT/2 + 50 - right_text.get_width()/2))
    if elapsed_time >= 3:
        wait_timer = False
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "red", player)
    for star in stars:
        pygame.draw.rect(WIN, "white", star)
    pygame.display.update()

# main function
def main():
    acceleration_interval = random.randint(1500, 3000)
    acceleration_amount = 1
    time_since_acceleration = 0
    max_stars = 50
    global STAR_VEL, last_speed_change, accelerated, wait_timer2
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    star_count = 0
    stars = []
    hit = False
    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # stars speed up
        time_since_acceleration += clock.tick(60)
        if time_since_acceleration >= acceleration_interval:
            STAR_VEL += acceleration_amount
            time_since_acceleration = 0
        if elapsed_time >= 3:
            wait_timer2 = True
        if wait_timer2:
            # coming stars
            current_star_count = len(stars)
            if current_star_count < max_stars:
                for _ in range(max_stars - current_star_count):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player.x + player.width <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL


        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_width()/2))
            pygame.display.update()
            pygame.time.delay(1000)
            break
        draw(player, elapsed_time, stars)
    pygame.quit()

main()

