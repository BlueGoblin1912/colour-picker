import pygame
import colorsys

class DisplayScreen(pygame.sprite.Sprite):
    def __init__(self, pos, groups,colour,saturation,luminosity):
        super().__init__(groups)
        self.hue = colorsys.rgb_to_hsv(float(colour[0]/255),float(colour[1]/255),float(colour[2]/255))[0]
        values = colorsys.hsv_to_rgb(self.hue,saturation,luminosity)
        self.hue = self.hue*360
        self.saturation = saturation*100
        self.luminosity = luminosity*100
        self.colour = []
        for i in range(3):
            self.colour.append(values[i]*255)
        self.image = pygame.Surface((1,1))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect(topleft = pos)

    def changeColour(self,hue):
        self.hue = colorsys.rgb_to_hsv(hue[0],hue[1],hue[2])[0]
        colour = colorsys.hsv_to_rgb(self.hue,self.saturation/100,self.luminosity/100)
        self.hue = self.hue*360
        self.colour = []
        for i in range(3):
            self.colour.append(colour[i]*255)
        self.image.fill(self.colour)

    def RGBtoHue(self,r,g,b):
        R = r/255
        G = g/255
        B = b/255
        if R > G and R > B:#R is the largest
            Hue = (G-B)/(R-min(G,B))
        elif G > R and G > B:#G is the largest
            Hue = 2 + (B-R)/(G-min(B,R))
        else:#B is the largest
            Hue = 4 +(R-G)/(B-min(R,G))
        
        Hue = Hue * 60
        if Hue < 0:
            Hue += 360
        return Hue

    
class DisplaySelector(pygame.sprite.Sprite):
    def __init__(self, groups,bar):
        super().__init__(groups)
        self.rect = pygame.Rect(277,24,15,15)
        self.pressed = False
        self.max = (284,284)
        self.min = (31,31)
        self.bar = bar

    def checkPressed(self):
        mousePos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]
        if click:
                if self.rect.collidepoint(mousePos) or self.bar.collidepoint(mousePos):
                    self.pressed = True
        if not click:
            self.pressed = False   
        
    def move(self):
        self.mousePos = pygame.mouse.get_pos()

        if self.pressed:
            self.rect.center = self.mousePos
            if self.rect.centery > self.max[1] :
                self.rect.centery = self.max[1]
            elif self.rect.centery < self.min[1] :
                self.rect.centery = self.min[1]              

            if self.rect.centerx > self.max[0]:
                self.rect.centerx = self.max[0]
            elif self.rect.centerx < self.min[0]:
                self.rect.centerx = self.min[0] 

    def update(self):
        self.checkPressed()
        self.move()