import json
import sys
import pygame
import random
import time
# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 790
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gravity Collector")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HOME_BUTTON = None
# Load images
background = pygame.image.load("bg2.webp").convert()
astronaut_img = pygame.image.load("astronaut-svgrepo-com.svg").convert_alpha()
coin_img = pygame.image.load("coin-svgrepo-com.svg").convert_alpha()

# Scale images
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
astronaut_img = pygame.transform.scale(astronaut_img, (50, 50))
coin_img = pygame.transform.scale(coin_img, (30, 30))

# Load level data
with open("level.json", "r") as f:
    level_data = json.load(f)

# Game variables
clock = pygame.time.Clock()
FPS = 60

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.is_hovered = False
        self.original_rect = self.rect.copy()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class Astronaut(pygame.sprite.Sprite):
    def __init__(self, x, y, weight):
        super().__init__()
        self.image = astronaut_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.jumping = False
        self.weight = weight
        self.weight_factor = weight / 70  # Assuming 70kg as a baseline

    def jump(self, gravity):
        if not self.jumping:
            self.velocity_y = -9 * (1 / gravity) / self.weight_factor  # Adjusted jump strength
            self.jumping = True

    def move_left(self):
        self.velocity_x = -5 / self.weight_factor

    def move_right(self):
        self.velocity_x = 5 / self.weight_factor

    def update(self, gravity):
        self.velocity_y += gravity * 0.5 * self.weight_factor
        self.rect.y += self.velocity_y
        self.rect.x += self.velocity_x

        # Keep astronaut within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.jumping = False
            self.velocity_y = 0
            
    def stop(self):
        self.velocity_x = 0
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def create_home_button():
    global HOME_BUTTON
    HOME_BUTTON = Button(10, 10, 100, 40, "Home", (100, 100, 100), WHITE)

def planet_selection():
    button_width = 200
    button_height = 50
    gap = 30
    columns = 2
    rows = 4
    total_width = (button_width * columns) + (gap * (columns - 1))
    total_height = (button_height * rows) + (gap * (rows - 1))
    start_x = (SCREEN_WIDTH - total_width) // 2
    start_y = (SCREEN_HEIGHT - total_height) // 2

    planets_buttons = [
        Button(start_x, start_y, button_width, button_height, "Mercury", (169, 169, 169), BLACK),
        Button(start_x + button_width + gap, start_y, button_width, button_height, "Venus", (255, 198, 73), BLACK),
        Button(start_x, start_y + button_height + gap, button_width, button_height, "Earth", (0, 255, 0), BLACK),
        Button(start_x + button_width + gap, start_y + button_height + gap, button_width, button_height, "Mars", (255, 0, 0), BLACK),
        Button(start_x, start_y + (button_height + gap) * 2, button_width, button_height, "Jupiter", (255, 140, 0), BLACK),
        Button(start_x + button_width + gap, start_y + (button_height + gap) * 2, button_width, button_height, "Saturn", (238, 232, 170), BLACK),
        Button(start_x, start_y + (button_height + gap) * 3, button_width, button_height, "Uranus", (173, 216, 230), BLACK),
        Button(start_x + button_width + gap, start_y + (button_height + gap) * 3, button_width, button_height, "Neptune", (0, 0, 255), BLACK),
    ]
    
    font = pygame.font.Font(None, 48)
    title_text = font.render("Choose the Correct Gravity !!!", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(planets_buttons)):
                    if planets_buttons[i].is_clicked(pygame.mouse.get_pos()):
                        return i # Return the index of the selected planet
        
        screen.blit(background,(0 ,0))
        
        screen.blit(title_text, title_rect)

        for button in planets_buttons:
            button.draw(screen)
        
        pygame.display.flip()

def get_player_weight():
    font = pygame.font.Font(None, 36)
    input_box = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('BLACK')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        try:
                            weight = float(text)
                            if 30 <= weight <= 200:  # Reasonable weight range in kg
                                return weight
                            else:
                                text = ''
                        except ValueError:
                            text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.blit(background, (0, 0))
        txt_surface = font.render(text, True, BLACK)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        prompt = font.render("Enter your weight in kg (30-200):", True, WHITE)
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 60))

        pygame.display.flip()
        clock.tick(30)

def load_level(level_number,player_weight):
    global current_level
    
    current_level_data = level_data[level_number]
    
    all_sprites = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()
    
    astronaut = Astronaut(50, SCREEN_HEIGHT - 100, player_weight)
    all_sprites.add(astronaut)

    # Get the collectibles data for this level
    collectibles_data = current_level_data.get("collectibles", [])

    # Generate random positions for collectibles
    for _ in range(len(collectibles_data)):
        x = random.randint(50, SCREEN_WIDTH - 50)  # 50 px margin on each side
        y = random.randint(180, SCREEN_HEIGHT - 100)  # 50 px from top, 150 px from bottom
        new_collectible = Collectible(x, y)
        all_sprites.add(new_collectible)
        collectibles.add(new_collectible)

    return astronaut, all_sprites, collectibles, time.time()

