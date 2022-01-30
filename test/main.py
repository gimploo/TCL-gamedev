#!/bin/python3

import pygame


# Display
print("GAME INITIALIZING")

pygame.display.init()
window = pygame.display.set_mode((800, 600))

PLAYER_WIDTH = 100
PLAYER_HEIGHT = 100

player = pygame.Rect((400,400,PLAYER_WIDTH,PLAYER_HEIGHT));


window_is_open = True

# Game loop
while window_is_open:

    # PLAYER INPUTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            window_is_open = False

        # TODO: able to hold down keys to move the player

        if event.type == pygame.KEYDOWN:

            if event.key== pygame.key.key_code('w'):
                player.y = player.y - 10
            if event.key == pygame.key.key_code('s'):
                player.y = player.y + 10

            if event.key == pygame.key.key_code('a'):
                player.x = player.x - 10
            if event.key == pygame.key.key_code('d'):
                player.x = player.x + 10

    # Fill the screen
    pygame.Surface.fill(window, (0,0,0))

    # TODO: rotate the player around its axis

    # Draw a rectangle
    pygame.draw.rect(window,(255,0,0),player)

    pygame.display.flip()


print("GAME CLOSED")
