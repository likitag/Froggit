"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

Likita Gangireddy lg425
12/21/2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE

    # Attribute _deathSound: Sound to play when frog dies
    # Invariant: _deathSound is a Sound Object that refers to the SPLAT_SOUND
    # audio file
    #
    # Attribute _death: frog death animation
    # Invariant: _death is a Death object, or None
    #
    # Attribute _comp: composite object
    # Invariant: _comp is a Lane object that corresponds to a particular lane,
    # or it is set to None
    #
    # Attribute _win: indicates if the game has been won
    # Invariant: _win is set to 'win' if the game has been won, else it is set
    # to None
    #
    # Attribute _reachexit: indicates whether the frog has reached an exit
    # Invariant: _reachexit is set to 'yes' if the frog has reached an exit,
    # else it is set to None
    #
    # Attribute _objects_json: A json dictionary of objects
    # Invariant: _objects_json is a valid json dictionary of objects in a
    # particular level file
    #
    # Attribute _sprites: A dictionary of sprite information.
    # Invariant: _sprites is a valid dictionary of sprite information retrieved
    # from _objects_json
    #
    # Attribute _json: json dictionary for level file
    # Invariant: _json is a valid json dictionary that provides information
    # about a particular level file.
    #
    # Attribute _width: width of level
    # Invariant: _width is an int that corresponds to the width of the level
    #
    # Attribute _fullheight: height of the level
    # Invariant: _fullheight is an int that corresponds to the height of the
    # level
    #
    # Attribute _height: height of level not including top row
    # Invariant: _height is an int that corresponds to the height of the level
    # not including the top row, which is reserved to display the lives
    #
    # Attribute _lanes: the lanes in the level
    # Invariant: _lanes is a list of GTiles
    #
    # Attribute _frogstartx: frog starting x position
    # Invariant: _frogstartx is an int that corresponds to the starting x
    # position of the frog.
    #
    # Attribute _frogstarty: frog starting y position
    # Invariant: _frogstarty is an int that corresponds to the starting y
    # position of the frog.
    #
    # Attribute _froglives: indicates the number of lives left
    # Invariant: _froglives is a list of GImages, whose length is between zero
    # and three, inclusive
    #
    # Attribute _liveslabel: label that says 'Lives:'
    # Invariant: _liveslabel is a GLabel with the text 'Lives:'
    #
    # Attribute _open_or_exit: list of opens and exits
    # Invariant: _open_or_exit is a list of objects with the source 'open.png'
    # or 'exit.png'
    #
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getFrog(self):
        """
        Returns the frog

        The frog is a Frog object.
        """
        return self._frog

    def setFrog(self, x, y):
        """
        Sets the frog to its starting position.

        Parameter x: The starting x position of the frog.
        Precondition: x is an int that refers to the starting x position of
        the frog

        Parameter y: The starting y position of the frog.
        Precondition: y is an int that refers to the starting y position of the
        frog.
        """
        self._frog = Frog(x,y, self._sprites)

    def setDeath(self, x, y):
        """
        Sets the death.

        Parameter x: The x position of the frog's death.
        Precondition: x is an int that corresponds to the x postion of the frog
        when it died.

        Parameter y: The y position of the frog's death.
        Precondition: y is an int that corresponds to the y postion of the frog
        when it died.
        """
        self._death = Death(x,y, self._sprites)

    def getFrogstartX(self):
        """
        Returns the frog's starting x position.
        """
        return self._frogstartx

    def getFrogstartY(self):
        """
        Returns the frog's starting y position.
        """
        return self._frogstarty

    def getFroglives(self):
        """
        Returns the frog lives.
        """
        return self._froglives

    def setFroglives(self, value):
        """
        Sets the frog lives.

        Parameter value: The lives left for the game
        Precondition: value is a list of GImages, and is the same length as
        the number of lives left in the game.
        """
        self._froglives = value

    def getReachexit(self):
        """
        Returns 'yes' if the frog has reached the exit, else it Returns None
        """
        return self._reachexit

    def setReachexit(self, value):
        """
        Sets reach exit.

        Parameter value: Indicates if the frog has reached an exit.
        Precondition: value is 'yes' if the frog has reached an exit, otherwise
        it is None.
        """
        self._reachexit = value

    def getWinStatus(self):
        """
        Returns the win status.
        """
        return self._win

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self, objects, json, width, height):
        """
        Initializes a game Level corresponding to a specific json.

        This Initializer takes in a json dictionary that consists of necessary
        Level information, along with the height and width of the window of this
        specfic level, in order to create the respective game Level.

        From this dictionary, the 'lanes' list is extracted in order to create
        individual GTiles for each lane of this level. Then, each of these lanes
        are used to create composite Lane objects.

        Additionally, the frog starting position is extracted from the json,
        which is then used in order to create the frog at the starting position.

        Parameter objects_json: A json dictionary of objects
        Precondition: objects_json is a valid json dictionary that refers to the
        specific objects that are in a particular level.

        Parameter json: A json dictionary with level information
        Precondition: json is a valid json dictionary that provides information
        about a particular level file.

        Parameter width: The width of the level.
        Precondition: Width is an int that corresponds to the width
        of the level file

        Parameter height: The height of the level.
        Precondition: height is an int that corresponds to the width
        of the level file
        """
        self._deathSound = Sound(SPLAT_SOUND)
        self._death = None
        self._comp=None
        self._win = None
        self._reachexit = None
        self._objects_json = objects
        self._sprites = self._objects_json['sprites']
        self._json = json
        self._width = width
        self._fullheight = height
        self._height = height//(len(self._json['lanes']))
        lanes = self._json['lanes']
        self._lanes = []
        i=0
        for item in self._json['lanes']:
            source = item['type'] + '.png'
            object = GTile(left = 0, bottom = GRID_SIZE*i, width=self._width,
            height=self._height, source=source)
            i = i+1
            self._lanes.append(object)
        for i in range(len(self._lanes)):
            self._comp=Lane(self._objects_json, self._json, self._lanes)
        self._frogstartx = self._json['start'][0]
        self._frogstarty = self._json['start'][1]
        self.setFrog(self._frogstartx, self._frogstarty)
        self._froglives=self._displaylives(len(self._lanes))
        self._liveslabel= self._liveslabel()
        self._open_or_exit=self._opens_and_exits()

    # UPDATE METHOD TO MOVE THE FROG AND UPDATE ALL OF THE LANES
    def update(self, input, dt):
        """
        Updates the frog, lanes, and death, and returns 'dead' if the frog
        has died.

        This method updates the frog position by calling the update method for
        the frog object. This method also calls the update method for the Lane
        objects, and if it returns 'reached exit', this method will set the frog
        to None, and set the _reachexit attribute to 'yes'. If the player has
        won the game, this method will set the _win attribute to 'win'.

        If the _death attribute is not None, then this method will call the
        update method for death, and if it returns 'done', this method will set
        the _death attribute to None, deduct a life, and then return 'dead'.
        This method also calls the road death and log ride methods.

        Parameter input: The keyboard input.
        Precondition: input is a string that refers to the particular key
        that the player presses.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is an number >= 0
        """
        self.input = input
        if self._frog is not None:
            EastorWest = self._collideEastorWest()
            North = self._collideNorth()
            South = self._collideSouth()
            self._frog.update(dt, input, self._width, self._fullheight,
            EastorWest, North, South)
        if self._frog is not None:
            if self._comp.update(dt, self._frog)=='reached exit':
                self._frog = None
                self._reachexit = 'yes'
        if self._comp.checkWin()=='game won':
            self._win = 'win'
        if self._death is not None:
            if self._death.update(dt) == "done":
                self._death = None
                self._froglives=self._froglives[:-1]
                return 'dead'
        self._roadDeath()
        self._logride(dt)

    def draw(self, view):
        """
        Draws the frog, lane, and death objects to the view.

        Parameter view: The view to draw to
        Precondition: view is a GView object
        """
        for lane in self._lanes:
            lane.draw(view)
        self._comp.draw(view)
        if self._frog is not None:
            self._frog.draw(view)
        if self._death is not None:
            self._death.draw(view)
        for x in self._froglives:
            x.draw(view)
        self._liveslabel.draw(view)
        for x in range(len(self._comp.getbluefrog())):
            self._comp.getbluefrog()[x].draw(view)

    def livescounter(self):
        """
        Returns whether the game is done, or still going

        This method returns 'done' if the there are no more lives left, or it
        will return 'still going' if there are still lives left.
        """
        if self._froglives==[]:
            return 'done'
        else:
            return 'still going'

    # ANY NECESSARY HELPERS (SHOULD BE HIDDEN)
    def _roadDeath(self):
        """
        Returns 'dead' if the frog is dead.

        This method detects whether one of the vehicles contains the frog, which
        indicates if the frog has been in a car accident. If this condition is
        met, then a death object is created with the coordinates of where the
        frog died, the death sound is played, the frog is set to None, and this
        method will return 'dead'.
        """
        if self._frog is not None:
            frog_row = int(self._frog.y//64)
            for j in self._comp.getObjects():
                if (j.contains((self._frog.x, self._frog.y)) and
                self._lanes[frog_row].source=='road.png'):
                    self.setDeath(self._frog.x, self._frog.y)
                    self._deathSound.play()
                    self._frog = None
                    return "dead"

    def _logride(self, dt):
        """
        Returns 'alive' if frog is alive, or 'drowning' if frog is drowning.

        This method creates a list for logs, for the speeds of the water lanes,
        and for the speeds of each log. It then determines whether the frog is
        in the water. If the frog is on a log, then this method will return
        'alive'. Otherwise, if the frog is just in the water, this method will
        create a death object, play the death sound, set the frog to None, and
        return 'drowning'.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is an number >= 0
        """
        waterlanespeed=[]
        logs= []
        for x in self._json['lanes']:
            if x['type']=='water':
                logs.append(x['objects'])
                waterlanespeed.append(x['speed'])
        logspeeds = []
        for i in range(len(logs)):
            for j in logs[i]:
                logspeeds.append(waterlanespeed[i])
        water_lanes = []
        for x in range(len(self._lanes)):
            if self._lanes[x].source == 'water.png':
                water_lanes.append(self._lanes[x])
        if self._frog is not None and self._frog.getAnimator() is None:
            for x in range(len(water_lanes)):
                if water_lanes[x].contains((self._frog.x, self._frog.y)):
                    if self._onlog(water_lanes, logspeeds, dt):
                        return 'alive'
                    else:
                        self.setDeath(self._frog.x, self._frog.y)
                        self._deathSound.play()
                        self._frog = None
                        return 'drowning'

    def _onlog(self, water_lanes, logspeeds, dt):
        """
        Returns True if frog is on the log, else, returns False.

        This method creates a list of the log objects, and determines whether
        any of the logs contain the frog. If this condition is met and the frog
        is within the frame of the level, the frog's x coordinate will
        change at the same speed as the log's while the frog remains stationary
        on the log, and this method will return True. Otherwise, this method
        will return False.

        Parameter water_lanes: the lanes of water.
        Precondition: water_lanes is a list of GTile objects that have the
        source 'water'

        Parameter logspeeds: list of speeds of logs.
        Precondition: logspeeds is a list that corresponds to the speeds of each
        log. The length of this list should be the same as the number of logs
        in the level.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is an number >= 0
        """
        logs = []
        for x in self._comp.getObjects():
            if 'log' in x.source:
                logs.append(x)

        for i in range(len(logs)):
            if logs[i].contains((self._frog.x, self._frog.y)):
                if (self._frog.x>=(GRID_SIZE//2) and
                self._frog.x<=self._width-(GRID_SIZE//2)):
                    self._frog.x = self._frog.x + (logspeeds[i]*dt)
                    return True
                else:
                    return False

    def _displaylives(self, numlanes):
        """
        Returns list of frog lives.

        This helper method creates and returns a list of three GImages with x
        and y coordinates in the upper right corner of the level window frame.

        Parameter numlanes: the number of lanes in the level.
        Precondition: numlanes is an int that correspond to the number of lanes
        in this level.
        """
        height = (numlanes*GRID_SIZE)+(GRID_SIZE//2)
        list = []
        x=(self._width)-(GRID_SIZE//2)
        y=height
        for i in range(3):
            frog = GImage(x=x,y=y,width=GRID_SIZE,height=GRID_SIZE)
            frog.source=FROG_HEAD
            list.append(frog)
            x = x-GRID_SIZE
        return list

    def _liveslabel(self):
        """
        Returns the lives label.

        This method will return a GLabel with the text "Lives: " in the upper
        right corner of the level window frame, placed in front of the frog
        live heads.
        """
        label = GLabel(text="Lives:",font_size=ALLOY_SMALL,font_name=ALLOY_FONT)
        label.linecolor=introcs.RGB(0,100,0)
        label.right=self._froglives[0].left-2*GRID_SIZE
        label.y = self._froglives[0].y
        return label

    def _opens_and_exits(self):
        """
        Returns list of open and exit objects.

        This method will identify whether an object is an open or exit, and if
        this condition is met, it will add it to a list of opens and exits, and
        return this list.
        """
        object_list=self._comp.getObjects()
        open_or_exit = []
        for i in range(len(object_list)):
            if (object_list[i].source=='open.png' or
            object_list[i].source=='exit.png'):
                open_or_exit.append(object_list[i])
        return open_or_exit

    def _collideNorth(self):
        """
        Returns False if the frog will land in a Hedge or occupied exit,
        True otherwise.

        If the player wishes to move the frog to the North, this method will
        detect whether the player is allowed to do this by identifying if the
        next position of the frog will be in a Hedge or occupied exit, or if it
        will be in an open or available exit. If the next position will be in a
        Hedge or occupied exit, this method will return False, and if the next
        position will be in an open or available exit, this method will return
        True. This method will also return True, if the next position is in
        general not a hedge or occupied exit.
        """
        frog_row = int(self._frog.y//64)
        if (self._lanes[frog_row+1].source)=='hedge.png':
            for j in self._comp.getbluefrog():
                if j.contains((self._frog.x, (self._frog.y+GRID_SIZE))):
                    return False
            for j in self._open_or_exit:
                if j.contains((self._frog.x, (self._frog.y+GRID_SIZE))):
                    return True
            return not self._frog.collides(self._lanes[frog_row])
        else:
            return True

    def _collideSouth(self):
        """
        Returns False if the frog will land in a Hedge or exit, True otherwise.

        If the player wishes to move the frog to the South, this method will
        detect whether the player is allowed to do this by identifying if the
        next position of the frog will be in a Hedge or exit, or if it
        will be in an open. If the next position will be in a Hedge or exit,
        this method will return False, and if the next position will be in an
        open, this method will return True. This method will also return True,
        if the next position is in general not a hedge or exit.
        """
        frog_row = int(self._frog.y//64)

        if (self._lanes[frog_row-1].source)=='hedge.png':
            for j in self._comp.getbluefrog():
                if j.contains((self._frog.x, (self._frog.y-GRID_SIZE))):
                    return False
            for j in self._open_or_exit:
                open = []
                if j.source == 'open.png':
                    open.append(j)
                    for x in open:
                        if x.contains((self._frog.x, (self._frog.y-GRID_SIZE))):
                            return True
                elif j.contains((self._frog.x, (self._frog.y-GRID_SIZE))):
                    return False
            return not self._frog.collides(self._lanes[frog_row])
        else:
            return True

    def _collideEastorWest(self):
        """
        Returns False if the frog will land in a Hedge or occupied exit,
        True otherwise.

        If the player wishes to move the frog to the East or West, this method
        will detect whether the player is allowed to do this by identifying if
        the next position of the frog will be in a Hedge or occupied exit, or
        if it will be in an open or available exit. If the next position will be
        in a Hedge or occupied exit, this method will return False, and if the
        next position will be in an open or available exit, this method will
        return True. This method will also return True, if the next position is
        in general not a hedge or occupied exit.
        """
        frog_row = int(self._frog.y//64)

        if (self._lanes[frog_row].source)=='hedge.png':
            for j in self._comp.getbluefrog():
                if j.contains((self._frog.x, (self._frog.y-GRID_SIZE))):
                    return False
            for j in self._open_or_exit:
                if j.contains((self._frog.x, self._frog.y)):
                    return False
            return not self._frog.collides(self._lanes[frog_row])
        else:
            return True
