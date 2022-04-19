
#gravity aura quite buggy

import pygame
import random, math
from abilities import Abilities
from button import Button

clock = pygame.time.Clock()

# Display
print("GAME INITIALIZING")
o_w = 1025
w_w = 800
w_h = 600

pygame.init()
pygame.display.init()
pygame.font.init()
game_window = pygame.display.set_mode((o_w, w_h))
window = pygame.Surface((w_w, w_h)).convert_alpha()

def font_creator(text, color, screen, x, y, bold = False , text_type = None, text_size = 30):
        
        if bold:
            font = pygame.font.SysFont(text_type, text_size)
            font.bold = True
        else:     
            font = pygame.font.SysFont(text_type, text_size)
            font.bold = False
        label = font.render(text, 1, color)
        screen.blit(label, (x, y))


def main_game(action_mode, best_score):
    p_w = 30
    p_h = 30
    global time, clock_time, score_time, score, prev_score_time 
    time = 0
    clock_time = 0

    #score variables
    score_time = 0
    score = 0
    def_score_inc = 25/100 #percentage 
    prev_score_time = 0



    screen_edge_correction = 10 #minor value correction in screen dimensions in order to be more precise with boundary collisions #set it to 16 if any problems occur

    #player surface creation

     
    global bomb_mode, blinking
    player_feat = [None, None] #player features
    player_color = (255,0,0) 
    player_angle = 0           #player starting angle
    player_health = 10
    player_rot_speed = 0.8  #optimum_rot_speed -->0.8(changed due to poor code opimisation)     #player_rotation_speed
    player_speed =  1    #optimum player speed --->0.5        #player movement speed
    player_growth = 'red cube'
    player_health_inc = 5
    bomb_mode = False
    blinking = False

    enemy_rot_speed = 1.5    #optimum enemy rot speed -->0.5 
    enemy_angle = 0
    enemy_speed = 1.5       #optimum enemy speed --> 0.5
    def_enemy_damage = 15/100  #percentage of its dimensions
    enemies = []
    enemy_edge_color = (33, 34, 40)
    player_rect_correction_factor = 1
    enemy_rect_correction_factor = 1.25
    powerup_correction_factor = 0.6
    aura_correction_factor = 1.24
    shield_rad_cent = 1.7
    gravity_rad_cent = 1.6
    limit = 3

    #player default starting position(center of screen).Since the player is cenetered later, these values are the center coordinates of the player and not the top left coordinates
    defpos_x = window.get_width()/2  
    defpos_y = window.get_height()/2

    #movement flags
    up = False
    down = False
    left = False
    right = False



    def spawn_point_generator():
        """genertaes spawn points for enemies"""
        x_list = []
        y_list = []
        for x in range(-200, 1001):
            if x < -2 or x > 802:
                x_list.append(x)

        for y in range(-200, 801):
            if y < - 2 or y > 602:
                y_list.append(y)


        enemy_pos = (random.choice(x_list), random.choice(y_list))

        return enemy_pos

    def enemy_generator(player_pos, enemy_list, limit, time):
        """Generates enemies"""
        if len(enemy_list) < limit:
            enemy_spawn = spawn_point_generator()
            #print(enemy_spawn)

            #randomly generating enemy dimensions
            if time < 50:
                enemy_dimension = random.randint(20, 40)
            elif time >= 50 and time < 90 :
                enemy_dimension = random.randint(25, 50)
            elif time >= 90 and time < 140:
                enemy_dimension = random.randint(32, 70)
            elif time >= 140 and time < 200:
                enemy_dimension = random.randint(65, 84)
            elif time >= 200 and time < 320:
                enemy_dimension = random.randint(68, 100)
            elif time >= 320 and time < 500:
                enemy_dimension = random.randint(75, 114)
            elif time >= 500:
                enemy_dimension = random.randint(75, 140)

            enemy_edge = pygame.Surface((enemy_dimension + 5, enemy_dimension + 5)).convert_alpha()
            enemy = pygame.Surface((enemy_dimension, enemy_dimension)).convert_alpha()
            travel_angle = math.atan2(player_pos[1] - enemy_spawn[1],player_pos[0] - enemy_spawn[0])
            collided = False
            slave = False
            enemy_rect = None
            def_dim = enemy_dimension
            enemy_list.append([travel_angle, enemy_spawn[0], enemy_spawn[1], enemy, enemy_dimension, collided, enemy_edge, slave, enemy_rect, def_dim])


    def enemy_wave_generator(limit, time, enemy_list):

        #new_limit 
        if enemy_list == []:                             #if enemies == []:
            #limit = random.randint(2,5)
            new_limit = 3
            #print("ok")

            
        #if 'gravity aura' in active_powers:
        #    new_limit = 12 







        if len(enemy_list) < limit:
            new_limit = int((12/880) * (time - 20) + 3)
            if time < 20:

                new_limit = 3
            elif time > 900:
                new_limit = 15 
            
            

        else:
            new_limit = limit

        return new_limit



    def animation_generator(enemy_list):
        """PLays destroyed animation"""
        width, height = enemy_list[3].get_width(), enemy_list[3].get_height()
        enemy_pieces = []
        for _ in range(3):
            #enemy_piece = pygame.Rect(enemy_list[0] + (width/4) * _, enemy_list[1] + (height/4) * _, (width/4), (height/4))
            
            enemy_piece = pygame.Surface((width/4, height/4)).convert_alpha()
            enemy_pieces.append(enemy_piece)

        return enemy_pieces

    def powerup_position_generator(player_pos, player_dimensions):
        """power up position"""
        accuracy_correction = 30
        player_x = list(range(int(player_pos[0] - accuracy_correction), int(player_pos[0] + player_dimensions + accuracy_correction)))
        player_y = list(range(int(player_pos[1] - accuracy_correction), int(player_pos[1] + player_dimensions + accuracy_correction)))
        x_limits = []
        y_limits = []

        for x in range(accuracy_correction, w_w - accuracy_correction):
            if x not in player_x:
                x_limits.append(x)

        for y in range(accuracy_correction, w_h - accuracy_correction):
            if y not in player_y:
                y_limits.append(y)

        power_pos = [random.choice(x_limits), random.choice(y_limits)]

        return power_pos

    def stored_powers_updater(stored_powers, new_power):
        """UPdates stored powers"""
        if stored_powers != {}:
            
            if new_power in stored_powers.keys():
                stored_powers[new_power] += 1
            else:
                stored_powers[new_power] = 1

        else:
            stored_powers[new_power] = 1


    def scoring():
        global score, score_time, prev_score_time
        s_s = 5
        s_i = 20
        #r_f = 1
        
        
        if score_time % s_s == 0 and score_time != prev_score_time:
            score += s_i
            prev_score_time = score_time
            #score_time += r_f 
            #score_error = True
            #print("Score: ", score_num, "time: ", score_time)
            #print("score: ", score, "score time", score_time)


    def shield_collision(power, enemy_rect, shield_rad, shield_centre):
        """Shield collision"""

        rect_points = [enemy_rect.topleft, enemy_rect.topright, enemy_rect.bottomleft, enemy_rect.bottomright]
        #print(shield_centre, rect_points)
        
        if power == 'shield':
            for points in rect_points:
                if (points[0] - shield_centre[0])**2 + (points[1] - shield_centre[1])**2 < shield_rad ** 2:
                    return True
            return False

        if power == 'gravity aura':
            rect_centre = enemy_rect.center
            if (rect_centre[0] - shield_centre[0])**2 + (rect_centre[1] - shield_centre[1])**2 < shield_rad ** 2:
                #print((rect_centre[0], rect_centre[1]))
                return (True, [rect_centre[0], rect_centre[1]])

            else:
                return (False, None)

        if power == 'bomb':
            for points in rect_points:
                if (points[0] - shield_centre[0])**2 + (points[1] - shield_centre[1])**2 < shield_rad ** 2:
                    return True
            return False     

    def health_interpreter(player_mode, player_health):
        """Changes player according to health"""
        global time
        if player_health >= 100:
            if player_mode == 'red cube':
                new_player_health = player_health - 100
                new_player_mode = 'blue giant'
            elif player_mode == 'blue giant':
                new_player_health = player_health - 100
                new_player_mode = 'slayer'
            elif player_mode == 'slayer':
                new_player_health = player_health - 100
                new_player_mode = 'bomb'
            elif player_mode == 'bomb':
                new_player_health = 100
                new_player_mode = 'bomb'
                
                

        elif player_health <= 0 and player_mode != 'dead':
            if player_mode == 'bomb':
                new_player_health = 100 + player_health
                new_player_mode = 'slayer'
            elif player_mode == 'red cube':
                new_player_health = 0
                new_player_mode = 'dead'
                time = 0
            elif player_mode == 'blue giant':
                new_player_health = 100 + player_health
                new_player_mode = 'red cube'
            elif player_mode == 'slayer':
                new_player_health = 100 + player_health
                new_player_mode = 'blue giant'
            

        else:
            new_player_mode = player_mode
            new_player_health = player_health


        return new_player_mode, new_player_health


    def health_projector(player_w, player_h, player_c):
        global bomb_mode, blinking
        p_mode, p_health = health_interpreter(player_growth, player_health)
        threshold_health = 15

        if p_mode == 'dead':
            return 0, 0, p_mode, player_c, p_health, 0, 0, 0
        if p_mode == 'red cube':
            size_slope = 25/84
            rot_slope = -0.2/25
            starting_rot = 3 
            starting_size = 25
            p_color = (255, 0, 0)
            new_score_inc = def_score_inc
            enemy_damage = def_enemy_damage
            #p_rot_speed = 
        elif p_mode == 'blue giant':
            size_slope = 20/84
            rot_slope = -0.6/20 
            starting_rot = 2.7
            starting_size = 60
            p_color = (0, 0, 255)
            new_score_inc = 1.5 *def_score_inc
            enemy_damage = 0.9 * def_enemy_damage
 
        elif p_mode == 'slayer':
            size_slope = 30 / 84
            starting_rot = 2
            rot_slope =  -1.2/30
            starting_size = 90
            p_color = (255, 157, 0)
            new_score_inc = 2.25 * def_score_inc
            enemy_damage = 0.72 * def_enemy_damage


        elif p_mode == 'bomb':
            size_slope = 0
            starting_rot = 0.8
            rot_slope = 0
            starting_size = 120
            new_score_inc = 4 * def_score_inc
            enemy_damage = 0.56 * def_enemy_damage
            if bomb_mode == False:
                #flashing logic
                flash_p = (4/98)*(player_health - 1) + 1

                if player_c[1] >= 160:
                    blinking = True
                        



                elif player_c[1] <= 0:
                    blinking = False
                    

                if blinking == True:
                    p_color = [255, player_c[1] - flash_p, player_c[1] - flash_p]
                    if p_color[1] <= 0:
                    
                        p_color[1] = 0
                        p_color[2] = 0

                elif blinking == False:
                    p_color = [255, player_c[1] + flash_p, player_c[1] + flash_p]
                    if p_color[1] >= 160:
                    
                        p_color[1] = 160
                        p_color[2] = 160

                p_color = tuple(p_color)
                #print(flash_p)





        if p_health >= threshold_health:
                p_width = (size_slope * (p_health - threshold_health)) + starting_size
                
                p_height = (size_slope * (p_health - threshold_health)) + starting_size
                p_rot_speed = (rot_slope * (p_width - starting_size)) + starting_rot

        if p_health < threshold_health:
            p_width = (size_slope * (threshold_health - threshold_health)) + starting_size
            
            p_height = (size_slope * (threshold_health - threshold_health)) + starting_size
            p_rot_speed = (rot_slope * (starting_size - starting_size)) + starting_rot

        if bomb_mode == True or bomb_mode == 'preparing':
            if bomb_mode == True:
                p_color = (255, 0, 0)
                if player_w <= 120 and player_w >= 1: #absorbing
                    player_w -= 0.4            #0.3
                    player_h -= 0.4            # 0.3
                    p_rot_speed += 1.5
                    p_width = player_w
                    p_height = player_h
                    
                    #print("ok")
                if player_w < 1 and player_w > 0.1: #waiting
                    player_w -= 0.0023      #0.0012
                    player_h -= 0.0023
                    p_width = player_w
                    p_height = player_h
                if player_w <= 0.1: #release start
                    bomb_mode = 'preparing'
            if player_w <= w_h + 200 and  bomb_mode == 'preparing': #releasing
                player_w += 1.3  #1
                player_h += 1.3
                p_width = player_w
                p_height = player_h
                p_rot_speed += 1

                if player_c[1] < 255:
                    
                    p_color = (255, (player_c[1] + 0.6) , 0)
                    

                elif player_c[1] >= 255 and player_c[2] < 80:
                    p_color = (255, 255, (player_c[2] + 0.5))
                else:
                    p_color = player_c
                
                


            if player_w > w_h + 200: #full destruction
                bomb_mode = 'complete destruction'

        if bomb_mode == 'complete destruction': #coming back to real form

            player_w -= 0.7
            player_h -= 0.7
            p_width = player_w
            p_height = player_h
            p_color = list(player_c)

            if player_c[0] > 102:
                p_color[0] = player_c[0] - 0.3

            if player_c[1] > 102:
                p_color[1] = player_c[1] - 0.3

            if player_c[2] < 102:
                p_color[2] = player_c[2] + 0.01

            p_color = tuple(p_color)


                    



            if player_w <= 25 and player_h <= 25:
                p_mode = 'red cube'
                p_health = 50
                bomb_mode = False
                p_color = (255, 0, 0)

            
                

        #print(p_color)
        #print(p_width, p_rot_speed)
        return p_width, p_height, p_mode, p_color, p_health, p_rot_speed, new_score_inc, enemy_damage






        #        new_player_width = 100
        #        new_player_height = 100
        #        new_player_color = (255, 0, 0)



        
        
    

    def score_board(stored_powers):
        """creates side panel"""
        font_creator('Score: ', (0, 0, 0), game_window, 813, 50, bold = True, text_type = 'Lucida Console', text_size = 25)
        font_creator( str(score), (0, 0, 0), game_window, 935, 50, bold = True, text_type = 'Lucida Console', text_size = 25)
        font_creator('Health: ', (210, 0, 0), game_window, 813, 90, bold = True, text_type = 'Lucida Console', text_size = 25)
        font_creator(str(player_health), player_color, game_window, 935, 90, bold = True, text_type = 'Lucida Console', text_size = 25)
        
        if player_growth == 'bomb':
            if time % 2 == 0 and bomb_mode == False:
                font_creator('bomb mode available', (0, 0, 0), game_window, 805, 130, bold = False, text_type = 'Lucida Console', text_size = 18)
                font_creator("[Press 'B']", (0, 0, 0), game_window, 840, 150, bold = True, text_type = 'Lucida Console', text_size = 17)

            elif bomb_mode != False:

                font_creator('bomb mode active', (255, 0, 0), game_window, 830, 130, bold = False, text_type = 'Lucida Console', text_size = 18)
        font_creator('POWERS', (80, 40, 0), game_window, 830, 200, bold = True, text_type = 'Eledonia', text_size = 40)
        if stored_powers != {}:
            st_num = 0
            plot_start = (820, 260)
            for abils in stored_powers:
                st_gap = 30
                new_st_pt = (plot_start[0],plot_start[1] + (st_num * st_gap))
                circ_rad = 10
                ability.ability_render(abils, game_window, new_st_pt, circ_rad)
                font_creator(f"({abils}): " + str(stored_powers[abils]), (0, 0, 0), game_window, new_st_pt[0] + 12, new_st_pt[1] - circ_rad, bold = False, text_type = 'Eledonia', text_size = 27)
                st_num += 1

        if active_powers != {}:
            at_num = 0
            plot_start = (820, 420)
            font_creator('ACTIVE POWERS', (80, 0, 150), game_window, 813, 380, bold = True, text_type = 'Eledonia', text_size = 30)
            for active_pow in active_powers:
                at_gap = 30
                new_at_pt = (plot_start[0],plot_start[1] + (at_num * at_gap))
                circ_rad = 10
                ability.ability_render(active_pow, game_window, new_at_pt, circ_rad)
                effective_time = {'time freeze' : 10, 'shield' : 15, 'gravity aura': 20}
                font_creator(f"  {str(effective_time[active_pow] - active_powers[active_pow])} s", (0, 0, 0), game_window, new_at_pt[0] + 12, new_at_pt[1] - circ_rad, bold = False, text_type = 'Eledonia', text_size = 27)
                at_num += 1




            













    #def collision_detector(enemy_center_pos, player_center_pos, enemy_width, enemy_height, player_height, player_width):
    #    """Detects collision"""
    #    enemy_center = [enemy_center_pos[0], enemy_center_pos[1]]
    #    player_center = [player_center_pos[0], player_center_pos[1]]
    #
    #    enemy_center[0] = int(enemy_center[0])
    #    enemy_center[1] = int(enemy_center[1])
    #    player_center[0] = int(player_center[0])
    #    player_center[1] = int(player_center[1])
    #
    #    enemy_width = int(enemy_width)
    #    enemy_height = int(enemy_height)
    #    if (enemy_center[0] + int(enemy_width)) in list(range(player_center[0] - int(player_width/2), (player_center[0] + int(player_width/2)))) and (enemy_center[1] + int(enemy_height)) in list(range(player_center[1] - int(player_height/2), (player_center[1] + int(player_height/2)))):
    #        return True
    #
    #    if (enemy_center[0] - int(enemy_width)) in list(range(player_center[0] - int(player_width/2), (player_center[0] + int(player_width/2)))) and (enemy_center[1] - int(enemy_height)) in list(range(player_center[1] - int(player_height/2), (player_center[1] + int(player_height/2)))):
    #        return True
    #
    #
    #    return False



    #process running flag
    window_is_open = True
    pause_buttons = [Button(290, 290, 30, 20, (255, 0, 0), text_size=30, text = 'Yes', text_color = (0, 0, 0)),Button( 487, 290, 30, 20, (255, 0, 0), text_size=30, text = 'No', text_color = (0, 0, 0))]

    ability = Abilities()
    active_power_icons = []
    stored_powers = {}
    active_powers = {}
    powerup_generation_time = 0
    collision_point = {}
    collider = 0
    render_time = None
    #powerup_active_time = 0

    # Game loop
    while window_is_open:

        clock_time += clock.get_rawtime()
            #print(clock_time)

        clock.tick()

            

        if clock_time/1000 >= 1:
            clock_time = 0
            time += 1
            score_time += 1
            #powerup_active_time += 1
            powerup_generation_time += 1

            if active_power_icons:
                for p_up in active_power_icons:
                    power[4] += 1

        #position chnages according to buttons
        if up:
            defpos_y -= player_speed
            #print("PLayer moving up")
            if 'gravity aura' in active_powers.keys(): #gravity aura slaves(need to be implemented in a better way)
                if collision_point != {}:
                    for pointers in collision_point:
                        collision_point[pointers][1] -= player_speed
            
        if down:
            defpos_y += player_speed
            #print("PLayer moving down")
            if 'gravity aura' in active_powers.keys(): #gravity aura slaves(need to be implemented in a better way)
                if collision_point != {}:
                    for pointers in collision_point:
                        collision_point[pointers][1] += player_speed
            
        if left:
            defpos_x -= player_speed
            #print("PLayer moving left")
            if 'gravity aura' in active_powers.keys(): #gravity aura slaves(need to be implemented in a better way)
                if collision_point != {}:
                    for pointers in collision_point:
                        collision_point[pointers][0] -= player_speed
            
        if right:
            defpos_x += player_speed
            #print("PLayer moving right")
            if 'gravity aura' in active_powers.keys(): #gravity aura slaves(need to be implemented in a better way)
                if collision_point != {}:
                    for pointers in collision_point:
                        collision_point[pointers][0] += player_speed
            

        

        # PLAYER INPUTS 
        for event in pygame.event.get():

            if event.type == pygame.QUIT: #quitting
                window_is_open = False
                break

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
                elif event.key == pygame.K_ESCAPE :
                    window_is_open = 'pause'
                    

                elif event.key == pygame.K_t:
                    if 'time freeze' in stored_powers:
                        if stored_powers['time freeze'] != 0:  
                            active_powers['time freeze'] = 0
                            stored_powers['time freeze'] -= 1

                elif event.key == pygame.K_x:
                    if 'shield' in stored_powers and 'gravity aura' not in active_powers:
                        if stored_powers['shield'] != 0:
                            active_powers['shield'] = 0
                            stored_powers['shield'] -= 1 

                elif event.key == pygame.K_g:
                    if 'gravity aura' in stored_powers and 'shield' not in active_powers:
                        if stored_powers['gravity aura'] != 0:
                            active_powers['gravity aura'] = 0
                            stored_powers['gravity aura'] -= 1

                elif event.key == pygame.K_b:
                    if player_growth == 'bomb':
                        bomb_mode = True


            if event.type == pygame.KEYUP: #Keyup events
                if event.key == pygame.K_w:
                    up = False
                elif event.key == pygame.K_s:
                    down = False
                elif event.key == pygame.K_a:
                    left = False
                elif event.key == pygame.K_d:
                    right = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()

                if window_is_open == 'pause':
                    for button in pause_buttons:
                        if button.check_cursor(mousepos):
                            if button.text == 'Yes':
                                window_is_open = False
                            else:
                                window_is_open = True
                            break





    # Fill the screen
        pygame.Surface.fill(game_window, (128, 128, 128))
        pygame.Surface.fill(window, (0,0,0))
        p_w, p_h, player_growth, player_color, player_health, player_rot_speed, score_inc , enemy_damage= health_projector(p_w, p_h, player_color)

        player = pygame.Surface((p_w,p_h)).convert_alpha()
        pygame.Surface.fill(player, player_color)

    #blitting window
        score_board(stored_powers)
        
        if player_growth != 'dead' and window_is_open != 'pause':
        #rotate the player around its axis
        
            player_rot = pygame.transform.rotate(player, player_angle) #rotating player surface   
            player_rot_center = (defpos_x - (player_rot.get_width()/2), defpos_y - (player_rot.get_height()/2)) #centering the surface so that it doesnt bounce
        
        
        #enemies generated in an instance
            limit = enemy_wave_generator(limit, time, enemies)
            enemy_generator((player_rot_center[0], player_rot_center[1]), enemies, limit, time)
            #print(len(enemies), time) 
        
        
        
        #player rectangle code for collision
        
            player_rect = player.get_rect()
            player_rect.width = p_w / player_rect_correction_factor
            player_rect.height = p_h / player_rect_correction_factor
            player_rect.x += defpos_x - (player.get_width()/ (player_rect_correction_factor * 2)) 
            player_rect.y += defpos_y - (player.get_width()/ (player_rect_correction_factor * 2)) 
            player_feat[0] = player
            player_feat[1] = player_rect
        
            
        
        #powerup code
            power_ups = 0
            #power up creation time genearation
            if active_power_icons == [] and powerup_generation_time == 0 and render_time == None:
                render_time = random.randint(5, 6)
                #print("render_time", render_time)
                #powerup_generation_time += (1/(10**20)) #to avoid to much random generations disrupting true randomness
                
            #power up generation     
            if powerup_generation_time == render_time:
                new_ab, rad = ability.ability_generator()
                
                position = powerup_position_generator((defpos_x, defpos_y), p_w)
                #print("rendered at", position, "at", render_time)
                rect_pos = pygame.Rect((position[0] - rad/(powerup_correction_factor * 2)), (position[1] - rad / (powerup_correction_factor * 2)), rad / (powerup_correction_factor), rad / (powerup_correction_factor))
                power_up_active_time = 0
                active_power_icons.append([new_ab, position, rect_pos,power_ups, power_up_active_time, rad])
                render_time = None
            
            #power up render
            for power in active_power_icons:
        
                ability.ability_render(power[0], window, power[1], rad)

                #pygame.draw.rect(window, (255, 255, 255), rect_pos)
                #pygame.draw.circle(window, (255, 255, 255), position, 40)
        
                shield_powerup = False
                gravity_powerup = False
                #print(power[4])
                if 'shield' in active_powers:
                    shield_powerup = shield_collision('shield', power[2], shield_rad_cent * player_feat[0].get_width(), player_feat[1].center)
        
                if 'gravity aura' in  active_powers:
                    gravity_powerup = shield_collision('gravity aura', power[2], gravity_rad_cent * player_feat[0].get_width(), player_feat[1].center)[0]
                
                #power up disappearing code
                if power[4] >= 5:
                    active_power_icons.pop(power[3])
                    powerup_generation_time = 0
        
                #power up collected code
                if player_rect.colliderect(power[2]) or shield_powerup == True or gravity_powerup == True :
                    active_power_icons.pop(power[3])
                    if power[0] == 'health':
                        player_health += player_health_inc

                    elif power[0] == 'score bag':
                        score += int((30 * (power[5] - 10) + 100))
        
                    else:
                        stored_powers_updater(stored_powers, power[0])
                    
                    powerup_generation_time = 0
                    
                    #print(stored_powers)
                    #print(enemy_angle)
        
        
            if active_powers:
                    
                for active_power, passed_time in active_powers.items():
                    ability.ability_effect_render(active_power, passed_time, active_powers, stored_powers, enemy_rect, player_feat, enemies, enemy, index, window)
                    if active_power not in active_powers.keys():
                        break
        
                for active_power, passed_time in active_powers.items():
                    if float(clock_time) == 0:
                        active_powers[active_power] += 1
                        #print(f"{active_power}: {active_powers[active_power]} s ------> real time:{time} s")
        
                
        
        
                
            
        
                
        
                    
        
        
            
        
        
        #enemy_code
            index = 0
            for enemy in enemies:
        
                
                # if enemy not collided
                if enemy[5] == False:
                    if 'time freeze' not in active_powers.keys():
                        if time < 50:

                            enemy_speed = (random.randrange(8, 11)) / 10    #0.5 --->def
                            enemy_rot_speed = (random.randrange(7, 12)) / 10 #0.5 --->def
                        elif time >= 50 and time < 90:
                            enemy_speed = (random.randrange(10, 14)) / 10    #0.5 --->def
                            enemy_rot_speed = (random.randrange(9, 15)) / 10 #0.5 --->def
        
                        elif time >= 90 and time < 150:
                            enemy_speed = (random.randrange(13, 17)) / 10    #0.5 --->def
                            enemy_rot_speed = (random.randrange(13, 19)) / 10 #0.5 --->def
        
                        elif time >= 150 and time < 350:
                            enemy_speed = (random.randrange(15, 20)) / 10    #0.5 --->def
                            enemy_rot_speed = (random.randrange(13, 20)) / 10 #0.5 --->def
        
                        elif time >= 350 and time < 600:
                            enemy_speed = (random.randrange(19, 27)) / 10    #0.5 --->def
                            enemy_rot_speed = (random.randrange(17, 22)) / 10 #0.5 --->def
                        else:
                            enemy_speed = (random.randrange(25, 30)) / 10    #0.5 --->def
                            enemy_rot_speed = (random.randrange(20, 27)) / 10 #0.5 --->def
                        
        
                    elif 'time freeze' in active_powers.keys():
                        enemy_speed -=  0.0045           #def -->0.0004
                        enemy_rot_speed -= 0.005        #def -->0.00049
        
        
                        if enemy_speed <=0:
                            enemy_speed = 0
        
                        if enemy_rot_speed <= 0:
                            enemy_rot_speed = 0
        
                      
                        #print(enemy_speed)
        
                    vel_x = math.cos(enemy[0]) * enemy_speed
                    vel_y = math.sin(enemy[0]) * enemy_speed    
                    enemy[1] += vel_x
                    enemy[2] += vel_y
                    #enemy_rect = enemy[3].get_rect()
                    
                    
        
                    #print(f"player rect: {player_rect}, enemy rect: {enemy_rect}")
                    pygame.Surface.fill(enemy[3], (255,255,255))
                    pygame.Surface.fill(enemy[6], enemy_edge_color)
                    enemy_edge_rot = pygame.transform.rotate(enemy[6], enemy_angle)
                    enemy_rot = pygame.transform.rotate(enemy[3], enemy_angle)
                    enemy_edge_rot_centre = (enemy[1] - (enemy_edge_rot.get_width()/2),enemy[2] - (enemy_edge_rot.get_height()/2))
                    enemy_rot_center = (enemy[1] - (enemy_rot.get_width()/2),enemy[2] - (enemy_rot.get_height()/2))
        
                    enemy_rect = enemy[3].get_rect()
        
                    enemy_rect.width = enemy[3].get_width() / (enemy_rect_correction_factor)
                    enemy_rect.height = enemy[3].get_height() / (enemy_rect_correction_factor)
                    enemy_rect.x = enemy[1] - (enemy[3].get_width()/ (enemy_rect_correction_factor * 2))
                    enemy_rect.y = enemy[2] - (enemy[3].get_height()/ (enemy_rect_correction_factor * 2)) 
                    enemy[8] = enemy_rect
                    
                    
        
                    #if collision_detector(enemy_rot_center, player_rot_center, enemy[3].get_width(), enemy[3].get_height(), p_h, p_w):
                    #   window_is_open = False
                    #   break
                    window.blit(enemy_edge_rot, enemy_edge_rot_centre)
                    window.blit(enemy_rot, enemy_rot_center)
                    #pygame.draw.rect(window, (0, 255, 0), enemy_rect)
                    
                    if enemy_rect.colliderect(player_rect) and 'shield' not in active_powers.keys() and 'gravity aura' not in active_powers.keys() and bomb_mode != 'complete destruction' and bomb_mode != 'preparing':
                        true_dimension = enemy[4]
                        collision_corrections = 0
                        if bomb_mode == False and 'time freeze' not in active_powers:
                            player_damage = int((enemy_damage) * true_dimension) #player damage
                            player_health -= player_damage                       #player health decrement
                        score += int(score_inc * true_dimension)             #score increment
                        if abs(player_rect.top - enemy_rect.bottom) > collision_corrections:
                            enemy[5] = True
        
                        if abs(enemy_rect.top - player_rect.bottom) > collision_corrections:
                            enemy[5] = True
        
                        if abs(enemy_rect.right - player_rect.left) > collision_corrections:
                            enemy[5] = True
        
                        if abs(player_rect.right - enemy_rect.left) > collision_corrections:
                            enemy[5] = True
        
                        else:
                            enemy[5] = False
        
                        #enemy[5] = True
        
                    elif 'shield' in active_powers.keys():
                        true_dimension = enemy[4]
                        if shield_collision('shield', enemy_rect, shield_rad_cent * player_feat[0].get_width(), player_feat[1].center):
                            enemy[5] = True
                            score += int(score_inc * true_dimension) #score incremnt
        
                    elif 'gravity aura' in  active_powers.keys():
                        true_dimension = enemy[4]
                        collision_statement = shield_collision('gravity aura', enemy_rect, gravity_rad_cent * player_feat[0].get_width(), player_feat[1].center)
                        collision_state = collision_statement[0]
                         
                        if collision_state == True:
        
                            enemy[5] = True
                            enemy[7] = True
                            collision_point[collider] = collision_statement[1]
                            enemy.append(collider)
                            collider += 1
        
                    elif bomb_mode == 'preparing' or bomb_mode == 'complete destruction':
                        true_dimension = enemy[4]
                        if shield_collision('bomb', enemy_rect, p_w, player_rect.center):
                            enemy[5] = True
                            score += int(score_inc * true_dimension) #score incremnt    
        
                        
        
        
                        
        
        
                            
        
        
        
        
                    
                        
                    
                    
        
                #if enemy collided
                if enemy[5] == True:
                    enemy_collision_color = (255, 172, 28)
                    if 'time freeze' not in active_powers.keys() and enemy[7] == False:
                        vel_x = math.cos(enemy[0]) * -0.95   #def -->0.5
                        vel_y = math.sin(enemy[0]) * -0.95 #def --> 0.5
                        dec_num = 200 #def-->300
                        
                        enemy_decrement_factor = (enemy[4] / dec_num)
                        enemy[4] -= enemy_decrement_factor
                        enemy[1] += vel_x - enemy_decrement_factor
                        enemy[2] += vel_y - enemy_decrement_factor
        
        
        
                    elif 'time freeze' in active_powers.keys():
                        vel_x = 0
                        vel_y = 0
                        dec_num = 150 #def --> 200
                        enemy_decrement_factor = (enemy[4] / dec_num)
                        enemy[4] -= enemy_decrement_factor
                        enemy[1] += vel_x 
                        enemy[2] += vel_y
                        #print(score) 
        
                    elif 'gravity aura' in active_powers.keys() and enemy[7] == True:
                        vel_x = 0
                        vel_y = 0
                        enemy_collision_color = player_color
        
                        #print(collision_point, enemy)
                        if len(enemy) == 11:
                            enemy[1] = collision_point[enemy[10]][0]  
                            enemy[2] = collision_point[enemy[10]][1]
                         
                        #enemy[1] += defpos_x
                        #enemy[2] += defpos_y
        
                    elif 'gravity aura' not in active_powers.keys() and enemy[7] == True:
                        score += int(score_inc * true_dimension) #score increment
                        enemy[7] = False
                        limit = 3  
        
                    
                    
                    enemy[3] = pygame.Surface((enemy[4], enemy[4])).convert_alpha()
                    enemy[6] = pygame.Surface((enemy[4] + 5, enemy[4] + 5)).convert_alpha() # enemy outline
                    pygame.Surface.fill(enemy[3], enemy_collision_color)
                    pygame.Surface.fill(enemy[6], enemy_edge_color)
                    enemy_rect = enemy[3].get_rect()
                    enemy_rect.width = enemy[3].get_width() / (aura_correction_factor)
                    enemy_rect.height = enemy[3].get_height() / (aura_correction_factor)
                    enemy_rect.x = enemy[1] - (enemy[3].get_width()/ (aura_correction_factor * 2))
                    enemy_rect.y = enemy[2] - (enemy[3].get_height()/ (aura_correction_factor * 2)) 
                    enemy_edge_rot = pygame.transform.rotate(enemy[6], enemy_angle)
                    enemy_rot = pygame.transform.rotate(enemy[3], enemy_angle)
                    enemy_edge_rot_centre = (enemy[1] - (enemy_edge_rot.get_width()/2),enemy[2] - (enemy_edge_rot.get_height()/2))
                    enemy_rot_center = (enemy[1] - (enemy_rot.get_width()/2),enemy[2] - (enemy_rot.get_height()/2))
                    
                    window.blit(enemy_edge_rot, enemy_edge_rot_centre)
                    window.blit(enemy_rot, enemy_rot_center)
                    #pygame.draw.rect(window, (0, 255, 0), enemy_rect)
                    
        
                    if enemy[4] > (8.75/10) * true_dimension and active_powers == {} and bomb_mode == False and action_mode == 'enabled': #unnecessary slow-motion code #def-->9/10
                       clock.tick(random.randint(45, 60))
                       #print("true")
        
                    if enemy[4] < 5:             #deletes enemies if collided enemies reduces size beyond a limit
                        enemies.pop(index)
        
                    if enemy[7] == True:
         
                        n_en = 0 #counting variable(local)
                        for unknown in enemies:
                            if unknown[8] != None:
        
                                if unknown[8].colliderect(enemy_rect):
                                    if unknown[7] != True:
                                        unknown[5] = True
                                        if unknown[4] == unknown[9]:     
                                            score += int(score_inc * true_dimension) #score increment
                            n_en += 1
        
                    
        
        
        
        #        ------TEST CODE-------
        #        if enemy[5] == True:
        #            piece_list = animation_generator(enemy)
        #            piece_num = 1
        #            for piece in piece_list:
        #                vel_x = math.cos(enemy[0])  * -0.2
        #                vel_y = math.sin(enemy[0]) * -0.2
        #                piece_x = enemy[1]
        #                piece_y = enemy[2]
        #                piece_x += vel_x
        #                piece_y += vel_y
        #
        #                
        #                piece_num += 1
        #                pygame.Surface.fill(piece, (255,255,255))
        #                window.blit(piece, (piece_x, piece_y))
        
                
                
        
        
        
                    
        
                    
                #if enemy out of bounds 
                if (enemy_rot_center[0] <= -500 or enemy_rot_center[0] >= 1500) or (enemy_rot_center[1] <= -500 or enemy_rot_center[1] >= 1500):
                    enemies.pop(index)       
        
                
                
                    
                index += 1
        
        
            
            #angle incrementation for rotation for enemy and player
            player_angle += player_rot_speed #angle incremented
            #if 'time freeze' not in active_powers:
            enemy_angle += enemy_rot_speed
            #print("cool")
        
            
        
        
            #Boundary collision detection
            if bomb_mode == False:
                if defpos_x + (p_w/2) + screen_edge_correction >= window.get_width(): #collision with right edge of screen
                    defpos_x -= 1
                if defpos_x - (p_w/2) - screen_edge_correction <= 0: #collision with left edge of screen
                    defpos_x += 1
                if defpos_y + (p_h/2) + screen_edge_correction >= window.get_height(): #collision with top edge of screen
                    defpos_y -= 1
                if defpos_y - (p_h/2) - screen_edge_correction <= 0: #collision with bottom edge of screen
                    defpos_y += 1
        
            
            
        
            #drawing player surface
            if bomb_mode == 'preparing' or bomb_mode == 'complete destruction':
                player = pygame.draw.circle(window, player_color, player_rect.center, p_w)
            else:
                window.blit(player_rot, player_rot_center) #drawing player surface onto window surface using blit function
            #pygame.draw.rect(window, (0, 255, 0), player_rect)
            #print("Health:", player_health)
            game_window.blit(window, (0, 0))
            #scoring()
        
        elif player_growth == 'dead':
            death_screen_time = 3
            if score > best_score:
                with open('high_scores.txt', 'w') as high_score:
                    high_score.write(str(score))

                

            if time <= death_screen_time:
                font_creator('YOU ARE DEAD', (255, 0, 0), window, 200, 280, bold = True, text_type = 'Eledonia', text_size = 70)        
                game_window.blit(window, (0, 0))

                
            else:
                window_is_open = False
                break



        elif window_is_open == 'pause':
            pygame.draw.rect(window, (255, 0, 0), [210, 240, 400, 100])
            font_creator('You pressed Q.Do you want to quit?', (0, 0, 0), window, 235, 250, bold = False, text_type = 'Eledonia', text_size = 30)
            for button in pause_buttons:
                button.draw_button(window)

                mousepos = pygame.mouse.get_pos()

                if button.check_cursor(mousepos):
                    button.text_color = (255, 255, 255)
                else:
                    button.text_color = (0, 0, 0)
            game_window.blit(window, (0, 0))
            



        

        pygame.display.flip()


    print("GAME CLOSED")

