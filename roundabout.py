﻿# -*- coding: utf-8 -*-
"""
File        :   roundabout.py
Description :   defines the class "Roundabout"
"""

import lib
import time

from vector         import Vector

import car          as __car__
import constants

class Roundabout:
    """
    Crossroads of our city ; may host several roads.
    """

    def __init__(self, 
                 new_x, 
                 new_y, 
                 new_spawning = False, 
                 radius       =constants.ROUNDABOUT_RADIUS_DEFAULT):
        """
        Constructor method : creates a new roundabout.
            new_coordinates (list) : the coordinates [x, y] for the roundabout
        """
        
        self.position       = Vector(constants.TRACK_SCALE * new_x + constants.TRACK_OFFSET_X, 
                                     constants.TRACK_SCALE * new_y + constants.TRACK_OFFSET_Y)
        self.radius         = radius
        
        self.incoming_roads = []
        self.leaving_roads  = []
        self.cars           = []
        self.to_kill        = [] 
        self.slots_cars     = {}
        
        self.max_cars       = constants.ROUNDABOUT_DEFAULT_MAX_CARS
        self.rotation_speed = constants.ROUNDABOUT_DEFAULT_ROTATION_SPEED
        
        self.spawning       = new_spawning
        self.spawn_timer    = time.clock()
        self.last_shift     = time.clock()
        
        self.slots_roads    = [None for i in range(self.max_cars)]
        self.selfish_load   = 0

        
    def host_road(self, road):
        """
        Connects a road to a slot, must be called during initialization.
        Connecte, lors d'une initialisation, une route à un slot sur le carrefour.
        """
        
        if road in self.slots_roads:
            return None
        
        # List of free slots  How many free slots there are
        free_slots = [i for (i, slot) in enumerate(self.slots_roads) if slot is None]

        if len(free_slots) > 0:
            #   Choose a random free slot to allocate for the road
            self.slots_roads[free_slots[0]] = road
            self.slots_cars[free_slots[0]]  = None
        else:
            raise Exception("ERROR (in Roundabout.host_road()) : there is no slot to host any further roads !")
            
    def _update_traffic_lights(self):
        """
        Gate handling
        """

        #First, let's have a global view of situation 
        around_incoming_loads, around_leaving_loads = [], []
        for road in self.incoming_roads:
            around_incoming_loads.append(road.begin.load)
            if road.begin.load > self.load and road.traffic_lights[constants.ENTRANCE]: #rond point chargé et qui laisse ses voitures se deverser vers moi
                self.set_gate(road, True)
            elif road.begin.load < self.load and abs((road.begin.load - self.load)/(self.load+0.001)) > 0.10 : #rondpoint vraiment pas chargé , je coupe
                self.set_gate(road, False)
                
        for road in self.leaving_roads:
            around_leaving_loads.append(road.end.load)
            if road.end.load < self.load and road.traffic_lights[constants.EXIT]: #rond point pas trop chargé et qui laisse passer mes voitures: j'ouvre
                self.set_gate(road, True)
            elif road.end.load > self.load and abs((road.begin.load - self.load)/(self.load+0.001)) > 0.10: #rondpoint bien chargé, je le laisse respirer
                self.set_gate(road, False)
        
        #Then, let's update each road, few rules because the general view overrules the local one.
        
        for road in self.incoming_roads:
            #   Too long waiting time : open the gate and not close others
            if road in self.incoming_roads and road.last_gate_update(constants.EXIT) > constants.WAITING_TIME_LIMIT and road.total_waiting_cars:
                self.set_gate(road, True)

        #   Full roundabout : close all incoming roads, open all leaving roads
        #ceci est inutile depuis que les voitures ne s'insère plus dans les slots pleins (sinon l'application de ce procédé ruine un peu le systeme de load)
        #if self.is_full:
        #    for road in self.incoming_roads:
        #        self.set_gate(road, False)
        #    for road in self.leaving_roads:
        #        self.set_gate(road, True)
        
 

    def update_car(self, car):
        """
        Updates a given car on the roundabout 
        """
        
        if not(car.next_way(True) is None) and self.leaving_roads:
            next_way = car.next_way(True) % len(self.leaving_roads) # Just read the next_way unless you really go there
            car_slot = lib.find_key(self.slots_cars, car)

            #   The car has lost its slot   
            if car_slot is None:
                raise Exception("ERROR (in Roundabout.update_car()) : a car has no slot !")
            
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
        if time.clock() - self.last_shift > constants.ROUNDABOUT_ROTATION_RATE:
            self.last_shift = time.clock()
            self.slots_roads = lib.shift_list(self.slots_roads)

        #   Spawning mode
        if self.spawning and len(self.leaving_roads) and (time.clock() - self.spawn_timer > constants.SPAWN_TIME):
            self.spawn_timer = time.clock() 
            num_possible_roads    = len(self.leaving_roads)
            # Possible ways out. NB : the "1000/ " thing ensures *integer* probabilities.
            possible_roads_events = [(self.leaving_roads[i], 1000/num_possible_roads) for i in range(num_possible_roads)]
        
            chosen_road = lib.proba_poll(possible_roads_events)
            if chosen_road.is_free:
                car_type_events = [(constants.STANDARD_CAR, 80), 
                                   (constants.TRUCK       , 15), 
                                   (constants.SPEED_CAR   ,  5)]
                                   
                new_car = __car__.Car(chosen_road, lib.proba_poll(car_type_events))

        #   Update traffic lights
        self._update_traffic_lights()
                
        #   Update cars
        for car in self.cars:
            self.update_car(car)
        
        #   Kill cars that have reached their destination
        for car in self.to_kill:
            car_slot = lib.find_key(self.slots_cars, car)
            self.slots_cars[car_slot] = None
            car.die()

        self.to_kill = []
    
    def set_gate(self, road, state):
        """
        Sets the state of the traffic lights on the road.
            road    (Road)  :   the road whose traffic lights are affected
            state   (bool)   :   the state (False = red, True = green) of the gate
        """
        #   Set which gate is to be updated
        if id(road.begin) == id(self):
            current_gate = constants.ENTRANCE
        else:
            current_gate = constants.EXIT
        
        #   Update if necessary
        if road.traffic_lights[current_gate] != state:
            road.traffic_lights_update[current_gate] = time.clock()
            road.traffic_lights[current_gate]        = state

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

    @property
    def selfish_load(self):
        """
        Returns in per cent a number called load (inspired by the load of a Linux station)
        """
        length_sum = sum([road.length for road in self.incoming_roads])
        self.selfish_load = self.total_waiting_cars*50/(length_sum+1) +  len(self.cars)*50 / self.max_cars

    @property
    def load(self):
        load = self.selfish_load
        for road in self.incoming_roads:
            load += road.begin.selfish_load / road.length
        for road in self.leaving_roads:
            load += road.end.selfish_load / road.length
        return load
