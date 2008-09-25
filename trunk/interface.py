#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pygame   # http://www.pygame.org
import init     # ./init.py

# Colors

black = (  0,   0,   0)
red   = (255,   0,   0)
green = (  0, 255,   0)
blue  = (  0,   0, 255)
white = (255, 255, 255)

light_red   = (255,  64,  64)
light_green = ( 64, 255,  64)
light_blue  = ( 64,  64, 255)

# Settings

size = width, height = (320, 240)            # Screen resolution

global screen                                # Screen object
global sim_running                           # Indicates whether the simulation is running
global debug                                 # Indicates whether debugging messages are displayed

screen = pygame.display.set_mode(size)       # Sets drawing surface
debug = True

# Node general properties
node_width  = 4
node_height = 4
node_color = red

# Car general properties
car_width  = 4
car_height = 4
car_color = green

# Road general properties
road_color = white

def init_display():
    pygame.init()                                             # Pygame initialization 
    pygame.display.set_caption("Thereisnorush (unstable)")    # Sets window caption

def draw_node(node):
    """
    Draws a given node on the screen.
        node (node) : the aforementioned node.
    """
    pt_topleft     = (node.x - node_width / 2 , node.y - node_height / 2 )
    pt_bottomright = (node_width, node_height)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.rect(screen, node_color, rectangle, 0)

def draw_car(car):
    """
    Draws a given car on the screen.
        car (car) : the aforementioned car.
    """
    
    xd, yd = car.road.begin.coords() # i like this OO call !
    xa, ya = car.road.end.coords()

    length_covered = car.pos * 100 / car.road.length
    x_position = xd + (xa - xd ) * length_covered / 100
    y_position = yd + (ya - yd ) * length_covered / 100
    pt_topleft     = (x_position - car_width / 2 , y_position - car_height / 2 )
    pt_bottomright = (car_width, car_height)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.rect(screen, car_color, rectangle, 0)

def draw_road(road):
    """
    Draws a given road on the screen and all the cars on it.
        road (road) : the aforementioned road.
    """
    pt_topleft     = (road.begin.x, road.begin.y)
    pt_bottomright = (road.end.x,   road.end.y)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.line(screen, road_color, pt_topleft, pt_bottomright, 1)
    
    for car in road.cars: draw_car(car)
    
def draw_scene():
    """
    Draws the complete scene on the screen
    """
    # Clear background  
    screen.fill(black)

    # First, draw the nodes, then draw the roads, with the cars on them
    for node in init.circuit.nodes: draw_node(node)
    for road in init.circuit.roads: draw_road(road)
    # Saves and displays
    pygame.display.flip()

def main_loop():
    """
    Main loop : keeps updating and displaying the scene forever,
                unless somebody hits Esc.
    """
    # Main loop

    sim_running = True

    while sim_running:
        # Check the users' actions
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sim_running = False
        
        # Draw the scene
        draw_scene()
        
    # End of simulation instructions
    pass
    
# Bootstrap

if (__name__ == "__main__"):
    # Before simulation instructions
    pass
    init_display()
    # Main loop
    main_loop()

# Don't write anything after that !
