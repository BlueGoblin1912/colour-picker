import pygame
from sys import exit

class ColourPicker:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400,260))
        self.clock = pygame.time.Clock()

        self.sliderRects = {
            "red": {"slider": pygame.Rect(250,30,25,8),"bar": "../graphics/red.png"},
            "green": {"slider":pygame.Rect(300,30,25,8),"bar": "../graphics/green.png"},
            "blue": {"slider":pygame.Rect(350,30,25,8),"bar": "../graphics/blue.png"}
            }
        
        self.colourRect = pygame.Rect(30,30,180,180)
        self.colouring = (255,255,255)
        self.barHeight = 200

        self.redBar = pygame.image.load(self.sliderRects["red"]["bar"]).convert()
        self.redRect = self.redBar.get_rect(topleft = (252,30))
        self.greenBar = pygame.image.load(self.sliderRects["green"]["bar"]).convert()
        self.greenRect = self.greenBar.get_rect(topleft = (302,30))
        self.blueBar = pygame.image.load(self.sliderRects["blue"]["bar"]).convert()
        self.blueRect = self.blueBar.get_rect(topleft = (352,30))
        self.barRects = [[self.redRect,"red"],[self.greenRect,"green"],[self.blueRect,"blue"]]

    def draw(self):
        self.screen.blit(self.redBar,self.redRect)
        self.screen.blit(self.greenBar,self.greenRect)
        self.screen.blit(self.blueBar,self.blueRect)

        
        pygame.draw.rect(self.screen,"white",self.sliderRects["red"]["slider"])
        pygame.draw.rect(self.screen,"white",self.sliderRects["green"]["slider"])
        pygame.draw.rect(self.screen,"white",self.sliderRects["blue"]["slider"])
        pygame.draw.rect(self.screen,self.colouring,self.colourRect)

    def move(self):
        if pygame.mouse.get_focused():
            buttons = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            for rect in self.barRects:
                if buttons[0] and rect[0].collidepoint(pos[0],pos[1]):              
                    self.sliderRects[rect[1]]["slider"][1] = pos [1]
    
    def colour(self,colour):
        sliderHeight = 200 - (self.sliderRects[colour]["slider"].center[1] - 34)
        if sliderHeight == 0:
            value = 0
        else:
            value = (sliderHeight / self.barHeight) * 255
        return int(value)       


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.screen.fill("#222222")
            self.draw()
            self.move()
            red = self.colour("red")
            green = self.colour("green")
            blue = self.colour("blue")
            self.colouring = (red,green,blue)

            pygame.display.update()
            self.clock.tick(60)

def open():
    colourPicker = ColourPicker()
    colourPicker.run()
    
if __name__ == "__main__":
    open()