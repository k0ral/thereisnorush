# -*- coding: utf-8 -*-
"""
File          :   init.py
Description   :   defines the classes and constants needed for the simulation
ToDo          :   · Rewrite update() to account for tunnelling and crossing a node
"""

import string #   standard python library

#   Useful constants

BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
BLUE        = (  0,   0, 255)
WHITE       = (255, 255, 255)

LIGHT_RED   = (255,  64,  64)
LIGHT_GREEN = ( 64, 255,  64)
LIGHT_BLUE  = ( 64,  64, 255)

RESOLUTION  = (WINDOW_WIDTH, WINDOW_HEIGHT) = (512, 384)

NODE_WIDTH  = 4
NODE_HEIGHT = 4
NODE_COLOR  = RED

CAR_WIDTH   = 4
CAR_HEIGHT  = 4
CAR_COLOR   = GREEN

ROAD_COLOR  = WHITE

NODE = "NODE"
ROAD = "ROAD"

class Track:
    """
    Our city model : a mathematical graph made of nodes, linked to each other by roads.
    """
   
    def __init__(self, new_nodes = None, new_roads = None):
        """
        Constructor method : creates a track given the nodes and roads.
            new_nodes (list) :   a list of the nodes
            new_roads (list) :   a list of the roads
        """ 
        if new_nodes is None:
            self.nodes = []
        else:
            self.nodes = new_nodes
        if new_roads is None:
            self.roads = []
        else:
            self.roads = new_roads

    def add_track_element(self, elements):
    
        """
        Adds an element to the track, once it's been checked and validated.
            elements    (list)      :   a list describing the element [type, arg1, arg2…]
        """
        
        if (elements[0] == NODE):
            #self.add_node([elements[1], elements[2]])
            self.nodes.append(Node([elements[1], elements[2]]))
        elif (elements[0] == ROAD):
            self.create_road(self.nodes[elements[1]], self.nodes[elements[2]], elements[3])
        else:
            # Should never be reached: something went wrong
            print "An error occured when loading the file."
            pass

    def get_lines(self, filename):
        """
        Reads a file and returns a list of its lines.
            filename    (string)    :   the complete name of the file to be read
        """
        
        filedata    = open(filename)
        lines       = []

        for line in filedata:
            lines += [line.strip()]

        return lines
        
    def track_line_parse(self, line):
        """
        Parses a line in a track description file.
            line    (string)    :   the line of text to be parsed
        """
        
        elements    = string.replace(string.upper(line), ",", " ").split()
        kind        = ""
        total_arguments     = 0

        # Get element type
        if len(elements) != 0:
            kind = elements[0]

        # Define how many arguments are to expect
        if (kind == NODE):
            total_arguments = 2
        elif (kind == ROAD):
            total_arguments = 3
        else:
            # Empty element or incorrect data
            print "Error during parsing: unknown element type '" + kind + "'."
            pass

        # Check whether the arguments are corrects
        if (len(elements) == 1 + total_arguments):
            # The line is correct, let's convert them and add the element !
            try:
                # Convert arguments to int and add the element
                for i in range(total_arguments):
                    elements[i + 1] = int(elements[i + 1])
                self.add_track_element(elements)
            except Exception, exc:
                # Ill-formed element
                print "Error parsing line : "
                print elements
                print exc 
                pass
        else:
            # The line is incorrect
            print "Incorrect line : "
            print elements
            pass

    def load_track_from_file(self, filename):
        """
        Loads a track from a textfile, checks its validity, parses it
        and loads it in the simulation.
            filename    (string)    :   the name of the file to load.
        """

        try:
            # Attempts to load & read the file
            lines = self.get_lines(filename)
        except Exception, exc:
            # The file doesn't exists or any other error
            print "The file " + filename + " cannot be loaded."
            print exc 
            pass
        for line in lines:
            self.track_line_parse(line)
            
    def create_road(self, new_begin, new_end, new_length):
        """
        Adds a road to the track.
            new_begin  (Node)    :   starting point for the road
            new_end    (Node)    :   ending point for the road
            new_length (int)     :   road length
        """
        
        if len(self.roads) == 0: self.roads = []
      
        self.roads += [Road(new_begin, new_end, new_length)]
        new_begin.add_road(self, False)
        new_end.add_road(self, True)

