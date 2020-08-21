
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
    def renderCurrent(screen):
        MenuManager.CURRENT.render(screen)
    


class Menu():

    def __init__(self, windowSize, index):
        self.elements = ELEMENT_LAYOUTS[index]
    
    def click(self, location):
        buttons = filter(lambda x: isinstance(x, Button), self.elements)
        clicked = filter(lambda x: x.hasBeenClicked(location))
        if clicked: clicked[0].onClick()
    
    def render(self, screen):
        for element in self.elements:
            element.render(screen)



class Button():

    def __init__(self, location, size, onClick):
        self.location = location
        self.size = size
        self.onClick = onClick
    
    def hasBeenClicked(self, location):
        return (location[0] > self.location - self.size[0] // 2 and
                location[0] < self.location + self.size[0] // 2 and
                location[1] > self.location - self.size[1] // 2 and
                location[1] < self.location + self.size[1] // 2)
    
    def render(self, screen):
        




ELEMENT_LAYOUTS = {
    0: [
        Button((), (), lambda MenuManager.goto(MENU_GAME))
        Button((), (), lambda MenuManager.goto(MENU_SETTINGS))
    ]
}
