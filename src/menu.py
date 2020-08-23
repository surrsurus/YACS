import pygame
from src import board


class MenuManager():

    WINDOW_SIZE   = None
    MENU_MAIN     = None
    MENU_SETTINGS = None
    MENU_JOIN     = None
    MENU_GAME     = None
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
        MenuManager.MENU_GAME     = Menu(MenuManager.WINDOW_SIZE, 3)
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

    def __init__(self, text, relativeLocation, size, onClick):
        pygame.font.init()
        self.relativeLocation = relativeLocation
        self.exactLocation = None
        self.size = size
        self.onClick = onClick
        self.rect = pygame.Rect((0,0), self.size)
        self.font = pygame.font.SysFont('Arial', 25)
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




ELEMENT_LAYOUTS = {
    0: [
        Button("test1", (50, 50), (200, 50), lambda pos: MenuManager.goto(MenuManager.MENU_GAME))
    ],
    1: [],
    2: [],
    3: [board.Board()],
}