class Road:
    """
    Connection between 2 nodes ; one-way only.
    """
    
    def __init__(self, new_begin, new_end, length):
        """
        Constructor method : creates a new road.
            new_begin  (Node)    : starting point for the road
            new_end    (Node)    : ending point for the road
            new_length (int)     : road length
        """
        
        self.begin  = new_begin
        self.end    = new_end
        self.cars   = [] 
        self.length = length
        self.gates  = [False, False]
    
    def update(self):
        queue_length = len((self.cars))

        for i in range(queue_length):
            self.cars[-i-1].update(queue_length-(i+1))

    def add_car(self, new_car, new_position):
        """
        Inserts a car at given position in the ordered list of cars.
            new_car      (Car)   :   car to be added
            new_position (float) :   curvilinear abscissa for the car
        """

        if len(self.cars) == 0:
            self.cars = []
        
        self.cars        =  [new_car] + self.cars
        new_car.position =   new_position
        new_car.road     =   self


class Node:
    """
    Crossroads of our city ; may host several roads.
    """
    
    def __init__(self, new_coordinates):
        """
        Constructor method : creates a new node.
            new_coordinates (list) : the coordinates [x, y] for the node
        """
        self.roads         = []
        self.x             = new_coordinates[0]
        self.y             = new_coordinates[1]
        self.roads_coming   = []
        self.roads_leaving  = []

    @property
    def coords(self):
        return (self.x, self.y)

   
    def add_road(self, road, is_coming):
        """
        Connect a road to this node.
            road        (Road)  :   the road object to be connected
            is_coming    (bool) :   True if the roads comes to this node, False otherwise
        """
        
        if is_coming:
            self.roads_coming    += [road]
        else:
            self.roads_leaving   += [road]
    
    def set_gate(self, road, state):
        """
        Sets the state of the gates on the road.
            road    (Road)  :   the road whose gates are affected
            state   (int)   :   the state (0 = red, 1 = green) of the gate
        """
        
        if (id(road.begin) == id(self)):
            road.gates[0] = state
        else:
            road.gates[1] = state
            
class Car:
    """
    Those which will crowd our city >_< .
    """
    
    def generate_path(self):
        """
        Assembles random waypoints into a "path" list
        """
        
        from random import randint
        
        total_waypoints  = randint(5, 18)
        path            = []
        
        for i in range(total_waypoints):
            path += [randint(1, 100)]
        
        return path
    
    
    def __init__(self, newPath, new_road):
        """
        Constructor method : a car is provided a (for now unmutable) sequence of directions.
            newPath (list)  :   a list of waypoints
            new_road (Road)  :   the road where the car originates
        
        Définie par la liste de ses directions successives, pour le moment cette liste est fixe.
        """
        
        self.path       = newPath
        # For now, the cars' speed is either 0 or 100
        # Cette « vitesse » est pour le moment 0 ou 100, ce sont des « point de deplacements »
        self.speed      = 0
        self.position   = 0
        self.road       = new_road
    
    def update(self, rang):
        """
        Updates the car speed and position, manages blocked pathways and queues.
            rang    (int)   :   position on the road (0 : last in)
        """

        #TEMPORARY
        delta_t = 0.01
        
        if rang == len(self.road.cars) - 1 : 
            obstacle = None #light
        else:
            obstacle = self.road.cars[rang + 1].position 
        
        self.speed = 50
        
        if self.position + self.speed*delta_t < obstacle:
            self.position += self.speed * delta_t
        elif obstacle != None:
            self.position = obstacle - CAR_WIDTH
            self.speed = 0
        else:
            #on oublie les histoires de feu rouge pour le moment : la voiture s'arrête.
            self.position = self.road.length -1
            self.speed = 0
            


#   TESTING ZONE

if (__name__ == '__main__'):
    pass

# Temporary testing zone

track = Track()
track.load_track_from_file("track_default.txt")
track.roads[1].add_car(Car([], track.roads[2]), 80)
track.roads[1].add_car(Car([], track.roads[1]), 30)
track.roads[1].add_car(Car([], track.roads[1]), 130)