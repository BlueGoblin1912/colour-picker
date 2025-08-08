import pygame
from displayScreen import *
from hueBar import *
import colorsys
from sys import exit

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((465,495))
        pygame.display.set_caption("Colour picker")
        icon = pygame.image.load("logo.png").convert_alpha()
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        #groups
        self.visibleSprites = pygame.sprite.Group()
        self.displaySprites = pygame.sprite.Group()
        self.hueSprites = pygame.sprite.Group()
        self.saturationSprites = pygame.sprite.Group()
        self.sliderSprites = pygame.sprite.Group()
        self.vibranceSprites = pygame.sprite.Group()

        self.colour = (255,0,0)
        self.createPixelGrid()
        self.createBars()
        self.pressed = None

        #values
        self.prevSelectorPos = (0,0)
        self.prevHuePos = (0,0)
        self.hue = 0
        self.saturation = 100
        self.vibrance = 100
        self.CMYK = []

        #font
        pygame.font.init()
        self.font = pygame.font.Font("../fonts/font.ttf",20)

    def createPixelGrid(self):
        self.borderSurf = pygame.Rect(25,25,266,266)
        for x in range(256):
            saturation = (x/ 255)
            for y in range(256):
                luminosity = (y/255)
                DisplayScreen((x+30,255-y+30),[self.visibleSprites,self.displaySprites],self.colour,saturation,luminosity)
    
    def createBars(self):
        #hue bar
        self.hue = [255,0,0]
        barChange = 3
        for y in range(305):
            HSVBar((330,28+y),[self.visibleSprites,self.hueSprites],self.hue.copy(),self.hue)
            if self.hue[0] == 255:
                if self.hue[2] != 0:
                    self.hue[2] -= 5
                elif self.hue[1] != 255:
                    self.hue[1] += 5
            if self.hue[1] == 255:
                if self.hue[0] != 0:
                    self.hue[0] -= 5
                elif self.hue[2] != 255:
                    self.hue[2] += 5
            if self.hue[2] == 255:
                if self.hue[1] != 0:
                    self.hue[1] -= 5
                elif self.hue[0] != 255:
                    self.hue[0] += 5
        self.hueBorderRect = pygame.Rect(326,25,27,311)      
        self.hueSlider = HSVSlider(324,22,[self.sliderSprites],self.hueBorderRect)

        #colour selector
        self.displaySelector = DisplaySelector([self.sliderSprites],self.borderSurf)  

        #Saturation slider
        saturation = 1
        for y in range(305):
            saturation = 1-(y/304)
            r,g,b = colorsys.hsv_to_rgb(colorsys.rgb_to_hsv(self.colour[0],self.colour[1],self.colour[2])[0],saturation,1)
            
            HSVBar((375,28+y),[self.visibleSprites,self.saturationSprites],(round(r*255),round(g*255),round(b*255)),saturation)

        self.satBorderRect = pygame.Rect(371,25,27,311)
        self.satSlider = HSVSlider(369,22,[self.sliderSprites],self.satBorderRect)

        #vibrance slider
        for y in range(305):
            vibrance = 1-(y/304)
            r,g,b = colorsys.hsv_to_rgb(colorsys.rgb_to_hsv(self.colour[0],self.colour[1],self.colour[2])[0],1,vibrance)
            
            HSVBar((420,28+y),[self.visibleSprites,self.vibranceSprites],(round(r*255),round(g*255),round(b*255)),vibrance)

        self.vibBorderRect = pygame.Rect(416,25,27,311)
        self.vibSlider = HSVSlider(414,22,[self.sliderSprites],self.vibBorderRect)

    def draw(self):
        for sprite in self.visibleSprites:
            self.screen.blit(sprite.image,sprite.rect)
        pygame.draw.rect(self.screen,"#222222",self.borderSurf,5)
        pygame.draw.rect(self.screen,"#222222",self.hueBorderRect,5)
        pygame.draw.rect(self.screen,"#222222",self.satBorderRect,5)
        pygame.draw.rect(self.screen,"#222222",self.vibBorderRect,5)
        pygame.draw.rect(self.screen,"#555555",self.hueSlider.rect,3)
        pygame.draw.rect(self.screen,"#555555",self.satSlider.rect,3)
        pygame.draw.rect(self.screen,"#555555",self.vibSlider.rect,3)
        pygame.draw.rect(self.screen,"#111111",self.displaySelector.rect,3)

    def getValues(self):
        if self.prevSelectorPos != self.displaySelector.rect.center or self.prevHuePos != self.hueSlider.rect.center:
            for sprite in self.displaySprites:
                if sprite.rect.collidepoint(self.displaySelector.rect.center):
                    self.prevSelectorPos = self.displaySelector.rect.center
                    self.prevHuePos = self.hueSlider.rect.center
                    self.saturation = round(sprite.saturation)
                    self.vibrance = round(sprite.luminosity)
            for sprite in self.hueSprites:
                if sprite.rect.collidepoint(self.hueSlider.rect.center):
                    self.colour = sprite.colour
                    self.hue = round(colorsys.rgb_to_hsv(self.colour[0],self.colour[1],self.colour[2])[0]*360)
                    for sprite in self.displaySprites:
                        sprite.changeColour(self.colour)

    def changeHSVvalues(self):
        if self.vibSlider.pressed or self.satSlider.pressed:
            pressed = True
        else:
            pressed = False

        if pressed:
            satRatio = self.satSlider.rect.centery/304
            vibRatio = self.vibSlider.rect.centery/304
            xpos = round(255-satRatio*255)
            ypos = round(vibRatio*255)
            self.displaySelector.rect.center = (53+xpos,7+ypos)
        else:
            xpos = self.displaySelector.rect.centerx/255
            ypos = self.displaySelector.rect.centery/255
            satRatio = round(361-(xpos*304))
            vibRatio = round((ypos*304)-15)
            self.satSlider.rect.y = satRatio
            self.vibSlider.rect.y = vibRatio

    def rgb_to_cmyk(self,r, g, b):
        if (r, g, b) == (0, 0, 0):
            return 0, 0, 0, 100
        c = 1 - r / 255
        m = 1 - g / 255
        y = 1 - b / 255
        min_cmy = min(c, m, y)
        c = (c - min_cmy) / (1 - min_cmy)
        m = (m - min_cmy) / (1 - min_cmy)
        y = (y - min_cmy) / (1 - min_cmy)
        k = min_cmy
        return round(c * 100), round(m * 100), round(y * 100), round(k * 100)
  
    def displayInfo(self):
        #RGB values
        R,G,B = colorsys.hsv_to_rgb(self.hue/360,self.saturation/100,self.vibrance/100)
        rgb = self.font.render(f"RGB:",False,"#666666")
        rgbrect = rgb.get_rect(topleft = (25,360))#25,315
        self.screen.blit(rgb,rgbrect)
        self.displayText(round(R*255),102,360,60,18)
        self.displayText(round(G*255),177,360,60,18)
        self.displayText(round(B*255),252,360,60,18)

        #HLS values
        hls = self.font.render(f"HSV:",False,"#666666")
        hlsrect = hls.get_rect(topleft = (25,405))
        self.screen.blit(hls,hlsrect)
        self.displayText(self.hue,102,405,60,18)
        self.displayText(self.saturation,177,405,60,18)
        self.displayText(self.vibrance,252,405,60,18)

        #CMYK values
        C,M,Y,K = self.rgb_to_cmyk(R*255,G*255,B*255)
        cmyk = self.font.render(f"CMYK:",False,"#666666")
        cmykrect = hls.get_rect(topleft = (25,450))
        self.screen.blit(cmyk,cmykrect)
        self.displayText(C,127,450,60,18)
        self.displayText(M,202,450,60,18)
        self.displayText(Y,277,450,60,18)
        self.displayText(K,352,450,60,18)

        #Hex values
        
        Hex = "#{:02X}{:02X}{:02X}".format(int(round(R*255)), int(round(G*255)), int(round(B*255)))
        hex = self.font.render(f"HEX:",False,"#666666")
        hexrect = hex.get_rect(topleft = (25,315))#125,425
        self.screen.blit(hex,hexrect)
        self.displayText(Hex,102,315,155,18)#205,425

        #colour preview window
        self.colourSurf = pygame.surface.Surface((85,85))
        self.colourSurf.fill((round(R*255),round(G*255),round(B*255)))
        self.colourRect = self.colourSurf.get_rect(center = (385,390))
        self.screen.blit(self.colourSurf,self.colourRect)
        pygame.draw.rect(self.screen,"#222222",self.colourRect,5)


    def displayText(self,text,x,y,h,w):
        surf = self.font.render(f"{text}",False,"#666666")
        rect = pygame.Rect(x,y,h,w)
        borderRect = rect.inflate(10,10)
        pygame.draw.rect(self.screen,"#AAAAAA",borderRect)
        pygame.draw.rect(self.screen,"#222222",borderRect,3)
        self.screen.blit(surf,rect)

    def updateSliders(self):
        if self.pressed == None:
            for sprite in self.sliderSprites:
                sprite.update()
                if sprite.pressed:
                    self.pressed = sprite
                    break
        else:
            self.pressed.update()
            if self.pressed.pressed == False:
                self.pressed = None

    def update(self):
        self.getValues()
        self.updateSliders()
        self.changeHSVvalues()
        self.draw()
        self.displayInfo()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            self.screen.fill("#333333")
            self.update()
            pygame.display.update()
            self.clock.tick(60)
    
if __name__ == "__main__":
    colourPicker = Game()
    colourPicker.run()