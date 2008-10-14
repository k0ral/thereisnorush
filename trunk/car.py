# -*- coding: utf-8 -*-
"""
File        :   car.py
Description :   defines the class "Car"
"""

delta_t = 0.01  # TEMPORARY

from random import randint

from road import Road
from node import Node

class Car:
    """
    Those which will crowd our city >_< .
    """
    
    CAR_DEFAULT_LENGTH      = 5
    CAR_DEFAULT_WIDTH       = 4
    CAR_DEFAULT_HEADWAY     = CAR_DEFAULT_LENGTH    # marge de sécurité
    CAR_DEFAULT_SPEED       = 0
    CAR_DEFAULT_ACCEL       = 50
    CAR_DEFAULT_COLOR       = ( 64,  64, 255)

    def __init__(self, new_path, new_location, new_position = 0):
        """
        Constructor method : a car is provided a (for now unmutable) sequence of directions.
            new_path (list)  :   a list of waypoints
            new_road (Road) :   the road where the car originates (for now, let's forbid the original location to be a node)
        headway: Desired headway to the preceding car / Distance souhaitée par rapport à la voiture devant
        Définie par la liste de ses directions successives, pour le moment cette liste est fixe.
        """

        self.path           = new_path
        self.waiting        = False         
        self.length         = self.CAR_DEFAULT_LENGTH
        self.width          = self.CAR_DEFAULT_WIDTH
        self.speed          = self.CAR_DEFAULT_SPEED 
        self.position       = new_position               
        self.headway        = self.CAR_DEFAULT_HEADWAY
        self.color          = self.CAR_DEFAULT_COLOR 
        self.acceleration   = self.CAR_DEFAULT_ACCEL     
        self.location       = new_location

        if isinstance(new_location, Road):
            self.location = new_location
            self.location.cars.insert(0, self)
        else:
            print new_location
            raise ValueError('new_location should be a Road')
        
        self.generate_path()
    
    def generate_path(self):
        """
        Assembles random waypoints into a "path" list.
        """
        self.path = [randint(0, 128) for i in range(2000)]
    
    def join(self, new_location, new_position = 0):
        """
        Allocate the car to the given location. The concept of location makes it possible to use this code for either a road or a node.
            new_location    (Road or Node)  :   road or node that will host, if possible, the car
            new_position    (list)          :   position in the road or in the node (note that the meaning of the position depends on the kind of location)
        """
        
        if self.location and self in self.location.cars:
            self.location.cars.remove(self)
        
        self.position       =   new_position
        old_location        =   self.location
        self.location       =   new_location
        self.location.cars.insert(0, self)
        
        #   Each time a car joins or leaves a node, this one has to update in order to calculate again the best configuration for the gates
        if isinstance(old_location, Node):

            old_location.update_gates()
        elif isinstance(new_location, Node):

            new_location.update_gates()
        else:
            raise Exception('ERROR (in join()): the car is teleporting!')
    
    def die(self):
        """
        Kills the car, which simply disappear ; may be mostly used in dead-ends.
        """
        
        if self.location.cars:
            for car in self.location.cars:
                if car == self:
                   self.location.cars.remove(car)
    
    def next_way(self, read_only=False):
        """
        Expresses the cars' wishes :P
        """
        
        # TEMPORARY 
        if len(self.path) == 0:
            return 0
        else:
            if not read_only:
                del self.path[0]
            return self.path[0]

    def _next_obstacle(self, rank):
        """
        Returns the position of the obstacle ahead of the car
        """
        obstacle = 0
        obstacle_is_light = False
        if rank >= len(self.location.cars) - 1: 
            obstacle_is_light = True
            if self.location.gates[1]:
                # The traffic lights are green: go on (even a little bit further)
                obstacle = self.location.length + self.headway
            else:
                # They are red: stop
                obstacle = self.location.length
        else:
            obstacle_is_light = False
            obstacle = self.location.cars[rank + 1].position - self.location.cars[rank + 1].length / 2

        return obstacle, obstacle_is_light
    
    def _act_smartly(self, rank, obstacle, obstacle_is_light, next_position):
        #   No obstacle
        if next_position + self.length / 2 + self.headway < obstacle:
            # « 1 trait danger, 2 traits sécurité : je fonce ! »
            self.position = next_position
            
            if self.speed + self.acceleration * delta_t >= self.location.max_speed:
                self.speed = self.location.max_speed
            elif self.speed < self.location.max_speed:
                self.speed += self.acceleration * delta_t
            
            #   EXPERIMENTAL : accounting for the deceleration in front of an obstacle
            # There is a problem with this part: imho the car should not decelerate until either the car ahead does, or the traffic lights are red! Plus, this should be done using acceleration, not speed directly-- Sharayanan
            # I've done this because in real life, when a car arrives at a crossroad, it has to decelerate by security and because it cannot turn while moving so fast ; your second point is alright, but more difficult to implement -- Ch@hine
            if (self.position + self.speed * 30 * delta_t + self.length / 2 + self.headway > obstacle):
                if obstacle_is_light:
                    if self.speed > 5:
                        self.speed /= 1.5
                else:
                    if self.speed - self.location.cars[rank + 1].speed > 5:
                        self.speed = (self.speed - self.location.cars[rank + 1].speed) / 2 + self.location.cars[rank + 1].speed
        
        #   Obstacle = previous car
        elif not obstacle_is_light:
            # On s'arrête au prochain obstacle
            
            if not self.waiting:
                self.position = obstacle - self.length/2 - self.headway
            #CONVENTION SENSITIVE
            self.waiting = self.location.cars[rank + 1].waiting
            
            # EXPERIMENTAL : stop the car that is waiting 
            if self.waiting:
                self.speed = 0
        
        #   Obstacle = light
        elif next_position + self.length / 2 + self.headway >= obstacle:
            if self.location.gates[1]:
                # Everything's ok, let's go !
                self.waiting = False
                self.join(self.location.end)
            else:
                # We have a closed gate in front of us : stop & align
                self.position = self.location.length - self.headway - self.length / 2
                self.waiting = True

    def update(self, rank):
        """
        Updates the car speed and position, manages blocked pathways and queues.
            rank    (int)   :   position on the road (0 : last in)
        """
        
        # TODO :
        #       · (C.U1) resort to more "realistic" physics (e.g. acceleration, braking...)
        
        if not isinstance(self.location, Road):
            return None
        
        obstacle, obstacle_is_light = self._next_obstacle(rank)
        
        next_position = self.position + self.speed * delta_t

        self._act_smartly(rank, obstacle, obstacle_is_light, next_position)
        