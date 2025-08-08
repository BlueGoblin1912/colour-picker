import pygame

class HSVBar(pygame.sprite.Sprite):
    def __init__(self,pos, groups,colour,value):
        super().__init__(groups)
        self.image = pygame.Surface((20,1))
        self.image.fill(colour)
        self.value = value
        self.colour = colour
        self.rect = self.image.get_rect(topleft = pos)

    def changeColour(self,colour):
        self.image.fill(colour)

class HSVSlider(pygame.sprite.Sprite):
    def __init__(self,x,y, groups,bar):
        super().__init__(groups)
        self.rect = pygame.Rect(x,y,31,12)
        self.pressed = False
        self.maxy = 22
        self.miny = 326
        self.bar = bar

    def checkPressed(self):
        mousePos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if click:
                if self.rect.collidepoint(mousePos) or self.bar.collidepoint(mousePos):
                    self.pressed = True
        if not click and self.pressed:
            self.pressed = False            
        
    def move(self):
        self.mousePos = pygame.mouse.get_pos()

        if self.pressed:
            self.rect.centery = self.mousePos[1]
            if self.rect.y < self.maxy:
                self.rect.y = self.maxy
            elif self.rect.y > self.miny:
                self.rect.y = self.miny                

    def update(self):
        self.checkPressed()
        self.move()
    
