import pygame
import sys
import random 
import math
import time
import asyncio

pygame.init()

# Set up window
infoObject = pygame.display.Info()
screen_width = infoObject.current_w
screen_height = infoObject.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
pygame.display.set_caption("Escape")

# funny booleans
dontmove = False
screen_right = screen_left = screen_up = screen_down = False
firsttime = True
firsttime_arrow = True
global firsttime_title
firsttime_title = True
firsttime_end = True
game_completes = 0
global first_control_time
first_control_time = True
first_control_timer = True

# Clock stuff
clock = pygame.time.Clock()
timer = 120
restart_factor = 0

# player setup
player_size = 40
player_speed = 5
player_rect = pygame.Rect(screen_width // 2, screen_height // 2, player_size, player_size)

async def main():
  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    pygame.display.update()
    await asyncio.sleep(0)
    clock.tick(60)



def make_npc_rect(width_position, height_position, npc_width, npc_height):
    return pygame.Rect(width_position, height_position, npc_width, npc_height)
# NPC setup
npc_rect = make_npc_rect(screen_width // 2, screen_height // 2 - screen_height // 4, player_size, player_size)
sign_rect = make_npc_rect(screen_width // 2, screen_height // 2 - screen_height // 4, player_size, player_size)

# Load player and NPC image (same for now)
player_image = pygame.image.load(r"assets/puffin.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

npc_image = pygame.image.load(r"assets/puffinSide.png").convert_alpha()
npc_image = pygame.transform.scale(npc_image, (player_size, player_size))

torch_image = pygame.image.load(r"assets/torch.png").convert_alpha()
torch_image = pygame.transform.scale(torch_image, (player_size, player_size))


arrow_image_1 = pygame.image.load(r"assets/arrow.png").convert_alpha()
arrow_image_1 = pygame.transform.scale(arrow_image_1, (player_size, player_size))
arrow_image_2 = pygame.transform.rotate(arrow_image_1, 270)
arrow_image_3 = pygame.transform.rotate(arrow_image_1, 90)
arrow_image_4 = pygame.transform.rotate(arrow_image_1, 180)
arrow_images = [arrow_image_1, arrow_image_2, arrow_image_3, arrow_image_4]
arrow_images_save = arrow_images.copy()
arrow_index = 0

title_image_sh = pygame.image.load(r"assets/title_sh.png").convert_alpha()
title_image_sh = pygame.transform.scale(title_image_sh, (screen_width, screen_height))

title_image_ch = pygame.image.load(r"assets/title_ch.png").convert_alpha()
title_image_ch = pygame.transform.scale(title_image_ch, (screen_width, screen_height))

# visible flags
player_visible = True
npc_visible = True
arrow_rect_visible = False
torches_visible = True
sign_visible = False
no_lights_text = False

# Font & dialogue box setup
font = pygame.font.SysFont("Arial", 32)
dialogue_box = pygame.Surface((screen_width - 100, 80), pygame.SRCALPHA)
dialogue_box.fill((0, 0, 0, 180))  # semi-transparent black box

# list 
npc_list = [npc_rect, sign_rect]
npc_visible_list = [npc_visible, sign_visible]
alltextboxes = [False for x in npc_list]

torch_r = make_npc_rect(screen_width - (player_size*5), screen_rect.height - (player_size * 10), player_size, player_size)
torch_l = make_npc_rect(screen_width - (player_size*27), screen_rect.height - (player_size*10), player_size, player_size)
torch_b = make_npc_rect(screen_rect.width - (player_size*16), screen_rect.height - (player_size*5), player_size, player_size)
torches_list = [torch_l, torch_b, torch_r]
# puzzle dict
puzzles = [{"direction":"right", "puzzle_name": "spin_arrow"}, {"direction":"up", "puzzle_name": "no_lights"}]
puzzles_save = puzzles.copy()
# puzzle flags
current_direction = "right"
level = 1
current_level = -1
random.shuffle(puzzles)


title_menu_pos = 0

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wait_b = False 
        while pygame.key.get_pressed()[pygame.K_SPACE]:
            pygame.event.pump()
        if x == len(linesinlist)-1:
            dontmove = False
            return False


def restart():
    global timer, current_direction, level, current_level, puzzles, firsttime, dontmove, screen_right, screen_left, screen_up, screen_down, npc_visible, restart_factor, current, arrow_rect_visible, torches_visible, firsttime_arrow, arrow_images, arrow_images_save, arrow_index
    timer = 120
    puzzles = puzzles_save.copy()
    current_direction = "right"
    level = 1
    current_level = -1
    random.shuffle(puzzles)
    firsttime = True
    player_rect.x = screen_width//2
    player_rect.y = screen_height//2
    dontmove = False
    screen_right = screen_left = screen_up = screen_down = False
    npc_visible = True
    restart_factor += current
    arrow_rect_visible = False
    torches_visible = True
    firsttime_arrow = True
    arrow_images = arrow_images_save.copy()
    arrow_index = 0
def spin_arrow():
    global arrow_rect, arrow_rect_visible, now, arrow_index, firsttime_arrow, current_direction, random_dir, arrow_images, arrow_images_save
    arrow_rect = make_npc_rect(screen_width // 2, screen_height // 2 -100, player_size, player_size)
    arrow_rect_visible = True
    if firsttime_arrow:
        arrow_images = arrow_images_save.copy()
        firsttime_arrow = False
        random_dir = random.randint(0,3)
        arrow_images.pop(random_dir)
        if random_dir == 0:
            current_direction = "up"
        elif random_dir == 1:
            current_direction = "right"
        elif random_dir == 2:
            current_direction = "left"
        elif random_dir == 3:
            current_direction = "down"
        now = time.time()
def no_lights():
    global sign_rect, sign_visible, no_lights_text, torches_visible
    sign_rect = make_npc_rect(screen_width // 2, screen_height // 2 - screen_height // 4, player_size, player_size)
    sign_visible = True
    npc_visible_list[1] = True
    no_lights_text = True
    torches_visible = False


game_state = "Title"
running = True
# Game loop
while running:
    if game_state == "Title":
        if firsttime_title:
            screen.blit(title_image_sh, (0, 0))
            firsttime_title = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            title_menu_pos = 1
            screen.blit(title_image_ch, (0, 0))
        if keys[pygame.K_UP]:
            title_menu_pos = 0
            screen.blit(title_image_sh, (0, 0))
        if keys[pygame.K_SPACE] and title_menu_pos == 0:
            if game_completes > 0:
                restart()
            restart_factor = pygame.time.get_ticks()
            game_state = "Game"
        elif keys[pygame.K_SPACE] and title_menu_pos == 1:
            game_state = "Credits"
    elif game_state == "Game":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear screen 
        screen.fill((30, 30, 30))

        for x in torches_list:
            if player_rect.colliderect(x) and torches_visible:
                player_rect.topleft = old_pos
        if torches_visible:
            for each in torches_list:
                screen.blit(torch_image, each.topleft)

        current = pygame.time.get_ticks() - restart_factor

        timer = 120 - (current//1000)
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
        if player_rect.colliderect(sign_rect) and sign_visible:
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

        if current_level >= len(puzzles):
            screen.fill((0,0,0))
            game_state = "End"
            continue
        if screen_right:
            npc_visible = False
            if current_direction == "right":
                screen.fill((60,60,60))

                level += 1

                current_level += 1
                arrow_rect_visible = False
                sign_visible = False
                torches_visible = True
                no_lights_text = False
                npc_visible_list[1] = False
                alltextboxes[1] = False
                if current_level < len(puzzles):
                    current_direction = puzzles[current_level]["direction"]
                    if puzzles[current_level]["puzzle_name"] == "spin_arrow":
                        spin_arrow()
                    elif puzzles[current_level]["puzzle_name"] == "no_lights":
                        no_lights()
                    else: 
                        arrow_rect_visible = False
                screen_right = False
            else:
                screen_right = False
                restart()
        elif screen_left:
            npc_visible = False
            if current_direction == "left":
                screen.fill((60,60,60))

                level += 1

                current_level += 1
                arrow_rect_visible = False
                sign_visible = False
                torches_visible = True
                no_lights_text = False
                npc_visible_list[1] = False
                alltextboxes[1] = False
                if current_level < len(puzzles):
                    current_direction = puzzles[current_level]["direction"]
                    if puzzles[current_level]["puzzle_name"] == "spin_arrow":
                        spin_arrow()
                    elif puzzles[current_level]["puzzle_name"] == "no_lights":
                        no_lights()
                    else: 
                        arrow_rect_visible = False
                screen_left = False
            else:
                screen_left = False
                restart()
        elif screen_down:
            npc_visible = False
            if current_direction == "down":
                screen.fill((60,60,60))

                level += 1

                current_level += 1
                arrow_rect_visible = False
                sign_visible = False
                torches_visible = True
                no_lights_text = False
                npc_visible_list[1] = False
                alltextboxes[1] = False
                if current_level < len(puzzles):
                    current_direction = puzzles[current_level]["direction"]
                    if puzzles[current_level]["puzzle_name"] == "spin_arrow":
                        spin_arrow()
                    elif puzzles[current_level]["puzzle_name"] == "no_lights":
                        no_lights()
                    else: 
                        arrow_rect_visible = False
                screen_down = False
            else:
                screen_down = False
                restart()
        elif screen_up:
            npc_visible = False
            if current_direction == "up":
                screen.fill((60,60,60))

                level += 1

                current_level += 1
                arrow_rect_visible = False
                sign_visible = False
                torches_visible = True
                no_lights_text = False
                npc_visible_list[1] = False
                alltextboxes[1] = False
                if current_level < len(puzzles):
                    current_direction = puzzles[current_level]["direction"]
                    if puzzles[current_level]["puzzle_name"] == "spin_arrow":
                        spin_arrow()
                    elif puzzles[current_level]["puzzle_name"] == "no_lights":
                        no_lights()
                    else: 
                        arrow_rect_visible = False
                screen_up = False

            else:
                screen_up= False
                restart()

        if player_visible:
            screen.blit(player_image, player_rect.topleft)
        if npc_visible:
            screen.blit(npc_image, npc_rect.topleft)
            if first_control_time:
                controls_txt = """Press Space to Interact
    Press X to go back except when talking or reading"""
                text_surface = font.render(str(controls_txt), True, (255, 255, 255))
                screen.blit(text_surface, (screen_width//4, screen_height//4)) 
                if first_control_timer:
                    ctrlnow = time.time()
                    first_control_timer = False
            if time.time() > ctrlnow+5:
                first_control_time = False
        if arrow_rect_visible:
            screen.blit(arrow_images[arrow_index], arrow_rect.topleft)
            if time.time() > now+0.25:
                now = time.time()
                arrow_index +=1
                if arrow_index >= len(arrow_images):
                    arrow_index = 0
        if sign_visible:
            screen.blit(npc_image, sign_rect.topleft)

        # Interaction logic
        for index, each in enumerate(npc_list):
            close_dirs = one_move_from_collision(player_rect, each, player_speed)
            if any(close_dirs.values()) and keys[pygame.K_SPACE] and npc_visible_list[index]:
                alltextboxes[index] = True
            else:
                dontmove = False

        if alltextboxes[0] == True and npc_visible:
            alltextboxes[0]  = make_textboxes(6, npc_rect, ["I have been stuck here for 10,000 years... (Press Space to Continue)", "Be careful of the time limit", "If the time reaches 0 in this dangerous cave...", "you will reset back here just like me.", "Just so you know, going right is the correct way out of this room", "After that, its all random"], alltextboxes[0] )  
            dontmove = True
        if alltextboxes[1] == True and sign_visible:
            alltextboxes[1] = make_textboxes(1, sign_rect, ["Walk where the light never shown"], no_lights_text)
            dontmove = True
            torches_visible = False
    elif game_state == "Credits":
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
        keys = pygame.key.get_pressed()
        f_credits_txt = """Programming - Supertiger576 and Flippdylalaland
        
        Art - Flippdylalaland and Supertiger576
        
        Made in Pygame
        """
        text_surface = font.render(str(f_credits_txt), True, (255, 255, 255))
        screen.blit(text_surface, (screen_width//4, screen_height//4))   
        if keys[pygame.K_x]:
            game_state = "Title"
            screen.blit(title_image_ch, (0, 0))
    elif game_state == "End":
        end_txt = """You Escaped.
        Thank you for playing
        """
        text_surface = font.render(str(end_txt), True, (255, 255, 255))
        screen.blit(text_surface, (screen_width//4, screen_height//4))  
        if firsttime_end:
            endnow = time.time()
            firsttime_end = False
        if time.time() > endnow+5:
            firsttime_title = True
            title_menu_pos = 0
            screen.blit(title_image_sh, (0, 0))
            game_state = "Title"
            game_completes +=1



    # Update screen
    pygame.display.flip()
    clock.tick(60)
asyncio.run(main())