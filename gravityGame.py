# Gravity Simulation by Igal
import gameEngine as gE
# Useful for later calc
from math import atan, sin, cos, pi

# Initializes the game engigne
gE.inits(GivenWidth = 1500, GivenHeight = 900, dec = 20)
# Sets a rate at which the computer will run at
rate = 0.01

# Constant G
G = 3
# Equation to calculate force given mass1, mass2 and distance
forceEquation = lambda mass1, mass2, dist: (G * mass1 * mass2) / dist

# Global radius calculation
# Note: this can be changed to make whatever you want
radiusCalculation = lambda mass: round(mass**0.5)

#===============================================================================

# Creates a planet class
class Planet:
    def __init__(self, mass, startingPos, velocity, col):
        # Calculates the radius of the planet in accordance to the global equation
        rad = radiusCalculation(mass)
        # Stores the gameEngine object to manipulate
        self.obj = gE.createCircle(radius = rad, startingPos = startingPos, velocity = velocity, colour = col)
        # Stores the mass of the planet
        self.mass = mass

    # Finds the distance to another planet
    def distanceToP2(self, p2):
        # Gets the difference between the 2 planets
        differenceXY = self.difference(p2)

        # Pythagorean to find unsquared distance between 2 planets
        unsquaredDist = (differenceXY[0])**2 + (differenceXY[1])**2

        # Returns the square root, aka distance
        return unsquaredDist**(1/2)

    # Finds the x,y differences between 2 planets
    def difference(self, P2):
        # Gets the x,y of our planet
        x, y = self.obj.pos
        # Gets the x,y of the other planet
        x1, y1 = P2.obj.pos

        # Returns tuple of the difference from our planet's POV
        return x - x1, y - y1

    def acceleration(self, P2):
        # If there is no collision
        if not self.obj.circleCircleCollison(rate, P2.obj):
            # Finds the gravtional force between 2 planets
            force = forceEquation(self.mass, P2.mass, self.distanceToP2(P2))
            # Finds the acceleration (F/m = a)
            acceleration = round(force / self.mass, 10)

            # Creates a vector of the differences in position
            diffVector = gE.createVector(self.difference(P2)[0], self.difference(P2)[1])
            # Normalizes the vector so it can be used to find acceleration with respect to x,y
            diffVector = diffVector.normalize()

            # Updates the object's velocity accordingly to the normal and acceleration
            self.obj.updateVel(-acceleration * diffVector.x, -acceleration * diffVector.y)

            return False
        else:
            # Sets both object's velocity to 0 as to stop collisions
            self.obj.velocity = [0, 0]
            P2.obj.velocity = [0, 0]

            return True

            """
            Note: this simulation won't deal with complex collisions
            we'll just set their velocities to 0
            """

    # Creates the velocity vector
    def createVelocityVector(self, velocity: list[float] = None):
        # Finds the center of the planet
        center = self.obj.giveCenter()
        # Rounds the center to whole numbers
        center = [round(center[0]), round(center[1])]

        # Checks if a velocity vector was given
        if velocity is None:
            # Sets the vector to the object's velocity
            velVector = self.obj.velocity
        else:
            # Sets the vector to the given velocity
            velVector = velocity

        # Stores and creates the velocity vector, from center to center + velocity vector
        self.vVector = gE.createLine(center, [center[0] + velVector[0], center[1] + velVector[1]])

    # Destroys the velocity vector
    def destroyVelocityVector(self):
        # Deletes the line
        self.vVector.destroy(self.vVector)
        # Sets the vector to None
        self.vVector = None

    # Destorys the planet
    def destroyPlanet(self):
        # Removes the velocity vector
        self.destroyVelocityVector()
        # Removes the planet object
        self.obj.destroy(self.obj)

    # Updates the radius of the planet
    def updateSize(self):
        # Removes the old velocity vector
        self.destroyVelocityVector()

        # Calculates new radius
        newRad = radiusCalculation(self.mass)

        # Store old data
        col = self.obj.colour
        pos = self.obj.pos
        vel = self.obj.velocity

        # Removes old planet
        self.obj.destroy(self.obj)

        # Recreates the new planet
        self.obj = gE.createCircle(radius = newRad, startingPos = pos, velocity = vel, colour = col)

        # Recreates the velocity vector
        self.createVelocityVector(pauseMenu.storedVels[pauseMenu.selectedIndex])


