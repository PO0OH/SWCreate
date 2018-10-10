import pygame
import random
import board
import score

class Tile:

    """Class to represent a single tile in the game"""

    s_width = 20
    s_height = 20

    def __init__( self, screenSurface, tileSurface, boardPos ):
        self.m_boardPos = boardPos
        self.m_screen   = screenSurface
        self.m_tileSurface = tileSurface
        return


    def render( self ):
        # convert to screen coords and blit
        currentScreenX = ( self.m_boardPos[ 0 ] ) * Tile.s_width
        currentScreenY = ( self.m_boardPos[ 1 ] ) * Tile.s_height
        currentBlockRect = pygame.Rect( currentScreenX, currentScreenY, Tile.s_width, Tile.s_height )
        self.m_screen.blit( self.m_tileSurface, currentBlockRect )
        return


class Tetrimino:
    
    """Class to represent a tetrimino in the game"""

    s_maxRepresentations = 4

    def __init__( self, imageSurface, screenSurface ):
        self.m_surface  = imageSurface
        self.m_screen   = screenSurface
        self.m_boardPos = [ int( ( board.Board.s_numTilesWidth / 2 ) - 1 ), board.Board.s_scorePaneHeight ]
        self.m_inPlay   = False 
        self.m_numRepresentations = 0
        self.m_currentRepIdx = 0
        self.m_representation = []
        for repIdx in range( 0, Tetrimino.s_maxRepresentations ): 
            self.m_representation.append( [] )
        return


    def addRepresentation( self, representationIdx, representation ):
        assert representationIdx < Tetrimino.s_maxRepresentations
        if ( representationIdx < Tetrimino.s_maxRepresentations ):
            self.m_representation[ representationIdx ] = representation
            self.m_numRepresentations = self.m_numRepresentations + 1
        return

    
    def nextRepresentation( self ):
        # switches to the next representation
        self.m_currentRepIdx = ( self.m_currentRepIdx + 1 ) % self.m_numRepresentations
        print ( "New tetrimino rep = ", self.m_currentRepIdx )
        return


    def move( self, deltaBoardPos ):
        self.m_boardPos[ 0 ] = self.m_boardPos[ 0 ] + deltaBoardPos[ 0 ]
        self.m_boardPos[ 1 ] = self.m_boardPos[ 1 ] + deltaBoardPos[ 1 ]
        return

    
    # checks whether the tetrimino will collide with the board if it's position or new representation
    # is updated with delta pos
    # this test is run before the tetrimino is moved according to the input
    def willCollideWithBoard( self, deltaPos, board, testNextRepresentation ):
        representationTestIdx = self.m_currentRepIdx
        if testNextRepresentation:
            representationTestIdx = ( representationTestIdx + 1 ) % self.m_numRepresentations
        
        for tetriminoLocalCoords in self.m_representation[ representationTestIdx ]:
            tetriminoBoardCoords = ( tetriminoLocalCoords[ 0 ] + self.m_boardPos[ 0 ] + deltaPos[ 0 ], tetriminoLocalCoords[ 1 ] + self.m_boardPos[ 1 ] + deltaPos[ 1 ] )
            if tetriminoBoardCoords[0] < 0 or tetriminoBoardCoords[0] >= board.s_numTilesWidth or tetriminoBoardCoords[1] >= board.s_scorePaneHeight + board.s_numTilesHeight: 
                return True
            for tile in board.m_tilesFilled:
                if tetriminoBoardCoords[0] == tile.m_boardPos[0] and tetriminoBoardCoords[1] == tile.m_boardPos[1]:
                    return True # collided with a tile on the board
        return False


    def shouldFixToBoard( self, board ):
        # tetrimino has reached bottom if any of the tiles in the current representation has collided
        # with another tile on the board or the bottom
        for tetriminoLocalCoords in self.m_representation[ self.m_currentRepIdx ]:
            tetriminoBoardCoords = ( tetriminoLocalCoords[ 0 ] + self.m_boardPos[ 0 ], tetriminoLocalCoords[ 1 ] + self.m_boardPos[ 1 ] )
            if tetriminoBoardCoords[ 1 ] >= board.s_scorePaneHeight + board.s_numTilesHeight -1:
                return True # reached bottom
            for tile in board.m_tilesFilled:
                if tetriminoBoardCoords[0] == tile.m_boardPos[0] and tetriminoBoardCoords[1] == tile.m_boardPos[1] -1:
                    return True # collided with a tile on the board
        return False


    def render( self ):
        for tetriminoLocalCoords in self.m_representation[ self.m_currentRepIdx ]:
            # create tile for each set of board coordinates and draw them!
            boardCoords = ( tetriminoLocalCoords[ 0 ] + self.m_boardPos[ 0 ], tetriminoLocalCoords[ 1 ] + self.m_boardPos[ 1 ] )
            tempTile = Tile( self.m_screen, self.m_surface, boardCoords )
            tempTile.render()
        return