def game_over_screen(weight, planet, gravity, score):
    font = pygame.font.Font(None, 36)
    title = font.render("Game Over", True, WHITE)
    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))

    home_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT - 100, 100, 50, "Home", (255, 0, 0), WHITE)
    results_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT - 100, 100, 50, "Results", (0, 255, 0), WHITE)

    results_text = [
        f"Weight: {weight} kg",
        f"Planet: {planet}",
        f"Gravity: {gravity:.2f} m/s²",
        f"Score: {score}"
    ]

    show_results = False

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if home_button.is_clicked(mouse_pos):
                    return "home"
                if results_button.is_clicked(mouse_pos):
                    show_results = not show_results

        screen.blit(background, (0, 0))
        screen.blit(title, title_rect)

        home_button.draw(screen)
        results_button.draw(screen)

        if show_results:
            for i, text in enumerate(results_text):
                rendered_text = font.render(text, True, WHITE)
                screen.blit(rendered_text, (SCREEN_WIDTH // 2 - 100, 200 + i * 40))

        pygame.display.flip()
        clock.tick(60)

def confirm_quit():
    confirm_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    confirm_screen.set_alpha(200)
    confirm_screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 36)
    text = font.render("Are you sure you want to quit?", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))

    yes_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20, 100, 50, "Yes", (255, 0, 0), WHITE)
    no_button = Button(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 + 20, 100, 50, "No", (0, 255, 0), WHITE)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_button.is_clicked(mouse_pos):
                    return True
                if no_button.is_clicked(mouse_pos):
                    return False

        screen.blit(confirm_screen, (0, 0))
        screen.blit(text, text_rect)
        
        yes_button.draw(screen)
        no_button.draw(screen)

        pygame.display.flip()
        
def get_planet_info(index):
    planets = [
        ("Mercury", 3.7),
        ("Venus", 8.87),
        ("Earth", 9.81),
        ("Mars", 3.721),
        ("Jupiter", 24.79),
        ("Saturn", 10.44),
        ("Uranus", 8.69),
        ("Neptune", 11.15)
    ]
    return planets[index]

      
def main():
    global current_level
    global level_data
    global HOME_BUTTON
    
    player_weight = get_player_weight()
    
    while True:
        selected_planet_index = planet_selection()
        create_home_button()
        
        # Set gravity based on selected planet
        if selected_planet_index == 0:  # Mercury
            gravity = 0.50
        elif selected_planet_index == 1:  # Venus
            gravity = 0.704
        elif selected_planet_index == 2:  # Earth
            gravity = 0.8
        elif selected_planet_index == 3:  # Mars
            gravity = 0.58
        elif selected_planet_index == 4:  # Jupiter
            gravity = 2.328
        elif selected_planet_index == 5:  # Saturn
            gravity = 0.89
        elif selected_planet_index == 6:  # Uranus
            gravity = 0.668
        elif selected_planet_index == 7:  # Neptune
            gravity = 1.137
        
        planet_name, planet_gravity = get_planet_info(selected_planet_index)
        
        # Load levels based on selected planet's gravity values.
        level_data_with_gravity_adjustment = []
        
        for level in level_data:
            level["gravity"] *= gravity 
            level_data_with_gravity_adjustment.append(level)
        
        level_data = level_data_with_gravity_adjustment
        
        current_level = 0
        astronaut, all_sprites, collectibles, _ = load_level(current_level, player_weight)
        
        score = 0 
        game_duration = 60  # 60 seconds per level, for all levels
        start_time = time.time()
        
        running = True
        
        while running:
            current_time = time.time()
            elapsed_time = current_time - start_time
            remaining_time = max(0, game_duration - elapsed_time)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if confirm_quit():
                        running = False
                    continue
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if confirm_quit():
                            pygame.quit()
                            sys.exit()
                        continue
                    if event.key == pygame.K_SPACE:
                        astronaut.jump(gravity)
                    elif event.key == pygame.K_LEFT:
                        astronaut.move_left()
                    elif event.key == pygame.K_RIGHT:
                        astronaut.move_right()
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        astronaut.stop()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if HOME_BUTTON.is_clicked(pygame.mouse.get_pos()):
                        running = False
            
            if remaining_time == 0:
                game_over_result = game_over_screen(player_weight, planet_name, planet_gravity, score)
                if game_over_result == "home":
                    break
                else:  # "results" - continue showing the game over screen
                    continue
            
            all_sprites.update(gravity)
            
            # Check for coin collection 
            collected_coins = pygame.sprite.spritecollide(astronaut, collectibles, True)
            score += len(collected_coins)

            # Check for level completion 
            if len(collectibles) == 0:
                current_level += 1
            
                if current_level < len(level_data):
                    astronaut, all_sprites, collectibles, _ = load_level(current_level, player_weight)
                else:
                    game_over_result = game_over_screen(player_weight, planet_name, planet_gravity, score)
                    if game_over_result == "home":
                        break
                    else:  # "results" - continue showing the game over screen
                        continue
        
            # Draw everything 
            screen.blit(background, (0, 0))
        
            all_sprites.draw(screen)
            
            # Display score, level info, and timer
            font = pygame.font.Font(None, 36)
        
            score_text = font.render(f"Score: {score}", True, WHITE)
            level_text = font.render(f"Level: {current_level + 1}", True, WHITE)
            timer_text = font.render(f"Time: {int(remaining_time)}s", True, WHITE)
        
            screen.blit(score_text, (SCREEN_WIDTH - 120, 10))
            screen.blit(level_text, (SCREEN_WIDTH - 120, 50))
            screen.blit(timer_text, (SCREEN_WIDTH - 120, 90))
            
            HOME_BUTTON.draw(screen)
            
            pygame.display.flip()
            clock.tick(FPS) 
        
if __name__ == "__main__": 
    main()