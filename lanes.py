"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

Likita Gangireddy lg425
12/21/2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _exitSound: Sound to play when frog reaches an exit
    # Invariant: _exitSound is a Sound Object that refers to the TRILL_SOUND
    # audio file
    #
    # Attribute _objects_json: json dictionary of objects
    # Invariant: _objects_json is a a valid json dictionary that refers to the
    # specific objects that are in a particular level.
    #
    # Attribute _bluefrog: list of safe frogs
    # Invariant: _bluefrog is a list of GImages that keeps track of the safe
    # frog objects
    #
    # Attribute _tiles: list of lanes in a level
    # Invariant: _tiles is a list of GTiles that corresponds to the number
    # of lanes in a level.
    #
    # Attribute _json: A json dictionary with level information
    # Invariant: _json is a valid json dictionary that provides information
    # about a particular level file.
    #
    # Attribute _obj: A list of the objects in a level
    # Invariant: _obj is a list of GImages, with one entry for each object in a
    # Level
    #
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getObjects(self):
        """
        Returns the list of object GImages
        """
        return self._obj

    def getbluefrog(self):
        """
        Returns the list of blue frog GImages
        """
        return self._bluefrog

    def __init__(self, objects_json, json, tiles):
        """
        Initializes a Lane.

        This Initializer takes in a json dictionary of the objects in a specific
        level, the json dictionary for general information about the level, and
        the list GTiles in the level, in order to initialize a lane object.

        A GImage is created for each image and appended to a list of objects.
        The objects in this class are considered composite objects because the
        objects consist of both GTiles and GImages, where the GImages are drawn
        on top of the GTiles.

        Parameter objects_json: A json dictionary of objects
        Precondition: objects_json is a valid json dictionary that refers to the
        specific objects that are in a particular level.

        Parameter json: A json dictionary with level information
        Precondition: json is a valid json dictionary that provides information
        about a particular level file.

        Parameter tiles: list of lanes in a level.
        Precondition: tiles is a list of GTiles that corresponds to the number
        of lanes in a level.
        """
        self._exitSound = Sound(TRILL_SOUND)
        self._objects_json = objects_json
        images = self._objects_json['images']
        self._bluefrog=[]
        self._tiles = tiles
        self._json = json
        lanes = self._json['lanes']
        self._obj = []
        for item in lanes:
            if 'objects' in item:
                list_of_objects = item['objects']
                for dictionary in list_of_objects:
                    type_object = dictionary['type']
                    position_object = dictionary['position']
                    source = type_object + '.png'
                    x = (position_object*GRID_SIZE)+(GRID_SIZE//2)
                    y = (lanes.index(item)*GRID_SIZE)+(GRID_SIZE//2)
                    if 'speed' in item:
                        if item['speed']>=0:
                            angle = 0
                        elif item['speed']<0:
                            angle = 180
                    else:
                        angle = 0
                    hitbox = images[source[:-4]]['hitbox']
                    object = GImage(x=x,y=y,source=source, angle=angle,
                    hitbox = hitbox)
                    self._obj.append(object)

    def update(self, dt, frog):
        """
        Updates the obstacles and returns 'reached exit' if frog has reached
        the exit.

        This method moves each obstacle in the list of objects based on their
        respective speeds. This method also takes into account the length of the
        buffer that the object moves off screen, in order to prevent collison
        of objects. If the frog has reached an exit, this method will return
        'reached exit'.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is an number >= 0

        Parameter frog: the frog
        Precondition: frog is an object of the Frog class.
        """
        buffer = self._json['offscreen']
        width = self._tiles[0].width
        lanes = self._json['lanes']
        list_of_speeds=[]
        for item in lanes:
            if 'speed' in item and 'objects' in item:
                for obstacle in item['objects']:
                    list_of_speeds.append(item['speed'])
            elif 'objects' in item:
                for obstacle in item['objects']:
                    list_of_speeds.append(0)
        for obstacle in range(len(self._obj)):
            if self._obj[obstacle].x < buffer*GRID_SIZE*-1:
                d = (self._obj[obstacle].x)-(buffer*GRID_SIZE*-1)
                self._obj[obstacle].x=(width)+((buffer*GRID_SIZE)+d)
            if self._obj[obstacle].x > width+(buffer*GRID_SIZE):
                d = (self._obj[obstacle].x)-(width+(buffer*GRID_SIZE))
                self._obj[obstacle].x=(buffer*GRID_SIZE*-1)+d
            else:
                item_speed=(list_of_speeds[obstacle]*dt)
                self._obj[obstacle].x=self._obj[obstacle].x + item_speed
        if self._reachedexit(frog)=='reached exit':
            return 'reached exit'

    def draw(self, view):
        """
        Draws the tiles and obstacles to the view

        Parameter view: The view to draw to
        Precondition: view is a GView object
        """
        for tile in self._tiles:
            tile.draw(view)

        for obstacle in self._obj:
            obstacle.draw(view)

    def checkWin(self):
        """
        Returns 'game won' if all of the exits are occupied with safe frogs.

        This method creates a list of exits, and also creates a list of exits
        that are occupied by blue frogs. When all of the exits are occupied,
        this occurs when the length of exits is the same as the length of taken
        exits, this method will return 'game won'
        """
        exits = []
        for x in self._obj:
            if x.source == 'exit.png':
                exits.append(x)
        taken=[]
        for x in exits:
            for y in self._bluefrog:
                if x.contains((y.x, y.y)):
                    taken.append('taken')
        if len(taken)==len(exits):
            return 'game won'

    def _reachedexit(self, frog):
        """
        Returns "reached exit" if the frog has reached an exit.

        This method identifies if an exit contains the frog, and if this
        condition is met, it will play the exit sound, add a safe frog to the
        list of blue frogs, and return "reached exit"

        Parameter frog: the frog
        Precondition: frog is an object of the Frog class.
        """
        for x in self._obj:
            if frog is not None:
                if x.source =='exit.png' and x.contains((frog.x, frog.y)):
                    self._exitSound.play()
                    self._bluefrog.append(GImage(x=x.x,y=x.y,source=FROG_SAFE))
                    return "reached exit"

                    
