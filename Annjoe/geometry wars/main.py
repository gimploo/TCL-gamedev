import pygame

# Display
print("GAME INITIALIZING")

pygame.display.init()
window = pygame.display.set_mode((800, 600))

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100

#player surface creation

player = pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT)).convert_alpha()
player_angle = 0           #player starting angle
player_rot_speed = 0.2     #player_rotation_speed
player_speed = 0.5         #player movement speed

#player default starting position(center of screen)
defpos_x = window.get_width()/2
defpos_y = window.get_height()/2

#movement flags
up = False
down = False
left = False
right = False

#process running flag
window_is_open = True

# Game loop
while window_is_open:

    #position chnages according to buttons
    if up:
        defpos_y -= player_speed
        #print("PLayer moving up")
    if down:
        defpos_y += player_speed
        #print("PLayer moving down")
    if left:
        defpos_x -= player_speed
        #print("PLayer moving left")
    if right:
        defpos_x += player_speed
        #print("PLayer moving right")

    

    # PLAYER INPUTS 
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #quitting
            window_is_open = False

        # TODO: able to hold down keys to move the player

        if event.type == pygame.KEYDOWN:#Keydown events

            if event.key== pygame.K_w:
                up = True
            elif event.key == pygame.K_s:
                down = True
            elif event.key == pygame.K_a:
                left = True
            elif event.key == pygame.K_d:
                right = True
            elif event.key == pygame.K_q:
                window_is_open = False

        if event.type == pygame.KEYUP: #Keyup events
            if event.key == pygame.K_w:
                up = False
            elif event.key == pygame.K_s:
                down = False
            elif event.key == pygame.K_a:
                left = False
            elif event.key == pygame.K_d:
                right = False




    # Fill the screen
    pygame.Surface.fill(window, (0,0,0))
    pygame.Surface.fill(player, (255,0,0))

    #rotate the player around its axis

    player_rot = pygame.transform.rotate(player, player_angle) #rotating player surface   
    player_rot_center = (defpos_x - (player_rot.get_width()/2), defpos_y - (player_rot.get_height()/2)) #centering the surface so that it doesnt bounce

    
    #drawing player surface
    window.blit(player_rot, player_rot_center) #drawing player surface onto window surface using blit function
    player_angle += player_rot_speed #angle incremented
    

    pygame.display.flip()


print("GAME CLOSED")