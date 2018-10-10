import pygame
import tetrimino
import score

class Board:

    """Class that represents the board. 
        Allows tiles to be set when a tetrimino reaches
        the bottom of the screen"""
        
    s_scorePaneHeight = 1

    s_numTilesWidth  = 16
    s_numTilesHeight = 25

    def __init__( self, screenSurface ):
        # array of tiles ( the filled parts of the board )
        self.m_screenSurface = screenSurface
        self.m_font          = pygame.font.SysFont( "monospace", 15 )
        self.resetForGame()
        return

    
    def resetForGame( self ):
        # clear the tile array
        self.m_tilesFilled = []
        score.ScoreManager.s_lines = 0
        return


    # fix the passed tetrimino to the board
    def fixTetrimino( self, passedTetrimino ):
        assert passedTetrimino.shouldFixToBoard( self )
        # create a tile from each of the coords in the tetriminos current representation
        for tetriminoLocalCoords in passedTetrimino.m_representation[ passedTetrimino.m_currentRepIdx ]:
            boardCoords = [ tetriminoLocalCoords[ 0 ] + passedTetrimino.m_boardPos[ 0 ], tetriminoLocalCoords[ 1 ] + passedTetrimino.m_boardPos[ 1 ] ]
            self.m_tilesFilled.append( tetrimino.Tile( self.m_screenSurface, passedTetrimino.m_surface, boardCoords ) )
        return


    def testForCompleteLine( self ):
        numRowsCompleted = 0
        tilesFilledInRow = []
        for rowIdx in range( 0, Board.s_numTilesHeight ):
            tilesFilledInRow.append( 0 )

        for tile in self.m_tilesFilled:
            tileRowIdx = tile.m_boardPos[ 1 ] - Board.s_scorePaneHeight
            tilesFilledInRow[ tileRowIdx ] = tilesFilledInRow[ tileRowIdx ] + 1

        for rowIdx in range( 0, Board.s_numTilesHeight ):
            if tilesFilledInRow[ rowIdx ] == Board.s_numTilesWidth:
                # row filled!
                # destroy tiles at that row
                # move tiles above - downwards
                self.destroyRow( rowIdx + Board.s_scorePaneHeight )
                self.moveTilesDown( rowIdx + Board.s_scorePaneHeight )
                score.ScoreManager.addLine()
        return numRowsCompleted


    # destroys all tiles on the passed row
    def destroyRow( self, rowIdx ):
        tilesToRemove = []
        for tile in self.m_tilesFilled:
            if rowIdx == tile.m_boardPos[ 1 ]:
                tilesToRemove.append( tile )

        for tile in tilesToRemove:
            self.m_tilesFilled.remove( tile )
        return


    # moves any tiles on the rows above rowIdx downwards by 1 tile
    def moveTilesDown( self, rowIdx ):
        for tile in self.m_tilesFilled:
            if tile.m_boardPos[ 1 ] < rowIdx:
                tile.m_boardPos[ 1 ] = tile.m_boardPos[ 1 ] + 1
        return


    # render filled parts of the board
    def render( self ):
        # render score pane
        fontSurface = self.m_font.render( "Lines:" + str( score.ScoreManager.s_lines ), 1, ( 255, 255, 255 ) )
        self.m_screenSurface.blit( fontSurface, (10,10) )

        # render tiles
        for tile in self.m_tilesFilled:
            tile.render()
        return
