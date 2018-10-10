import pygame
import tetrimino
import board
import score

class BaseState:

    """Base State"""

    def __init__( self ):
        self.m_transition = None
        return
    def enter( self, screen ):
        return
    def update( self ):
        return
    def render( self ):
        return
    def getTransition( self ):
        return self.m_transition

class IntroState( BaseState ):

    """Intro state"""

    def enter( self, screen ):
        self.m_screen = screen
        self.m_logo   = pygame.image.load( "logo.jpg" )

    def handleEvent( self, event ):
        if event.type == pygame.KEYDOWN:
            self.m_transition = InGameState()
        return

    def render( self ):
        logoRect = self.m_logo.get_rect()
        self.m_screen.blit( self.m_logo, logoRect )
        return

class GameOverState( BaseState ):


    def enter( self, screen ):
        self.m_screen = screen
        self.m_logo   = pygame.image.load( "gameover.jpg" )

    def handleEvent( self, event ):
        # 키보드에서 키를 눌러요
        if event.type == pygame.KEYDOWN:
            # 근데 그 키가 'q'라면?
            if event.key == pygame.K_q:
                # 게임 꺼버리기~
                pygame.display.quit()
            # 그 키가 'Q'가 아니라면?
            else:
                self.m_transition = InGameState()
        return

    def render( self ):
        logoRect = self.m_logo.get_rect()
        self.m_screen.blit( self.m_logo, logoRect )
        return

class InGameState( BaseState ):

    """In-game state"""

    def handleEvent( self, event ):
        if event.type == pygame.KEYDOWN:
            self.m_tetriminoMgr.keyPressed( event.key ) 
        return

    def enter( self, screen ):
        # initialise board
        # initialise tetrimino manager
        self.m_transition = None
        self.m_board        = board.Board( screen )
        self.m_tetriminoMgr = tetrimino.TetriminoManager( screen,self.m_board )
        return

    def update( self ):
        # update the game
        self.m_tetriminoMgr.update()
        # failed?
        if self.m_tetriminoMgr.m_failed:
            self.m_transition = GameOverState()
        return

    def render( self ):
        # render the game
        self.m_board.render()
        self.m_tetriminoMgr.render()
        return


class Game:

    """Main game object"""

    def __init__( self, resolution ):

        assert resolution[0] > 0 and resolution[1] > 0
        print ( "Initialising game (window width", resolution[0], ", window height", resolution[1], ")" )

        # initialise pygame
        pygame.init()
        self.m_screen = pygame.display.set_mode( resolution )
        pygame.display.set_caption( "Tetris!" )
        pygame.display.set_icon( pygame.image.load( "tile_red.png" ) )
        # enter a state
        self.m_gameState = IntroState()
        self.m_gameState.enter( self.m_screen )
        return


    def update( self ):
        # detect a state transition
        if self.m_gameState.getTransition() != None:
            self.m_gameState = self.m_gameState.getTransition()
            self.m_gameState.enter( self.m_screen )

        # handle pygame events
        for event in pygame.event.get():
            self.m_gameState.handleEvent( event )
            if event.type == pygame.QUIT: 
                return False

        # update the state
        self.m_gameState.update()

        # clear the screen
        self.m_screen.fill((0,0,0))

        # render the state
        self.m_gameState.render()

        # flip
        pygame.display.flip()

        return True


    def quit( self ):
        # quit pygame
        pygame.display.quit()
        return