# ---- #
class StraightPolyomino( Tetrimino ):

    """Class to represent a Straight Polyomino in the game"""
    
    def __init__( self, imageSurface, screenSurface ):
        # init base
        super( StraightPolyomino, self ).__init__( imageSurface, screenSurface )

        # create some representations
        super( StraightPolyomino, self ).addRepresentation( 0, [ (0,0), (1,0), (2,0), (3,0) ] )
        super( StraightPolyomino, self ).addRepresentation( 1, [ (0,0), (0,1), (0,2), (0,3) ] )

        return

# -- #
# -- #
class SquarePolyomino( Tetrimino ):

    """Class to represent a Square Polyomino in the game"""
    
    def __init__( self, imageSurface, screenSurface ):
        # init base
        super( SquarePolyomino, self ).__init__( imageSurface, screenSurface )

        # create some representations
        super( SquarePolyomino, self ).addRepresentation( 0, [ (0,0), (1,0), (1,1), (0,1) ] )

        return

# --- #
#  -  #
class TPolyomino( Tetrimino ):

    """Class to represent a T Polyomino in the game"""
    
    def __init__( self, imageSurface, screenSurface ):
        # init base
        super( TPolyomino, self ).__init__( imageSurface, screenSurface )

        # create some representations
        super( TPolyomino, self ).addRepresentation( 0, [ (0,1), (1,1), (2,1), (1,2) ] )
        super( TPolyomino, self ).addRepresentation( 1, [ (1,0), (1,1), (1,2), (2,1) ] )
        super( TPolyomino, self ).addRepresentation( 2, [ (0,1), (1,1), (2,1), (1,0) ] )
        super( TPolyomino, self ).addRepresentation( 3, [ (0,1), (1,0), (1,1), (1,2) ] )

        return

# --- #
#   - #
class JPolyomino( Tetrimino ):

    """Class to represent a J Polyomino in the game"""
    
    def __init__( self, imageSurface, screenSurface ):
        # init base
        super( JPolyomino, self ).__init__( imageSurface, screenSurface )

        # create some representations
        super( JPolyomino, self ).addRepresentation( 0, [ (0,0), (1,0), (2,0), (2,1) ] )
        super( JPolyomino, self ).addRepresentation( 1, [ (1,0), (1,1), (1,2), (0,2) ] )
        super( JPolyomino, self ).addRepresentation( 2, [ (0,1), (0,2), (1,2), (2,2) ] )
        super( JPolyomino, self ).addRepresentation( 3, [ (0,0), (1,0), (0,1), (0,2) ] )

        return


#   - #
# --- #
class LPolyomino( Tetrimino ):

    """Class to represent a L Polyomino in the game"""
    
    def __init__( self, imageSurface, screenSurface ):
        # init base
        super( LPolyomino, self ).__init__( imageSurface, screenSurface )

        # create some representations
        super( LPolyomino, self ).addRepresentation( 0, [ (0,1), (0,0), (1,0), (2,0) ] )
        super( LPolyomino, self ).addRepresentation( 1, [ (0,0), (1,0), (1,1), (1,2) ] )
        super( LPolyomino, self ).addRepresentation( 2, [ (0,1), (1,1), (2,1), (2,0) ] )
        super( LPolyomino, self ).addRepresentation( 3, [ (0,0), (0,1), (0,2), (1,2) ] )

        return


#  -- #
# --  #
class SPolyomino( Tetrimino ):

    """Class to represent a S Polyomino in the game"""
    
    def __init__( self, imageSurface, screenSurface ):
        # init base
        super( SPolyomino, self ).__init__( imageSurface, screenSurface )

        # create some representations
        super( SPolyomino, self ).addRepresentation( 0, [ (0,1), (1,1), (1,0), (2,0) ] )
        super( SPolyomino, self ).addRepresentation( 1, [ (0,0), (0,1), (1,1), (1,2) ] )

        return

# --  #
#  -- #
class ZPolyomino( Tetrimino ):

    """Class to represent a Z Polyomino in the game"""
    
    def __init__( self, imageSurface, screenSurface ):
        # init base
        super( ZPolyomino, self ).__init__( imageSurface, screenSurface )

        # create some representations
        super( ZPolyomino, self ).addRepresentation( 0, [ (0,0), (1,0), (1,1), (2,1) ] )
        super( ZPolyomino, self ).addRepresentation( 1, [ (2,0), (2,1), (1,1), (1,2) ] )

        return


