## The city ##
The **city** is the playground where the simulation takes place.

It is a set of roads and roundabouts (accounting for crossroads), on which cars may travel. It is represented as an object (class `Track`, file `track.py`).

### Philosophy ###

### Saving and loading cities ###
Cities can be saved and recovered from files with the `Track_Parser` class (file `track.py`). The syntax required for those files is very simple :

  * It is a text file ;
  * In which each line may begin with `Road`, `Node` or `#` (comments) ;
  * Then, the following arguments should be provided, separated by a space or a comma :
    * `x, y, spawn_mode` (if the element is a `Node`) ;
    * `node_begin, node_end` (if the element is a `Road`).

Where :
  * `x` and `y` are integers representing the coordinates for the node ;
  * `spawn_mode` is an integer (either 0 or 1) indicating whether the node spawns cars ;
  * `node_begin` and `node_end` are integers representing the nodes' indices (the first node in the file has index 0) for the nodes the road connects.

**Caution** : the file should provide the nodes _before_ the roads, to avoid calling unreferenced nodes.
## The roads ##
The **roads** of our city are objects (class `Road`, file `init.py`) that act mainly as passive containers: they host cars and allow them to move freely, only providing basic informations (_e.g._ geometry, speed limit…) to them.

The roads are one-way only.

The roads also have two traffic lights - one at the beginning and one at the end.

### Main properties ###
  * `begin` : the `Node` from which the road departs.
  * `end  ` : the `Node` to which the road arrives.
  * `cars ` : a list of `Car` elements, representing all the cars on the road.
  * `gates` : a two-element list of `int` representing the current state of the traffic lights (0 : red, 1 : green)

### Secondary properties ###
  * `max_speed` : an `int` representing the speed limit for the road.
  * `gates_update` : a two-element list of `int` representing the time (in milliseconds) since the last update of the traffic lights.

## The roundabouts ##