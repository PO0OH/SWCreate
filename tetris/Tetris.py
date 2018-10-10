import game
import sys
import board
import tetrimino

# game entry point
def main():

    # create the game
    resolution = ( board.Board.s_numTilesWidth * tetrimino.Tile.s_width , (board.Board.s_scorePaneHeight + board.Board.s_numTilesHeight) * tetrimino.Tile.s_height )
    theGame = game.Game( ( resolution ) )

    # update the game
    updateGame = True
    while updateGame:
        updateGame = theGame.update()

    # finished updating - quit
    theGame.quit()

    return

if __name__ == "__main__":
    main()