class TetriminoManager:

    """Class to spawn and manage the currently controlled tetrimino in the game"""

    def __init__( self, screenSurface, board ):
        self.m_screenSurface = screenSurface 
        self.m_lastUpdateTimeMS = 0
        self.m_failed = False
        self.m_board = board
        self.m_spawner = TetriminoSpawner()
        # spawn an initial tetrimino
        self.spawnNewTetrimino()
        return


    # spawn and return a new tetrimino
    def spawnNewTetrimino( self ): 
        self.m_spawnedTetrimino = self.m_spawner.spawnTetrimino( self.m_screenSurface )
        return


    # moves the spawned tetrimino one unit down the board if possible
    # otherwise spawn a new tetrimino
    def moveTetriminoDown( self):
        moved = False
        if self.m_spawnedTetrimino.shouldFixToBoard( self.m_board ):
            # the tetrimino reached the top of the board? ( failed )
            if self.m_spawnedTetrimino.m_boardPos[ 1 ] <= board.Board.s_scorePaneHeight:
                self.m_failed = True
            else:
                # add coords to board
                self.m_board.fixTetrimino( self.m_spawnedTetrimino )
                # test the board for any complete lines
                self.m_board.testForCompleteLine()
                # spawn a new tetrimino
                self.spawnNewTetrimino()
        else:
            self.m_spawnedTetrimino.move( ( 0,1 ) )
            moved = True
        return moved


    # handle input
    def keyPressed( self, key ):
        if key == pygame.K_UP:
            if self.m_spawnedTetrimino.willCollideWithBoard( (0,0), self.m_board, True ) == False: 
                self.m_spawnedTetrimino.nextRepresentation()
        elif key == pygame.K_RIGHT:
            deltaPos = ( 1,0 )
            if self.m_spawnedTetrimino.willCollideWithBoard( deltaPos, self.m_board, False ) == False: 
                self.m_spawnedTetrimino.move( deltaPos )
        elif key == pygame.K_LEFT:  
            deltaPos = ( -1,0 )
            if self.m_spawnedTetrimino.willCollideWithBoard( deltaPos, self.m_board, False ) == False: 
                self.m_spawnedTetrimino.move( deltaPos )
        elif key == pygame.K_DOWN:
            self.moveTetriminoDown()
        elif key == pygame.K_SPACE :
            self.moveTetriminoDown()

        return


    def update( self ):
        # time to update the position of the spawned tetrimino (gravity)?
        currentTime = pygame.time.get_ticks()
        timeToMoveDown = currentTime - score.ScoreManager.s_speed >= self.m_lastUpdateTimeMS
        if timeToMoveDown:
            moved = self.moveTetriminoDown()
            if moved:
                self.m_lastUpdateTimeMS = currentTime
        return


    def render( self ):
        # draw the spawned tetrimino
        self.m_spawnedTetrimino.render()
        return


class TetriminoSpawner:

    """Class to spawn random tetriminos"""

    def spawnTetrimino( self, screenSurface ):
        randInt = random.randint( 0, len( TetriminoSpawner.s_tetriminoMap ) - 1 )
        return self.s_tetriminoMap[ randInt ]( self, screenSurface )
        
    def spawnStraightPolyomino( self, screenSurface ):
        return StraightPolyomino( pygame.image.load( "tile_red.png" ), screenSurface )

    def spawnSquarePolyomino( self, screenSurface ):
        return SquarePolyomino( pygame.image.load( "tile_light_blue.png" ), screenSurface )

    def spawnTPolyomino( self, screenSurface ):
        return TPolyomino( pygame.image.load( "tile_dark_blue.png" ), screenSurface )

    def spawnJPolyomino( self, screenSurface ):
        return JPolyomino( pygame.image.load( "tile_orange.png" ), screenSurface )

    def spawnLPolyomino( self, screenSurface ):
        return LPolyomino( pygame.image.load( "tile_yellow.png" ), screenSurface )

    def spawnSPolyomino( self, screenSurface ):
        return SPolyomino( pygame.image.load( "tile_green.png" ), screenSurface )

    def spawnZPolyomino( self, screenSurface ):
        return ZPolyomino( pygame.image.load( "tile_purple.png" ), screenSurface )

    s_tetriminoMap = { 0: spawnStraightPolyomino,
                       1: spawnSquarePolyomino,
                       2: spawnTPolyomino,
                       3: spawnJPolyomino,
                       4: spawnLPolyomino,
                       5: spawnSPolyomino,
                       6: spawnZPolyomino }
