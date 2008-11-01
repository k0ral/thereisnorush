# -*- coding: utf-8 -*-
"""
File        :   constants.py
Description :   defines the constants
"""

#   Revision information

REVISION_NUMBER = 122
REVISION_NAME   = 'Thereisnorush (testing)'

#   Colors (R, G, B, [Alpha])
BLACK       =   0,   0,   0
RED         = 255,   0,   0
GREEN       =   0, 255,   0
BLUE        =   0,   0, 255
WHITE       = 255, 255, 255
GRAY        = 190, 190, 190
ORANGE      = 255, 128,   0

LIGHT_RED   = 255,  64,  64
LIGHT_GREEN =  64, 255,  64
LIGHT_BLUE  =  64,  64, 255

TRANSPARENT = 0, 0, 0, 0

#   Available vehicle features
DEFAULT_LENGTH      = 0
DEFAULT_WIDTH       = 1
DEFAULT_HEADWAY     = 2
DEFAULT_SPEED       = 3
DEFAULT_FORCE       = 4
DEFAULT_MASS        = 5
DEFAULT_COLOR       = 6

#   Available vehicle types
STANDARD_CAR    = 0
SPEED_CAR       = 1
TRUCK           = 2
VEHICLE_TYPES   = [STANDARD_CAR, SPEED_CAR, TRUCK]

#   Vehicle specification
VEHICLE                 = {}

#   Standard car
VEHICLE[STANDARD_CAR]   = {}
VEHICLE[STANDARD_CAR][DEFAULT_LENGTH]   = 5
VEHICLE[STANDARD_CAR][DEFAULT_WIDTH]    = 4
VEHICLE[STANDARD_CAR][DEFAULT_HEADWAY]  = VEHICLE[STANDARD_CAR][DEFAULT_LENGTH]
VEHICLE[STANDARD_CAR][DEFAULT_SPEED]    = 0
VEHICLE[STANDARD_CAR][DEFAULT_FORCE]    = 10.0
VEHICLE[STANDARD_CAR][DEFAULT_MASS]     = 1.0
VEHICLE[STANDARD_CAR][DEFAULT_COLOR]    = WHITE

#   Speed car
VEHICLE[SPEED_CAR]      = {}
VEHICLE[SPEED_CAR][DEFAULT_LENGTH]  = VEHICLE[STANDARD_CAR][DEFAULT_LENGTH]
VEHICLE[SPEED_CAR][DEFAULT_WIDTH]   = VEHICLE[STANDARD_CAR][DEFAULT_WIDTH]
VEHICLE[SPEED_CAR][DEFAULT_HEADWAY] = VEHICLE[STANDARD_CAR][DEFAULT_HEADWAY]
VEHICLE[SPEED_CAR][DEFAULT_SPEED]   = VEHICLE[STANDARD_CAR][DEFAULT_SPEED]
VEHICLE[SPEED_CAR][DEFAULT_FORCE]   = VEHICLE[STANDARD_CAR][DEFAULT_FORCE] * 5
VEHICLE[SPEED_CAR][DEFAULT_MASS]    = VEHICLE[STANDARD_CAR][DEFAULT_MASS] / 1.5
VEHICLE[SPEED_CAR][DEFAULT_COLOR]   = LIGHT_RED

#   Truck
VEHICLE[TRUCK]          = {}
VEHICLE[TRUCK][DEFAULT_LENGTH]  = VEHICLE[STANDARD_CAR][DEFAULT_LENGTH]
VEHICLE[TRUCK][DEFAULT_WIDTH]   = VEHICLE[STANDARD_CAR][DEFAULT_WIDTH]
VEHICLE[TRUCK][DEFAULT_HEADWAY] = VEHICLE[STANDARD_CAR][DEFAULT_HEADWAY]
VEHICLE[TRUCK][DEFAULT_SPEED]   = VEHICLE[STANDARD_CAR][DEFAULT_SPEED]
VEHICLE[TRUCK][DEFAULT_FORCE]   = VEHICLE[STANDARD_CAR][DEFAULT_FORCE] * 5
VEHICLE[TRUCK][DEFAULT_MASS]    = VEHICLE[STANDARD_CAR][DEFAULT_MASS] * 5
VEHICLE[TRUCK][DEFAULT_COLOR]   = LIGHT_BLUE

#   Track
TRACK_OFFSET_X = 32
TRACK_OFFSET_Y = 32
TRACK_SCALE    = 3.5

#   Roundabout
ROUNDABOUT_WIDTH                  = 3
ROUNDABOUT_HEIGHT                 = 3
ROUNDABOUT_COLOR                  = RED
ROUNDABOUT_RADIUS_DEFAULT         = 10
ROUNDABOUT_DEFAULT_ROTATION_SPEED = 10
ROUNDABOUT_ROTATION_RATE          = 0.500
ROUNDABOUT_DEFAULT_MAX_CARS       = 5

#   Road
ROAD_COLOR             = WHITE
ROAD_DEFAULT_MAX_SPEED = 50
ROAD_DEFAULT_LENGTH    = 100
ROAD_DEFAULT_WIDTH     = 5

#   Rules
WAITING_CARS_LIMIT = 8
WAITING_TIME_LIMIT = 10.000

#   Other
SCENE_RESOLUTION    = (SCENE_WIDTH, SCENE_HEIGHT)   = (1000, 750)
PANEL_RESOLUTION    = (PANEL_WIDTH, PANEL_HEIGHT)   = (200, 500)
delta_t             = 0.1

DISPLAY_DENSITY     = False # You may de-activate per-density coloring (+ fps)

EXIT     = 1
ENTRANCE = 0
SPAWN_TIME      = 2.0
