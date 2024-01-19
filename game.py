import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load player run animation frames
        player_run_1 = pygame.image.load('graphics/player/player_run_1.png').convert_alpha()
        player_run_2 = pygame.image.load('graphics/player/player_run_2.png').convert_alpha()
        self.player_run = [player_run_1, player_run_2]
        
        # Initialize player properties
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/player_jump.png').convert_alpha()

        self.image = self.player_run[self.player_index]

        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        # Load jump sound
        self.jump_sound = pygame.mixer.Sound('audio/jump_02.wav')
        self.jump_sound.set_volume(0.5)


    def player_action(self):
         # Check for key presses (SPACE) to trigger player jump
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        # Apply gravity to player, restricting to a lower boundary
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300: self.rect.bottom = 300

    def update(self):
        # Update player actions, gravity, and animation state
        self.player_action()
        self.apply_gravity()
        self.animation_state()
    
    def animation_state(self):
        # Update player animation based on jump state
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            # Cycle through run animation frames
            self.player_index += 0.1
            if self.player_index >= len(self.player_run): self.player_index = 0
            self.image = self.player_run[int(self.player_index)]
    
class Enemy(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        # Load enemy frames based on type (bee or mouse)
        if type == 'bee':
            bee_1 = pygame.image.load('graphics/bee/bee_1.png').convert_alpha()
            bee_2 = pygame.image.load('graphics/bee/bee_2.png').convert_alpha()
            self.frames = [bee_1, bee_2]
            y_pos = 190
        else:
            mouse_1 = pygame.image.load('graphics/mouse/mouse_1.png').convert_alpha()
            mouse_2 = pygame.image.load('graphics/mouse/mouse_2.png').convert_alpha()
            self.frames = [mouse_1, mouse_2]
            y_pos = 300
            
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        # Update enemy animation state
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        # Update enemy animation, position, and check for destruction
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
    
    def destroy(self):
        # Destroy enemy if off-screen
        if self.rect.x <= -100:
            self.kill()

# Display and return the current game score
def print_score():
    curr_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {curr_time}', False,(64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return curr_time

# Check for collisions between player and enemies
def collision_sprite():
	if pygame.sprite.spritecollide(player.sprite, enemy_group,False):
		enemy_group.empty()
		return False
	else: return True


# Initialize Pygame
pygame.init()

# Set up game window
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Harvest-Hex')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)

# Game state variables
game_active = False
start_time = 0
score = 0

# Background music
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)


# Create player group
player = pygame.sprite.GroupSingle()
player.add(Player())

# Create enemy group
enemy_group = pygame.sprite.Group()


# Load sky and ground surfaces
sky_surface = pygame.image.load('graphics/near-background.png').convert() # converts image to sth pygame can work with more easily
ground_surface = pygame.image.load('graphics/ground.png').convert()

# Load intro screen elements
player_stand = pygame.image.load('graphics/player/player_stand.png')
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))


game_title = test_font.render('Harvest-Hex',False,(110, 186, 149))
game_title_rect = game_title.get_rect(center = (400, 80))

game_text = test_font.render('Press Space to Start', False, (110, 186, 149))
game_text_rect = game_text.get_rect(center = (400, 330))

# Set up game timer for enemy characters
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer,1500)


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # If the game is active, spawn enemies based on timer
        if game_active:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(choice(['bee', 'mouse', 'bee', 'mouse'])))
		
        # If the game is not active, start the game on SPACE key press
        else:
             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    # Update and draw game elements during active gameplay
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = print_score()

        player.draw(screen)
        player.update()

        enemy_group.draw(screen)
        enemy_group.update()

        game_active = collision_sprite()
    # Display intro screen and score information when not in active gameplay
    else:
        screen.fill((84, 119, 132))
        screen.blit(player_stand, player_stand_rect)
        
        score_text = test_font.render(f'Your score: {score}', False,(110, 186, 149))
        score_text_rect = score_text.get_rect(center = (400, 330))
        screen.blit(game_title, game_title_rect)
        
        if score == 0: screen.blit(game_text, game_text_rect)
        else: screen.blit(score_text, score_text_rect)

    pygame.display.update()
    clock.tick(60)
