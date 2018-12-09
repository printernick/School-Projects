# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from enum import Enum

class MyAI ( Agent ):

    class Direction ( Enum ):
        UP = 1
        LEFT = 2
        RIGHT = 3
        DOWN = 4
            
    class MARKERS ( Enum ):
        POSSIBLE = 1
        IMPOSSIBLE = 2
        UNKNOWN = 3
            
    def __init__ ( self ):
        
        #A list containing a dictionary for every square on the map.
        #The keys in the dictionary are:
        #OK: a bool representing if the square is 100% safe (true) or not
        #Pit status: a MARKER that indicates if it is possibly a pit, not possibly a pit, or unknown
        #Wumpus status: same as above but for the wumpus
        #Explored: a bool representing if this area has been visited
        
        self.learnedArea = [[{'OK': False, 'Pit status': MyAI.MARKERS.UNKNOWN,
                              'Wumpus status': MyAI.MARKERS.UNKNOWN, 'Explored': False} for i in range(7)] for j in range(7)] 
        
        
        self.learnedArea[0][0]['OK'] = True
        self.learnedArea[0][0]['Explored'] = True
        
        
        
        
        #Conceptually x and y, but reversed in the list
        #location of our current position
        self.x = 0
        self.y = 0
    
        self.lootedGold = False
        self.wumpusDead = False
        self.haveArrow = True
        self.backtracking = False
        self.previousSquares = []
        self.previouslyShot = False
        
        self.facingDirection = MyAI.Direction.RIGHT
        

        
    def getAction( self, stench, breeze, glitter, bump, scream ):
       
        if self.backtracking:
            return self._goHome()

     
        if bump:
            
            self._reverseLocation()
            self._shrinkBoard()
            
        if scream:
            
            self.wumpusDead = True
            self._changeAllStatuses('Wumpus status', self._getEveryCoordinate(), MyAI.MARKERS.IMPOSSIBLE)
            
        elif self.previouslyShot:
            
            self.previouslyShot = False
            self._changeAllStatuses('Wumpus status', self._getCoordinatesInFront(), MyAI.MARKERS.IMPOSSIBLE)
            

        if self.learnedArea[self.y][self.x]['Explored'] == False:
            self.learnedArea[self.y][self.x]['Explored'] = True
        
        adjacentSquares = self._getAdjacentSquares()
            
        if stench and not self.wumpusDead:
            
            self._changeAllStatuses('Wumpus status', adjacentSquares, MyAI.MARKERS.POSSIBLE)
            
            if self.haveArrow:
                
                self.haveArrow = False
                self.previouslyShot = True
                return Agent.Action.SHOOT
            
        if breeze:
            
            self._changeAllStatuses('Pit status', adjacentSquares, MyAI.MARKERS.POSSIBLE)
        
        #adjacent squares are safe
        if (not stench and not breeze):
            
            self._changeAllStatuses('OK', adjacentSquares, True)

        #No pit
        elif (not breeze):
            self._changeAllStatuses('Pit status', adjacentSquares, MyAI.MARKERS.IMPOSSIBLE)

        #No wumpus
        elif (not stench):
            self._changeAllStatuses('Wumpus status', adjacentSquares, MyAI.MARKERS.IMPOSSIBLE)
        
         
        if glitter and not self.lootedGold:
            self.lootedGold = True
            self.backtracking = True
            return Agent.Action.GRAB

        x, y = self._getValidAdjMove(adjacentSquares)
        if x == -1:
            self.backtracking = True
            return self._goHome()
        else:
            return self._turnTowardsSquare(x, y)
            
        
    
