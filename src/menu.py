import pygame
import board
import util

pygame.font.init()

class MenuManager():

    WINDOW_SIZE   = None
    MENU_MAIN     = None
    MENU_SETTINGS = None
    MENU_JOIN     = None
    GAME_SERVER   = None
    GAME_CLIENT   = None
    CURRENT       = None
    
    def __init__(self):
        pass

    @staticmethod
    def setWindowSize(size):
        MenuManager.WINDOW_SIZE = size
        MenuManager.init()

    @staticmethod
    def init():
        MenuManager.MENU_MAIN     = Menu(MenuManager.WINDOW_SIZE, 0)
        MenuManager.MENU_SETTINGS = Menu(MenuManager.WINDOW_SIZE, 1)
        MenuManager.MENU_JOIN     = Menu(MenuManager.WINDOW_SIZE, 2)
        MenuManager.GAME_SERVER   = Menu(MenuManager.WINDOW_SIZE, 3)
        MenuManager.GAME_CLIENT   = Menu(MenuManager.WINDOW_SIZE, 4)
        MenuManager.CURRENT = MenuManager.MENU_MAIN
    
    @staticmethod
    def goto(menu):
        MenuManager.CURRENT = menu
    
    @staticmethod
    def drawCurrent(screen):
        MenuManager.CURRENT.draw(screen)

    @staticmethod
    def handleClick(location):
        MenuManager.CURRENT.click(location)
    

class Menu():

    def __init__(self, windowSize, index):
        self.elements = ELEMENT_LAYOUTS[index]
    
    def click(self, location):
        clickables = filter(lambda x: isinstance(x, Button) or isinstance(x, board.Board), self.elements)
        clicked = filter(lambda x: x.hasBeenClicked(location), clickables)
        result  = list(clicked)
        if result: result[0].onClick(location)
    
    def draw(self, screen):
        for element in self.elements:
            element.draw(screen)


class Button():

    COLOR = pygame.Color(230, 230, 230)

    def __init__(self, text, relativeLocation, onClick, size=(240, 100), font='Arial'):
        self.relativeLocation = relativeLocation
        self.exactLocation = None
        self.size = size
        self.onClick = onClick
        self.rect = pygame.Rect((0,0), self.size)
        self.font = pygame.font.SysFont(font, 40)
        self.text = text
    
    def hasBeenClicked(self, location):
        return self.rect.collidepoint(location)
    
    def draw(self, screen):
        self.exactLocation = (screen.get_width()  * self.relativeLocation[0] // 100, 
                              screen.get_height() * self.relativeLocation[1] // 100)
        self.rect.center = self.exactLocation
        pygame.draw.rect(screen, Button.COLOR, self.rect)
        text = self.font.render(self.text, True, (0,0,0))
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)


class ButtonWithIndicator(Button):

    def __init__(self, text, relativeLocation, size=(240, 100), font='Arial'):
        super().__init__(text, relativeLocation, self.onClick, size, font)
        self.state = False
        self.indicatorRect = pygame.Rect(0, 0, self.size[1], self.size[1])
    
    def draw(self, screen):
        super().draw(screen)
        indicatorLocation = ((screen.get_width()  * self.relativeLocation[0] // 100) + 180, 
                              screen.get_height() * self.relativeLocation[1] // 100)
        self.indicatorRect.center = indicatorLocation
        if self.state:
            pygame.draw.rect(screen, util.GRAY, self.indicatorRect)
            text = self.font.render("ON", True, (0,0,0))
            text_rect = text.get_rect(center = self.indicatorRect.center)
            screen.blit(text, text_rect)
        else:
            pygame.draw.rect(screen, util.BLACK, self.indicatorRect)
            text = self.font.render("OFF", True, (255,255,255))
            text_rect = text.get_rect(center = self.indicatorRect.center)
            screen.blit(text, text_rect)
    
    def onClick(self, pos):
        self.state = not self.state


class Text():
     
    COLOR = pygame.Color(0, 0, 0)

    def __init__(self, text, relativeLocation, fontSize=25, font='Arial'):
        self.text = text
        self.relativeLocation = relativeLocation
        self.font = pygame.font.SysFont(font, fontSize)

    def draw(self, screen):
        self.exactLocation = (screen.get_width()  * self.relativeLocation[0] // 100, 
                              screen.get_height() * self.relativeLocation[1] // 100)
        text = self.font.render(self.text, True, (0,0,0))
        text_rect = text.get_rect(center = self.exactLocation)
        screen.blit(text, text_rect)
        
def updateBoards(board):
    ELEMENT_LAYOUTS[3][0] = board
    ELEMENT_LAYOUTS[4][0] = board

ELEMENT_LAYOUTS = {
    0: [
        Text("YACS", (50, 15), 100),
        Text("Yet Another Chess Simulator", (50, 25), 40),
        Button("Host Game", (50, 50), lambda pos: MenuManager.goto(MenuManager.GAME_SERVER)),
        Button("Join Game", (50, 65), lambda pos: MenuManager.goto(MenuManager.MENU_JOIN)),
        Button("Settings", (50, 80), lambda pos: MenuManager.goto(MenuManager.MENU_SETTINGS)),
    ],
    1: [
        ButtonWithIndicator("Setting1", (46, 30)),
        Button("Go Back", (50, 80), lambda pos: MenuManager.goto(MenuManager.MENU_MAIN)),
    ],
    2: [Button("Go Back", (50, 80), lambda pos: MenuManager.goto(MenuManager.MENU_MAIN)),],
    3: [
        board.Board(),
        Button("Quit Game", (80, 80), lambda pos: MenuManager.goto(MenuManager.MENU_MAIN)),
    ],
    4: [
        board.Board(),
        Button("Quit Game", (80, 80), lambda pos: MenuManager.goto(MenuManager.MENU_MAIN)),
    ],
}