#main menu
def main_menu():
    """Main_menu"""
    
    menu = 'main menu'
    main_menu_buttons = [Button( 450, 200, 100, 35, (255, 0, 0), text_size=23, text = 'Play', text_color = (0, 0, 0)), Button( 450, 255, 100, 35, (255, 0, 0), text_size=23, text = 'Help', text_color = (0, 0, 0)), Button( 450, 305, 100, 35, (255, 0, 0), text_size=23, text = 'Settings', text_color = (0, 0, 0)), Button( 450, 355, 100, 35, (255, 0, 0), text_size=23, text = 'Quit', text_color = (0, 0, 0))]
    help_buttons = [Button(20, 550, 200, 30, (255, 0, 0), text_size=23, text = 'Previous', text_color = (0, 0, 0)), Button( 805, 550, 200, 30, (255, 0, 0), text_size=23, text = 'Next', text_color = (0, 0, 0)), Button( 800, 20, 200, 30, (255, 0, 0), text_size=23, text = 'Back to main menu', text_color = (0, 0, 0))]
    action_hero_cam = 'enabled'
    settings_buttons = [Button(50, 150, 300, 30, (255, 0, 0), text_size=22, text = f'Action-hero cam:{action_hero_cam.title()}', text_color = (0, 0, 0)), Button(50, 190, 300, 30, (255, 0, 0), text_size=22, text = 'Reset High Score', text_color = (0, 0, 0)), Button( 800, 20, 200, 30, (255, 0, 0), text_size=22, text = 'Back to main menu', text_color = (0, 0, 0))]
    #page_num = 0
    game_name = 'CRazY CubE'  #'aCtIon CubE'

    

    while menu != False:

        pygame.Surface.fill(game_window, (0, 0, 0))

        font_creator(game_name, (255, 255, 255), game_window, 280, 10, bold = False , text_type = 'Impact', text_size = 100)

        #reading high score
        with open('high_scores.txt', 'r') as h_s:

            new_high_score = h_s.read().strip()

    
        for event in pygame.event.get():
    
            if event.type == pygame.QUIT: #quitting
                menu = False
                pygame.quit()
                break
    
            # TODO: able to hold down keys to move the player
    
            if event.type == pygame.MOUSEBUTTONDOWN:#Keydown events
                mousepos = pygame.mouse.get_pos()
    
                if menu == 'main menu':
                    
                    for _ in main_menu_buttons:
                        if _.check_cursor(mousepos):
                            #print("ok")
                            if _.text == 'Play':
                                #print("ok")
                                #window_is_open = True
                                main_game(action_hero_cam, int(new_high_score))

                            elif _.text == 'Help':
                                menu = 'help'
                                #page_num = 1
                                break

                            elif _.text == 'Settings':
                                menu = 'settings'
                                #page_num = 1
                                break

                            elif _.text == 'Quit':
                                menu = False
                                pygame.quit()
                                break

                            

                elif menu == 'help':
                    for _ in help_buttons:
                        if _.check_cursor(mousepos):
                            if _.text == 'Next':
                                _.text = 'No next page'

                            elif _.text == 'Previous':
                                _.text = 'No previous page'
                            elif _.text == 'Back to main menu':
                                menu = 'main menu'
                                help_buttons[0].text = 'Previous'
                                help_buttons[1].text = 'Next'
                                break

                elif menu == 'settings':
                    for _ in settings_buttons:
                        if _.check_cursor(mousepos):
                            #print("ok")
                            if _.text == f'Action-hero cam:{action_hero_cam.title()}':
                                if action_hero_cam == 'enabled':
                                   
                                    action_hero_cam = 'disabled'

                                else:
                                    #print("ok")
                                    action_hero_cam = 'enabled'
                                _.text = f'Action-hero cam:{action_hero_cam.title()}'
                            
                            elif _.text == 'Back to main menu':
                                menu = 'main menu'
                            elif _.text == 'Reset High Score':
                                with open('high_scores.txt', 'w') as high_score:
                                    high_score.write(str(0))



                                
                            
                            break




                                
                                
                
    
        if menu == 'main menu':
            font_creator("HIGH SCORE:", (255, 255, 255), game_window, 600, 150, bold = True , text_type = 'Small Fonts', text_size = 40)
            font_creator(new_high_score, (255, 255, 255), game_window, 810, 150, bold = True , text_type = 'Small Fonts', text_size = 40)
    
            for button in main_menu_buttons:
                button.draw_button(game_window)

                mousepos = pygame.mouse.get_pos()
                
                if button.check_cursor(mousepos):
                    button.color = (255, 255, 255)
                else:
                    button.color = (255, 0, 0) 
    
                
    
    
        elif menu == 'help':
    
            for button in help_buttons:
                button.draw_button(game_window)

                mousepos = pygame.mouse.get_pos()

                if button.check_cursor(mousepos):
                    button.color = (255, 255, 255)
                else:
                    button.color = (255, 0, 0) 

            with open('help_pages.txt') as help_pages:
                page = help_pages.readlines()
                #line_num = 0

            for _ in range(len(page)):
                #print(_)
                gap = _ * 19


                font_creator(page[_].strip(), (255, 255, 255), game_window, 50, 120 + gap, bold = False , text_type = 'Impact', text_size = 16)

        elif menu == 'settings':

            for button in settings_buttons:
                button.draw_button(game_window)

                mousepos = pygame.mouse.get_pos()

                if button.check_cursor(mousepos):
                    button.color = (255, 255, 255)
                else:
                    button.color = (255, 0, 0) 




    
    
    
    
        pygame.display.flip()


main_menu()





    
    
    
    
    
    