##############################################################################################################
###############################HELPER FUNCTIONS###############################################################

    def _updateLocation(self):
        '''Updates the class attributes representing 
        the agents current location.
        
        Adds to the stack of previous squares if not
        backtracking'''
        
        if not self.backtracking:
            self.previousSquares.append((self.x, self.y))
        
        if self.facingDirection == MyAI.Direction.RIGHT:
            self.x += 1
        elif self.facingDirection == MyAI.Direction.UP:
            self.y += 1
        elif self.facingDirection == MyAI.Direction.LEFT:
            self.x -= 1
        elif self.facingDirection == MyAI.Direction.DOWN:
            self.y -= 1
            
        
        
    def _reverseLocation(self):
        '''When encountering a bump, we would move
        our location without sensing the bump. After we sense
        the bump, we revert our location to be accurate again'''
        
        if self.facingDirection == MyAI.Direction.RIGHT:
            self.x -= 1
        elif self.facingDirection == MyAI.Direction.UP:
            self.y -= 1
        elif self.facingDirection == MyAI.Direction.LEFT:
            self.x += 1
        elif self.facingDirection == MyAI.Direction.DOWN:
            self.y += 1
    
    def _shrinkBoard(self):
        '''After bumping, we should know a more accurate
        size of the board and can shrink our 2D list
        based on the Direction we were facing'''
        
        if self.facingDirection == MyAI.Direction.RIGHT:
            self.learnedArea = [x[:self.x+1] for x in self.learnedArea]
        elif self.facingDirection == MyAI.Direction.UP:
            self.learnedArea = self.learnedArea[:self.y+1]
            
        self.previousSquares.pop()
            
    def _getAdjacentSquares(self) -> [(int, int)]:
        '''From the current position, return all coordinates 
        in the form (x, y) in a list with bound checking'''
        
        adjacentSquares = []
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for x_coord, y_coord in directions:
            new_x = self.x + x_coord
            new_y = self.y + y_coord
            
            if self._isInBounds(new_x, new_y):
                adjacentSquares.append((new_x, new_y))
        return adjacentSquares

    def _changeStatus(self, status: str, x: int, y: int, marker):
        '''Change the square with the given marker. Does not
        change the status if it was previously marked impossible.'''
        
        if((not self._isInBounds(x, y)) or type(self.learnedArea[y][x]) != bool and self.learnedArea[y][x][status] == MyAI.MARKERS.IMPOSSIBLE):
            return
        else:
            if (status == 'Pit status' and 
                self.learnedArea[y][x]['Wumpus status'] == MyAI.MARKERS.IMPOSSIBLE and 
                marker == MyAI.MARKERS.IMPOSSIBLE):
                self.learnedArea[y][x]['OK'] = True
            elif (status == 'Wumpus status' and 
                self.learnedArea[y][x]['Pit status'] == MyAI.MARKERS.IMPOSSIBLE and 
                marker == MyAI.MARKERS.IMPOSSIBLE):
                self.learnedArea[y][x]['OK'] = True
            
            self.learnedArea[y][x][status] = marker

    def _changeAllStatuses(self, status: str, coordinates: [(int, int)], marker):
        '''Mark all squares from the given coordinates with the given marker.'''
        
        for x_coord, y_coord in coordinates:
            self._changeStatus(status, x_coord, y_coord, marker)
        
    def _turnTowardsSquare(self, x: int, y: int) -> Agent.Action:
        '''Given the coordinates to an adjacent square,
        return the turning action that will be closest to facing
        that square. 
        
        If already facing the correct Direction, go forward'''
        
        if y > self.y:
            if self.facingDirection in [MyAI.Direction.DOWN, MyAI.Direction.LEFT]:
                turn = MyAI.Direction.RIGHT
            elif self.facingDirection == MyAI.Direction.RIGHT:
                turn = MyAI.Direction.LEFT
            else:
                self._updateLocation()
                return Agent.Action.FORWARD
        if x > self.x:
            if self.facingDirection in [MyAI.Direction.UP, MyAI.Direction.LEFT]:
                turn = MyAI.Direction.RIGHT
            elif self.facingDirection == MyAI.Direction.DOWN:
                turn = MyAI.Direction.LEFT
            else:
                self._updateLocation()
                return Agent.Action.FORWARD

        if y < self.y:
            if self.facingDirection in [MyAI.Direction.UP, MyAI.Direction.RIGHT]:
                turn = MyAI.Direction.RIGHT
            elif self.facingDirection == MyAI.Direction.LEFT:
                turn = MyAI.Direction.LEFT
            else:
                self._updateLocation()
                return Agent.Action.FORWARD
        if x < self.x:
            if self.facingDirection in [MyAI.Direction.UP, MyAI.Direction.RIGHT]:
                turn = MyAI.Direction.LEFT
            elif self.facingDirection == MyAI.Direction.DOWN:
                turn = MyAI.Direction.RIGHT
            else:
                self._updateLocation()
                return Agent.Action.FORWARD
        move = self._updateDirection(turn)
        return move

    def _isSameDirection(self, x: int, y: int) -> bool:
        
        '''Given a coordinate, returns True if agent is facing the 
        direction to go forward into the new square and False
        if the agent is facing another directon'''
        
        return ((y > self.y and self.facingDirection == MyAI.Direction.UP) or
                (x > self.x and self.facingDirection == MyAI.Direction.RIGHT) or
                (y < self.y and self.facingDirection == MyAI.Direction.DOWN) or
                (x < self.x and self.facingDirection == MyAI.Direction.LEFT))

    def _getValidAdjMove(self, coords: [(int, int)]) -> (int, int):
        
        '''Given a list of adjacent coordinates, return the coordinate
        of a valid move that the agent can reach in the least amount of 
        turns.
        
        Returns (-1, -1) if not valid adjacent moves'''
        
        valid_moves = []
        for x,y in coords:
            if not self.learnedArea[y][x]['Explored'] and self.learnedArea[y][x]['OK']:
                if self._isSameDirection(x, y):
                    valid_moves = [(x, y)] + valid_moves
                else:
                    valid_moves.append((x, y))
    
        if len(valid_moves) == 0:
            return (-1, -1)
        else:
            return valid_moves[0]

    

    def _goHome(self) -> Agent.Action:
        
        '''Returns actions to backtrack to previous
        squares. If the gold has been looted, travels back
        to the starting square as soon as possible to climb out.
        
        If gold has not been looted, checks adjacent moves along the
        way to see if there are other valid areas to explore'''
        
        if not self.lootedGold:
            x, y = self._getValidAdjMove(self._getAdjacentSquares())
            if x != -1:
                self.backtracking = False
                return self._turnTowardsSquare(x, y)
        
        if len(self.previousSquares) == 0:
            return Agent.Action.CLIMB
        
        x, y = self.previousSquares[-1]
        action = self._turnTowardsSquare(x, y)
        if action == Agent.Action.FORWARD:
            self.previousSquares.pop()
        return action
    
    
    def _isInBounds(self, x: int, y: int) -> bool:
        '''Given an x coordinate and a y coordinate,
        return whether or not that is in bounds based
        on the current knowledge of the dimensions'''
        
        return x != -1 and x < len(self.learnedArea[0]) and y != -1 and y < len(self.learnedArea)
    
    def _updateDirection(self, direction) -> Agent.Action:
        
        '''Given a direction to turn, update the direction
        the agent believes it is facing based on the current
        facing direction and the direction it is turning'''
        
        if direction == MyAI.Direction.RIGHT:
            if self.facingDirection == MyAI.Direction.UP:
                self.facingDirection = MyAI.Direction.RIGHT
            elif self.facingDirection == MyAI.Direction.RIGHT:
                self.facingDirection = MyAI.Direction.DOWN
            elif self.facingDirection == MyAI.Direction.DOWN:
                self.facingDirection = MyAI.Direction.LEFT
            else:
                self.facingDirection = MyAI.Direction.UP
            return Agent.Action.TURN_RIGHT
        else:
            if self.facingDirection == MyAI.Direction.UP:
                self.facingDirection = MyAI.Direction.LEFT
            elif self.facingDirection == MyAI.Direction.RIGHT:
                self.facingDirection = MyAI.Direction.UP
            elif self.facingDirection == MyAI.Direction.DOWN:
                self.facingDirection = MyAI.Direction.RIGHT
            else:
                self.facingDirection = MyAI.Direction.DOWN
            return Agent.Action.TURN_LEFT
        
    def _getEveryCoordinate(self) -> list:
        
        '''Returns a list of all the coordinates in the entire
        environment. Used to remove all wumpus markers when
        the wumpus is dead (perceives a scream)'''
        
        return [(x, y) for x in range(len(self.learnedArea[0])) for y in range(len(self.learnedArea))]
    
    def _getCoordinatesInFront(self) -> list:
        
        '''Returns a list of coordinates in front of the agent based
        on the direction it is facing. Used for shooting the arrow
        and missing'''
        
        if self.facingDirection == MyAI.Direction.UP:
            return [(self.x, y) for y in range(self.y, len(self.learnedArea))]
        elif self.facingDirection == MyAI.Direction.DOWN:
            return [(self.x, y) for y in range(0, self.y)]
        elif self.facingDirection == MyAI.Direction.RIGHT:
            return [(x, self.y) for x in range(self.x, len(self.learnedArea[0]))]
        else:
            return [(x, self.y) for x in range(0, self.x)]
    
    def _printMap(self):
        
        '''A debugging function that prints the map
        that the agent believes the environment is like'''
        
        if self.facingDirection == MyAI.Direction.RIGHT:
            print('-->')
        elif self.facingDirection == MyAI.Direction.LEFT:
            print('<--')
        elif self.facingDirection == MyAI.Direction.UP:
            print('^')
        elif self.facingDirection == MyAI.Direction.UP:
            print('v')  
            
        for i in reversed(range(len(self.learnedArea))):
            for j in range(len(self.learnedArea[i])):

                
                if i == self.y and j == self.x:
                    print('A', end = '')
                if self.learnedArea[i][j]['OK']:
                    print('O', end = '')
                if self.learnedArea[i][j]['Explored']:
                    print('E', end = '')
                else:
                    print('.', end = '')
                    
                print('   ', end = '')
                    
            print('\n')
        
        print()
    