# Class to deal with the pause menu
class Pause:
    def __init__(self, traceSteps: int, skippingSteps: int = 2):
        # Keeps track of how many steps it needs to trace
        self.traceSteps = traceSteps
        # Keeps track of how many steps it'll skip
        self.skippingSteps = skippingSteps
        # Keeps a list of traced steps (that is because traced steps are lines)
        self.tracedSteps = []

        # Creates an empty value for all the stored velocities
        self.storedVels = []
        # Loops through all the planets
        for i in range(len(planets)):
            # Adds a empty velocity
            self.storedVels.append([0, 0])

        # Variable to see if the game is "paused"
        self.pause = True
        # Creates a small circle that will change colour if
        # the game is paused.
        self.pauser = gE.createCircle(radius = 5, startingPos = [5, 5], velocity = [0, 0], colour = "green")

        # Stores the index of which planet is selected to be manipulated
        self.selectedIndex = -1

        # Creates the initial velocity vectors
        self.dealVelVec()
        # Traces out initial path of the planets
        self.tracer()
        # Switches the values of the planets to pause them
        self.switchVels()


    # Switches the 2 velocities between 0s and their original for pausing
    def switchVels(self):
        # Loops through each stored velocity
        for i in range(len(planets)):
            # Switches the two (planet's velocity and stored velocity)
            self.storedVels[i], planets[i].obj.velocity = planets[i].obj.velocity, self.storedVels[i]

    # Deals with assigning velocity vectors
    def dealVelVec(self):
        # If the game is paused
        if self.pause:
            # Loops through all planets
            for P in planets:
                # Creates the velocity vector of the planet
                P.createVelocityVector()
        else:
            # Loops through all planets
            for P in planets:
                # Destroys all the velocity vectors
                P.destroyVelocityVector()

    # Deals if something is clicked when the game is paused
    def clickEvent(self, pos):
        # Gets the index of the planet clicked
        index = planetClicked(pos)

        # Checks if a planet was clicked
        if index != -1:
            # Changes the old selected to black as it is not selected
            planets[self.selectedIndex].obj.changeColour("black")
            # Changes the index of the selected
            self.selectedIndex = index
            # Colours the new selected planet
            planets[self.selectedIndex].obj.changeColour("red")

    # Switches the between pause states
    def switch(self):
        # If game is paused
        if self.pause:
            # Switches the pause bool
            self.pause = False
            # Switches the colour of the pause indicator
            self.pauser.changeColour("white")

            # Changes the colour of the selected index back to black
            planets[self.selectedIndex].obj.changeColour("black")

            self.delTracer()
        else:
            # Switches the bool
            self.pause = True
            # Switches colour of the pause indicator
            self.pauser.changeColour("green")

            # Changes the colour of the selected index to red
            planets[self.selectedIndex].obj.changeColour("red")

            self.tracer()

        # Switches velocities
        self.dealVelVec()
        # Deals with velocity vectors
        self.switchVels()

    # Traces where the planets will be
    def tracer(self):
        # Uses global planets parameter so as to actually affect the planets
        global planets

        # Stores the planet info before tracing them so as to
        # not actually change anything
        planeteryInfo = []

        # Stores the current amount of traced steps we passed
        currentStep = 0

        # Appends the first traced step, currently empty
        self.tracedSteps.append([])
        # Loops through the planets
        for P in planets:
            # Stores planetery info
            planeteryInfo.append([P.obj.pos.copy(), P.obj.velocity.copy()])

            # Finds their rounded center
            planetPos = P.obj.giveCenter()
            planetPos = [round(planetPos[0]), round(planetPos[1])]

            # Adds their initial position to the tracedSteps so we can later make lines
            self.tracedSteps[currentStep].append(planetPos)

        # Keeps looping until we are done all the wanted steps
        while currentStep < self.traceSteps:
            # Increments the step counter
            currentStep += 1

            # Adds another empty place to store traced steps
            self.tracedSteps.append([])

            # Loops through the amount of steps we skip
            for _ in range(self.skippingSteps):
                # Accelerates the planets
                calculateAcceleration()

                # Moves the planets
                for P in planets:
                    P.obj.move(rate)

            # Loops through all the planets
            for i in range(len(planets)):
                # Finds the planet's current center rounded
                planetPos = planets[i].obj.giveCenter()
                planetPos = [round(planetPos[0]), round(planetPos[1])]

                # Goes back and replaces coordinates with actual lines to represent traced steps
                self.tracedSteps[currentStep - 1][i] = gE.createLine(vertex1 = self.tracedSteps[currentStep - 1][i], vertex2 = planetPos, colour = "orange")

                # Adds the current position for next loop
                self.tracedSteps[currentStep].append(planetPos)

        # Loops through all the stored planet info
        for i in range(len(planeteryInfo)):
            # Switches the position back to before traced
            planets[i].obj.pos = planeteryInfo[i][0]
            # Switches the velocity back to before traced
            planets[i].obj.velocity = planeteryInfo[i][1]

    # Deletes the tracers
    def delTracer(self):
        # Loops through the tracers - 1 (final one is not a line but position
        for step in range(len(self.tracedSteps) - 1):
            # Loops through each line in each step
            for line in self.tracedSteps[step]:
                # Destroys the line
                line.destroy(line)

        # Clears the list of everything
        self.tracedSteps.clear()

    # Function to update tracers
    def updateTracer(self):
        # Delete the tracer
        self.delTracer()
        # Retraces the tracers
        self.tracer()


