# -*- coding: utf-8 -*-
"""
File        :   roundabout.py
Description :   defines the class "Roundabout"
"""

import constants    as __constants__
import init
from math           import pi
from pygame         import time
from random         import randint
from vector         import Vector
import car          as __car__

class Roundabout:
    """
    Crossroads of our city ; may host several roads.
    """

    def __init__(self, new_x, new_y, new_spawning=False, radius=__constants__.ROUNDABOUT_RADIUS_DEFAULT):
        """
        Constructor method : creates a new roundabout.
            new_coordinates (list) : the coordinates [x, y] for the roundabout
        """
        
        self.position       = Vector(__constants__.TRACK_SCALE * new_x + __constants__.TRACK_OFFSET_X, __constants__.TRACK_SCALE * new_y + __constants__.TRACK_OFFSET_Y)
        self.incoming_roads = []
        self.leaving_roads  = []
        self.max_cars       = __constants__.ROUNDABOUT_DEFAULT_MAX_CARS
        self.cars           = []
        self.slots_cars     = {}
        self.slots_roads    = [None for i in range(self.max_cars)]
        self.spawning       = new_spawning
        self.spawn_timer    = time.get_ticks()
        self.last_rotation  = time.get_ticks()
        self.rotation_speed = __constants__.ROUNDABOUT_DEFAULT_ROTATION_SPEED
        self.to_kill        = [] 
        
    def host_road(self, road):
        """
        Connecte, lors d'une initialisation, une route à un slot sur le carrefour.
        """
        if road in self.slots_roads:
            return None
        
        #   How many free slots there are
        total_free_slots = len([slot for slot in self.slots_roads if slot is None])

        if total_free_slots:
            #   Choose a random free slot to allocate for the road
            free_slots = [i for (i,slot) in enumerate(self.slots_roads) if slot is None]

            if free_slots:
                self.slots_roads[free_slots[0]] = road
                self.slots_cars[free_slots[0]]  = None
            else:
                raise Exception("WARNING: There is no slot to host any further roads!")
            
    def _update_gate(self, road):
        """
        Road-specific gate handling
            road (Road) : the road whose traffic ligths are to be handled
        """
        #   Too many waiting cars
        if road.total_waiting_cars > 8:
            #   Leaving road : do not send more cars in this road
            if road.begin == self:
                self.set_gate(road, False)

            #   Incoming road : give higher priority to this road
            elif road.end == self:
                self.set_gate(road, True)
                for other_road in self.incoming_roads:
                    if other_road.total_waiting_cars <= 8:
                        self.set_gate(other_road, False)
        
        #   Too long waiting time : open the gate and close others
        if road.last_gate_update(__constants__.LEAVING_GATE) > 10000 and not road.gates[__constants__.LEAVING_GATE] and road.total_waiting_cars:
            self.set_gate(road, True)

            for other_road in self.incoming_roads:
                if other_road.last_gate_update(__constants__.LEAVING_GATE) <= 10000 or not other_road.total_waiting_cars:
                     self.set_gate(other_road, False)
    
    def update_gates(self):
        """
        Manages the gates of the roads. This function will be the key part of the code, that's why it is called everytime
        """
        # CAUTION: this *has* to be in a separate loop !
        for road in self.incoming_roads:
            self._update_gate(road)
        
        #   Priority 0
        if self.is_full:
            for road in self.incoming_roads:
                self.set_gate(road, False)
            for road in self.leaving_roads:
                self.set_gate(road, True)
    
    def update_car(self, car):
        """
        Updates a given car on the roundabout 
        """
        
        if not(car.next_way(True) is None) and self.leaving_roads:
            next_way = car.next_way(True) % len(self.leaving_roads) # Just read the next_way unless you really go there
            car_slot = init.find_key(self.slots_cars, car)

            #   The car has lost its slot   
            if car_slot is None:
                raise Exception("ERROR (in roundabout.update_car()) : a car has no slot !")
            
            #   The car's slot is in front of a leaving road
            if self.slots_roads[car_slot] in self.leaving_roads:            
                if (self.leaving_roads[next_way].is_free) and self.slots_roads[car_slot] == self.leaving_roads[next_way]:
                #la route sur laquelle on veut aller est vidée et surtout _en face_  du slot de la voiture
                    car.join(self.leaving_roads[car.next_way(False) % len(self.leaving_roads)]) # cette fois on fait une lecture destructive

        #la voiture n'a pas d'endroit où aller : on la met dans le couloir de la mort
        else:
            self.to_kill.append(car)

    def update(self):
        """
        Updates the roundabout : rotate the cars, dispatch them...
        """
        #   Make the cars rotate
        if time.get_ticks() - self.last_rotation > __constants__.ROUNDABOUT_ROTATION_RATE:
            self.last_rotation = time.get_ticks()
            self.slots_roads = init.shift_list(self.slots_roads)
        
        #   Update gates
        self.update_gates()
        
        #   Spawning mode
        if self.spawning and len(self.leaving_roads) and (time.get_ticks() - self.spawn_timer > __constants__.SPAWN_TIME):
            self.spawn_timer = time.get_ticks()
            chosen_road = self.leaving_roads[randint(0, len(self.leaving_roads) - 1)]
            if chosen_road.is_free:
                new_car = __car__.Car(chosen_road)
        
        #   Update cars
        for car in self.cars:
            self.update_car(car)
        
        #   Kill cars that have reached their destination
        for car in self.to_kill:
            car_slot = init.find_key(self.slots_cars, car)
            self.slots_cars[car_slot] = None
            car.die()

        self.to_kill = []
    
    def set_gate(self, road, state):
        """
        Sets the state of the gates on the road.
            road    (Road)  :   the road whose gates are affected
            state   (bool)   :   the state (False = red, True = green) of the gate
        """
        #   Leaving road
        if (id(road.begin) == id(self)):
            if road.gates[__constants__.INCOMING_GATE] != state:
                road.gates[__constants__.INCOMING_GATE] = state
                if road.gates[__constants__.INCOMING_GATE] != state: road.gates_update[__constants__.INCOMING_GATE] = time.get_ticks()
        
        #   Incoming road
        else:
            if road.gates[__constants__.LEAVING_GATE] != state:
                road.gates[__constants__.LEAVING_GATE] = state
                if road.gates[__constants__.LEAVING_GATE] != state: road.gates_update[__constants__.LEAVING_GATE] = time.get_ticks()

    @property
    def is_full(self):
        """
        Returns whether there is no place left on the roundabout.
        """
        return (len(self.cars) >= self.max_cars)

    @property
    def total_waiting_cars(self):
        """
        Returns the number of cars waiting on all the incoming roads connected to this roudabout.
        """
        total = 0
        for road in self.incoming_roads:
            total += road.total_waiting_cars

        return total