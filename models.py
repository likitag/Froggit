"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

Likita Gangireddy lg425
12/21/2020
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.

class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _jumpSound: Sound to play when frog jumps
    # Invariant: _jumpSound is a Sound Object that refers to the CROAK_SOUND
    # audio file
    #
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAnimator(self):
        """
        Returns the coroutine animator
        """
        return self._animator

    def __init__(self, x, y, sprites):
        """
        Initializes frog.

        This Initializer utilizes the super method in order to use the
        initializer from the GSprite class.

        Parameter x: The starting x position of the frog.
        Precondition: x is an int that refers to the starting x position of
        the frog

        Parameter y: The starting y position of the frog.
        Precondition: y is an int that refers to the starting y position of the
        frog.

        Parameter sprites: A dictionary of sprite information
        Precondition: sprites is a valid dictionary of sprite information
        """
        frog_sprite_info = sprites['frog']
        file = frog_sprite_info['file']
        size = frog_sprite_info['size']
        format = frog_sprite_info['format']
        hitboxes= frog_sprite_info['hitboxes']
        x = (x*GRID_SIZE)+(GRID_SIZE//2)
        y = (y*GRID_SIZE) + (GRID_SIZE//2)
        super().__init__(x=x,y=y, source=file, format=format, angle=FROG_NORTH,
        hitboxes=hitboxes, frame = 0)
        self._animator= None
        self._jumpSound = Sound(CROAK_SOUND)

    def update(self,dt, input, width, height, EastorWest, North, South):
        """
        Animates the frog.

        Parameter dt: The number of seconds since the last animation frame
        Precondition: dt is an number >= 0

        Parameter input: The keyboard input.
        Precondition: input is a string that refers to the particular key
        that the player presses.

        Parameter width: width of level
        Precondition: width is an int that corresponds to the width of the level

        Parameter height: height of the level
        Precondition: height is an int that corresponds to the height of the
        level

        Parameter EastorWest: boolean that indicates whether the frog can move
        in the East or West direction.
        Precondition: EastorWest is a boolean

        Parameter North: boolean that indicates whether the frog can move North
        Precondition: North is a boolean

        Parameter South: boolean that indicates whether the frog can move South
        Precondition: South is a boolean.
        """
        self.input = input
        if self._animator is not None:
            try:
                x = self._animator.send(dt)
            except:
                self._animator=None
        elif self.input.is_key_down('left'):
            self.angle=FROG_WEST
            if self.x-GRID_SIZE>=0 and EastorWest:
                self._jumpSound.play()
                self._animator = self.makeAnimator(-GRID_SIZE,FROG_SPEED, 'left')
                next(self._animator)
        elif self.input.is_key_down('right'):
            self.angle=FROG_EAST
            if self.x+GRID_SIZE<=width and EastorWest:
                self._jumpSound.play()
                self._animator = self.makeAnimator(GRID_SIZE,FROG_SPEED, 'right')
                next(self._animator)
        elif self.input.is_key_down('up'):
            self.angle=FROG_NORTH
            if self.y+GRID_SIZE<=(height-(GRID_SIZE*1.5)) and North:
                self._jumpSound.play()
                self._animator = self.makeAnimator(GRID_SIZE,FROG_SPEED, 'up')
                next(self._animator)
        elif self.input.is_key_down('down'):
            self.angle=FROG_SOUTH
            if self.y-GRID_SIZE>=(GRID_SIZE//2) and South:
                self._jumpSound.play()
                self._animator = self.makeAnimator(-GRID_SIZE,FROG_SPEED, 'down')
                next(self._animator)

    def makeAnimator(self,dx, speed, direction):
        """
        Animates the frog over a certain distance in a certain amount of time.

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dx: The amount to move the frog
        Precondition: dx is a number (int or float)

        Paramter speed: The number of seconds to animate the frog
        Precondition: speed is a number > 0

        Paramter direction: The direction to animate the frog.
        Precondition: a valid string direction ('right', 'left', 'up', or
        'down')
        """
        startx = self.x
        finalx = startx+dx
        starty=self.y
        finaly = starty+dx
        seconds = 0
        steps = dx/speed
        while seconds<speed:
            dt = (yield)
            amount = steps*dt
            seconds = seconds + dt
            if direction == 'left' or direction == 'right':
                self.x = self.x+amount
                fracx = 2*(self.x-startx)/(finalx-startx)
                self._checkframe(fracx)
            if direction == 'up' or direction == 'down':
                self.y=self.y + amount
                fracy = 2*(self.y-starty)/(finaly-starty)
                self._checkframe(fracy)
        if direction =='right' or direction=='left':
            self.x=startx+dx
            self.frame = 0
        if direction == 'up' or direction == 'down':
            self.y = starty+dx
            self.frame = 0

    def _checkframe(self, frac):
        """
        Changes the frame of the Frog GSprite.

        This method takes in a fraction, and changes the frame based on the
        value of the fraction.

        Paramter frac: A number that indicates how much of the animation has
        been completed.
        Precondition: frac is an int or float.
        """
        if frac<=2/7:
            self.frame = 1
        elif frac<=4/7:
            self.frame = 2
        elif frac<=6/7:
            self.frame = 3
        elif frac<=8/7:
            self.frame = 4
        elif frac<=10/7:
            self.frame = 3
        elif frac<=12/7:
            self.frame = 2
        elif frac<=2.0:
            self.frame = 1


# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
class Death(GSprite):
    """
    A class representing the death

    The death is represented as a sprite, and therefore, it is made as a
    subclass of GSprite
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE
    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)
    #
    # Attribute _animating: indicates whether the death is animating or not
    # Invariant: _animating is a boolean
    #
    def __init__(self, x, y, sprites):
        """
        Initializes death.

        This Initializer utilizes the super method in order to use the
        initializer from the GSprite class.

        Parameter x: The x position where the frog died.
        Precondition: x is an int that refers to the x position where the frog
        died

        Parameter y: The y position where the frog died.
        Precondition: y is an int that refers to the y position where the frog
        died

        Parameter sprites: A dictionary of sprite information
        Precondition: sprites is a valid dictionary of sprite information
        """
        death_sprite_info = sprites['skulls']
        file = death_sprite_info['file']
        size = death_sprite_info['size']
        format = death_sprite_info['format']
        super().__init__(x=x, y=y, source=file, format=format, frame = 0)
        self._animator = None
        self._animating = True

    def update(self,dt):
        """
        Animates the death.

        Parameter dt: The number of seconds since the last animation frame
        Precondition: dt is an number >= 0
        """
        if not self._animator is None:
            try:
                self._animator.send(dt)
            except:
                self._animator = None
        elif self._animating:
            self._animator=self.makeAnimator(DEATH_SPEED)
            next(self._animator)
        elif not self._animating:
            return "done"

    def makeAnimator(self, speed):
        """
        Animates the death for a certain amount of time.

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Paramter speed: The number of seconds to animate the death
        Precondition: speed is a number > 0
        """
        seconds = 0
        while seconds<speed:
            dt = (yield)
            seconds = seconds + dt
            frac = (seconds)/(DEATH_SPEED)
            self._checkframe(frac)
        self._animating = False

    def _checkframe(self, frac):
        """
        Changes the frame of the death GSprite.

        This method takes in a fraction, and changes the frame based on the
        value of the fraction.

        Paramter frac: A number that indicates how much of the animation has
        been completed.
        Precondition: frac is an int or float.
        """
        if frac<=1/7:
            self.frame = 1
        elif frac<=2/7:
            self.frame = 2
        elif frac<=3/7:
            self.frame = 3
        elif frac<=4/7:
            self.frame = 4
        elif frac<=5/7:
            self.frame = 5
        elif frac<=6/7:
            self.frame = 6
        elif frac<=7/7:
            self.frame = 7