# Calculates the acceleration of each planet to each other
def calculateAcceleration():
    # Loops each planet
    for P1 in planets:
        # Loops through every other planet
        for P2 in planets:
            # If the distance between the 2 is 0 (aka its the same planet) ignore it
            if P1.distanceToP2(P2) != 0:
                # Otherwise properly accelerate the 2 planets
                P1.acceleration(P2)

# Finds if a planet was clicked, if so returns it's index, otherwise -1
def planetClicked(clickedArea):
    # Loops through all the planets
    for i in range(len(planets)):
        # Checks if the point clicked on a planet
        if planets[i].obj.pointCollison(clickedArea):
            # Returns the index of the clicked planet
            return i
    # Returns -1 as no planet was found
    return -1

# Function to move the 'camera' in accordance to the amount
def moveCamera(moveAmount):
    # Uses the global planets
    global planets

    # Loops over planets
    for P in planets:
        # Updates their x,y position
        P.obj.pos[0] -= moveAmount[0]
        P.obj.pos[1] -= moveAmount[1]

        # If the game is paused
        if pauseMenu.pause:
            # Updates velocity vectors
            P.destroyVelocityVector()
            P.createVelocityVector()

            # Switches the planet's stored velocities to the current planet velocities
            pauseMenu.switchVels()
            # Updates the tracers
            pauseMenu.updateTracer()
            # Switches it back
            pauseMenu.switchVels()


# Loads up the empty planets
planets = []

# Initializes the pause menu
pauseMenu = Pause(500, 5)

