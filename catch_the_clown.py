import pygame, random, json

pygame.init()

# Set display surface
WINDOW_WIDTH = 945
WINDOW_HEIGHT = 600
CENTER_X = WINDOW_WIDTH // 2
CENTER_Y = WINDOW_HEIGHT // 2
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Catch the Clown")

# Set FPS and clockhttps://github.com/jefftmarks/clown_pygame.git
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_START_LIVES = 5
CLOWN_START_VELOCITY = 3
CLOWN_ACCELERATION = 0.5

score = 0
player_lives = PLAYER_START_LIVES

clown_velocity = CLOWN_START_VELOCITY
clown_dx = random.choice([-1, 1])
clown_dy = random.choice([-1, 1])

# Load colors
with open('COLORS.json') as f:
    COLORS = json.load(f)

# Set fonts
font = pygame.font.Font('assets/Franxurter.ttf', 32)

# Set text
title_txt = font.render("Catch the Clown", True, COLORS["BLUE"])
title_rect = title_txt.get_rect()
title_rect.topleft = (50, 10)

score_txt = font.render(f"Score: {str(score)}", True, COLORS["YELLOW"])
score_rect = score_txt.get_rect()
score_rect.topright = (WINDOW_WIDTH - 50, 10)

lives_txt = font.render(f"Lives: {str(player_lives)}", True, COLORS["YELLOW"])
lives_rect = lives_txt.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 50, 50)

game_over_txt = font.render("GAME OVER", True, COLORS["BLUE"], COLORS["YELLOW"])
game_over_rect = game_over_txt.get_rect()
game_over_rect.center = (CENTER_X, CENTER_Y)

continue_txt = font.render("Click anywhere to play again", True, COLORS["YELLOW"], COLORS["BLUE"])
continue_rect = continue_txt.get_rect()
continue_rect.center = (CENTER_X, CENTER_Y + 64)

# Set sound and music
click_sound = pygame.mixer.Sound('assets/click_sound.wav')
miss_sound = pygame.mixer.Sound('assets/miss_sound.wav')
pygame.mixer.music.load('assets/ctc_background_music.wav')

# Set images
bg_img = pygame.image.load('assets/background.png')
bg_rect = bg_img.get_rect()
bg_rect.topleft = (0, 0)

clown_img = pygame.image.load('assets/clown.png')
clown_rect = clown_img.get_rect()
clown_rect.center = (CENTER_X, CENTER_Y)

# Main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        # Player quits
        if event.type == pygame.QUIT:
           running = False 
        
        # Player clicks screen
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # The clown was clicked
            if clown_rect.collidepoint(mouse_x, mouse_y):
                click_sound.play()
                score += 1
                clown_velocity += CLOWN_ACCELERATION

                # Move clown in new direction
                prev_dx, prev_dy = clown_dx, clown_dy
                while((prev_dx, prev_dy) == (clown_dx, clown_dy)):
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])
            # Clown missed
            else:
                miss_sound.play()
                player_lives -= 1

    # Move the clown
    clown_rect.x += clown_dx * clown_velocity
    clown_rect.y += clown_dy * clown_velocity

    # Bounce the clown off edge of display
    if clown_rect.left <= 0 or clown_rect.right >= WINDOW_WIDTH:
        clown_dx = -1 * clown_dx
    if clown_rect.top <= 0 or clown_rect.bottom >= WINDOW_HEIGHT:
        clown_dy = -1 * clown_dy

    # Update HUD
    score_txt = font.render(f"Score: {str(score)}", True, COLORS["YELLOW"])
    lives_txt = font.render(f"Lives: {str(player_lives)}", True, COLORS["YELLOW"])

    # Check for game over
    if player_lives == 0:
        display_surface.blit(game_over_txt, game_over_rect)
        display_surface.blit(continue_txt, continue_rect)
        pygame.display.update()

        # Pause game untinl the player clicks
        pygame.mixer.music.stop()
        paused = True
        while paused:
            for event in pygame.event.get():
                # Player wants to play again
                if event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_START_LIVES

                    clown_rect.center = (CENTER_X, CENTER_Y)
                    clown_velocity = CLOWN_START_VELOCITY
                    clown_dx = random.choice([-1, 1])
                    clown_dy = random.choice([-1, 1])

                    pygame.mixer.music.play(-1, 0.0)

                    paused = False
                # Player quits
                if event.type == pygame.QUIT:
                    paused = False
                    running = False

    # Blit background
    display_surface.blit(bg_img, bg_rect)
    
    # Blit HUD
    display_surface.blit(title_txt, title_rect)
    display_surface.blit(score_txt, score_rect)
    display_surface.blit(lives_txt, lives_rect)

    # Blit assets
    display_surface.blit(clown_img, clown_rect)

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
