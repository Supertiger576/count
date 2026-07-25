import pygame
import sys
import random 
import math

pygame.init()

# Set up window
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Escape")

# funny booleans
dontmove = False
screen_right = screen_left = screen_up = screen_down = False
firsttime = True

# Clock stuff
clock = pygame.time.Clock()
timer = 120
restart_factor = 0

# player setup
player_size = 40
player_speed = 5
player_rect = pygame.Rect(screen_width // 2, screen_height // 2, player_size, player_size)

def make_npc_rect(width_position, height_position, npc_width, npc_height):
    return pygame.Rect(width_position, height_position, npc_width, npc_height)
# NPC setup
npc_rect = make_npc_rect(screen_width // 2, screen_height // 2 - screen_height // 4, player_size, player_size)

# Load player and NPC image (same for now)
player_image = pygame.image.load(r"player_image").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

npc_image = pygame.image.load(r"funny_puffin.gif").convert_alpha()
npc_image = pygame.transform.scale(npc_image, (player_size, player_size))

# visible flags
player_visible = True
npc_visible = True

# Font & dialogue box setup
font = pygame.font.SysFont("Arial", 32)
dialogue_box = pygame.Surface((screen_width - 100, 80), pygame.SRCALPHA)
dialogue_box.fill((0, 0, 0, 180))  # semi-transparent black box

# list 
npc_list = [npc_rect]
npc_visible_list = [npc_visible]
alltextboxes = [False for x in npc_list]

# puzzle dict
puzzles = [{"direction":"right"}, {"direction":"left"}, {"direction":"down"}, {"direction":"up"}]
# puzzle flags
current_direction = "right"
level = 1
current_level = -1
random.shuffle(puzzles)


# functions
# detect if next movement will collide with other rect
def one_move_from_collision(player_rect, npc_rect, speed):
    return {
        "up": player_rect.move(0, -speed).colliderect(npc_rect),
        "down": player_rect.move(0, speed).colliderect(npc_rect),
        "left": player_rect.move(-speed, 0).colliderect(npc_rect),
        "right": player_rect.move(speed, 0).colliderect(npc_rect)
    }
# make textboxes
def make_textboxes(numberof_lines, npc_rect, linesinlist, textboxname):
    global numberlines, alltextboxes, dontmove
    for x in range(numberof_lines):
        screen.blit(dialogue_box, (50, screen_height - 120))
        text_surface = font.render(linesinlist[x], True, (255, 255, 255))
        screen.blit(text_surface, (60, screen_height - 100))
        pygame.display.flip()

        wait_b = True
        while wait_b:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wait_b = False 
        while pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
        if x == len(linesinlist)-1:
            dontmove = False
            return False


def restart():
    global timer, current_direction, level, current_level, puzzles, firsttime, dontmove, screen_right, screen_left, screen_up, screen_down, npc_visible, restart_factor, current
    timer = 120
    puzzles = [{"direction":"right"}, {"direction":"left"}, {"direction":"down"}, {"direction":"up"}]
    current_direction = "right"
    level = 1
    current_level = -1
    random.shuffle(puzzles)
    firsttime = True
    player_rect.x = screen_width//2
    player_rect.y = screen_width//2
    dontmove = False
    screen_right = screen_left = screen_up = screen_down = False
    npc_visible = True
    restart_factor += current

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    current = pygame.time.get_ticks() - restart_factor
    # Clear screen 
    screen.fill((30, 30, 30))

    timer = 10 - (current//1000)
    text_surface = font.render(str(timer), True, (255, 255, 255))
    screen.blit(text_surface, (screen_width - 50, 0))            
    if timer == 0:
        restart()

    # old position 
    old_pos = player_rect.topleft

    # keys
    keys = pygame.key.get_pressed()

    if dontmove == False:
        if keys[pygame.K_UP]: player_rect.y -= player_speed
        if keys[pygame.K_DOWN]: player_rect.y += player_speed
        if keys[pygame.K_LEFT]: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]: player_rect.x += player_speed


    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # NPC collision
    if player_rect.colliderect(npc_rect) and npc_visible:
        player_rect.topleft = old_pos

    # bounds
    if (player_rect.x +player_size) >= screen_width and keys[pygame.K_RIGHT]:
        screen_right = True
        player_rect.x = 50
    if (player_rect.x -player_size) <= 0 and keys[pygame.K_LEFT]:
        screen_left = True
        player_rect.x = screen_width - 50
    if (player_rect.y + player_size) >= screen_height and keys[pygame.K_DOWN]:
        screen_down = True
        player_rect.y = 50
    if (player_rect.y - player_size) <= 0 and keys[pygame.K_UP]:
        screen_up = True
        player_rect.y = screen_height - 50
    player_rect.x = max(0, min(player_rect.x, screen_width - player_size))
    player_rect.y = max(0, min(player_rect.y, screen_height - player_size))

    if screen_right:
        if current_direction == "right":
            screen.fill((60,60,60))

            level += 1

            current_level += 1
            if current_level < len(puzzles):
                current_direction = puzzles[current_level]["direction"]
            screen_right = False
        else:
            screen_right = False
            pass
    elif screen_left:
        if current_direction == "left":
            screen.fill((60,60,60))

            level += 1

            current_level += 1
            if current_level < len(puzzles):
                current_direction = puzzles[current_level]["direction"]
            screen_left = False
        else:
            screen_left = False
            pass
    elif screen_down:
        if current_direction == "down":
            screen.fill((60,60,60))

            level += 1

            current_level += 1
            if current_level < len(puzzles):
                current_direction = puzzles[current_level]["direction"]
            screen_down = False
        else:
            screen_down = False
            pass
    elif screen_up:
        if current_direction == "up":
            screen.fill((60,60,60))

            level += 1

            current_level += 1
            if current_level < len(puzzles):
                current_direction = puzzles[current_level]["direction"]
            screen_up = False

        else:
            screen_up= False
            pass

    if player_visible:
        screen.blit(player_image, player_rect.topleft)
    if npc_visible:
        screen.blit(npc_image, npc_rect.topleft)

    # Interaction logic
    for index, each in enumerate(npc_list):
        close_dirs = one_move_from_collision(player_rect, each, player_speed)
        if any(close_dirs.values()) and keys[pygame.K_SPACE] and npc_visible_list[index]:
            alltextboxes[index] = True
        else:
            dontmove = False

    if alltextboxes[0] == True:
        alltextboxes[0]  = make_textboxes(6, npc_rect, ["I have been stuck here for 10,000 years... (Press Space to Continue)", "Be careful of the time limit", "If the time reaches 0 in this dangerous cave...", "you will reset back here just like me.", "Just so you know, going right is the correct way out of this room", "After that, its all random"], alltextboxes[0] )  
        dontmove = True



    # Update screen
    pygame.display.flip()
    clock.tick(60)