try:
    while 1:
        # Pauses the frame rate
        gE.wait(rate)
        # Updates the frames and stores what keys were clicked
        events = gE.update(rate)

        # Checks if the user asked to pause
        if events[0] == ' ':
            # Switches the pause menu
            pauseMenu.switch()
        # Checks if the user wanted to move the camera
        elif events[0] is not None and events[0] in 'ijkl':
            if events[0] == 'i':
                moveCamera((0, 10))
            elif events[0] == 'k':
                moveCamera((0, -10))
            elif events[0] == 'j':
                moveCamera((10, 0))
            else:
                moveCamera((-10, 0))

        # Checks if the game is currently paused
        if pauseMenu.pause:
            # Checks if the user clicked on the game
            if events[1] is not None:
                if events[1][0] == 1 and pauseMenu.selectedIndex != -1:
                    # Updates the pauseMenu selected index
                    pauseMenu.clickEvent(events[1][1])
                elif events[1][0] == 2:
                    # Checks if a planet was right clicked
                    index = planetClicked(events[1][1])
                    if index == -1:
                        # Creates a new planet
                        planets.append(Planet(10, events[1][1], [0, 0], "red"))
                        # Adds a velocity vector
                        planets[len(planets) - 1].createVelocityVector()
                        # Adds a new stored velocity to the pause menu
                        pauseMenu.storedVels.append([0, 0])

                        if pauseMenu.selectedIndex != -1:
                            planets[pauseMenu.selectedIndex].obj.changeColour('black')

                        # Updates the selected index to the newest planet
                        pauseMenu.selectedIndex = len(planets) - 1
                    else:
                        # Removes the stored velocities of the planet
                        pauseMenu.storedVels.pop(index)
                        # Destroys the planet
                        planets[index].destroyPlanet()
                        # Removes it from the list
                        planets.pop(index)

                        # To update the index properly, it checks if the popped
                        # index was before or after the selected index
                        if pauseMenu.selectedIndex > index:
                            # Resets index
                            pauseMenu.selectedIndex -= 1
                        elif pauseMenu.selectedIndex == index:
                            # Resets index
                            pauseMenu.selectedIndex -= 1
                            # If there are planets
                            if len(planets) > 0:
                                # Changes the new selected planet to red
                                planets[pauseMenu.selectedIndex].obj.changeColour('red')

                    if len(planets) > 0:
                        # Switches the planet's stored velocities to the current planet velocities
                        pauseMenu.switchVels()
                        # Updates the tracers
                        pauseMenu.updateTracer()
                        # Switches it back
                        pauseMenu.switchVels()
                    else:
                        pauseMenu.selectedIndex = -1



            # Checks if the user pressed a, s, w, d
            if events[0] is not None and pauseMenu.selectedIndex != -1:
                if events[0] in 'asdw':
                    # Destroys the velocity vectors
                    planets[pauseMenu.selectedIndex].destroyVelocityVector()

                    # Updates the velocity vector of the current selected planet
                    if events[0] == 'a':
                        pauseMenu.storedVels[pauseMenu.selectedIndex][0] += -10
                    elif events[0] == 's':
                        pauseMenu.storedVels[pauseMenu.selectedIndex][1] += 10
                    elif events[0] == 'w':
                        pauseMenu.storedVels[pauseMenu.selectedIndex][1] += -10
                    else:
                        pauseMenu.storedVels[pauseMenu.selectedIndex][0] += 10

                    # Updates the velocity vector of the selected planet
                    planets[pauseMenu.selectedIndex].createVelocityVector(pauseMenu.storedVels[pauseMenu.selectedIndex])

                    # Switches the planet's stored velocities to the current planet velocities
                    pauseMenu.switchVels()
                    # Updates the tracers
                    pauseMenu.updateTracer()
                    # Switches it back
                    pauseMenu.switchVels()

                # Checks if the user wants to add mass
                elif events[0] in 'uy':
                    # Checks if they want to increase mass
                    if events[0] == 'u':
                        # Increases mass
                        planets[pauseMenu.selectedIndex].mass += 10
                    elif events[0] == 'y' and planets[pauseMenu.selectedIndex].mass > 10:
                        # Decreases mass if there is more than 10
                        planets[pauseMenu.selectedIndex].mass -= 10

                    # Updates the size of the selected planet
                    planets[pauseMenu.selectedIndex].updateSize()

                    # Switches the planet's stored velocities to the current planet velocities
                    pauseMenu.switchVels()
                    # Updates the tracers
                    pauseMenu.updateTracer()
                    # Switches it back
                    pauseMenu.switchVels()

        else:
            # If not paused, then update accelerations
            calculateAcceleration()
except:
    pass

