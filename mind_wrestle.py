import pygame
from enum import Enum

from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

class GameState(Enum):
    Unconnected = 1
    Begin = 2
    InProgress = 3
    Halted = 4
    end = 5

##def onQualityValue(quality):
##    print("Quality value: %d" % quality)
##    if quality > 10:
##        pinapsOne.activateRedLED()
##        pinapsOne.deactivateGreenLED()
##        print ("RED");
##    else:
##        pinapsOne.deactivateRedLED()
##        pinapsOne.activateGreenLED()
##        print ("GREEN");

class AnimatedObject(pygame.sprite.Sprite):
    def __init__(self, animationRate, animationImages):
        super(AnimatedObject, self).__init__()

        self.animationIndex = 0
        self.animationRate = animationRate
        self.animationImages = animationImages
        self.image = self.animationImages[self.animationIndex]
        self.currentTick = 0
        self.rect = pygame.Rect(0, 0, 64, 64) #???
    
    def update(self, tick):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.currentTick += 1
        if(self.currentTick >= self.animationRate):
            self.animationIndex += 1
            self.currentTick = 0
        if self.animationIndex >= len(self.animationImages):
            self.animationIndex = 0
        self.image = self.animationImages[self.animationIndex]

    def imageSize(self, size):
        self.animationImages = [pygame.transform.scale(x, size) for x in self.animationImages]; self.animationImages

    def imagePos(self, pos):
        self.rect.center = pos

def onQualityValueOne(quality):
    print("")
    print("Pinaps ONE")
    print("Quality value: %d" % quality)

def onQualityValueTwo(quality):
    print("")
    print("Pinaps TWO")
    print("Quality value: %d" % quality)


def onAttention(attention):
    print("Attention value: %d" % attention)

def onMedititation(meditation):
    print("Meditation value: %d" % meditation)


def onEEGPowerReceived(eegSignal):
    print("Delta value: %d" % eegSignal.delta)
    print("Theta value: %d" % eegSignal.theta)
    print("Low alpha value: %d" % eegSignal.lAlpha)
    print("High alpha value: %d" % eegSignal.hAlpha)
    print("Low beta value: %d" % eegSignal.lBeta)
    print("High beta value: %d" % eegSignal.hBeta)
    print("Low Gamma value: %d" % eegSignal.lGamma)
    print("Medium gamma value: %d" % eegSignal.mGamma)

pinapsOne = PiNapsController()
pinapsTwo = PiNapsController(0x98)

def main():
    ##Setup game##
    tugValue = 120
    globalTick = 0

    #Initialize the pygame module#
    pygame.init()
    
    #load and set the logo#
    logo = pygame.image.load("resources/Blino_Logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Blino - Mind Wrestle")
    
    #Create a surface on screen that has the size of 240 x 180#
    displayInfo = pygame.display.Info()
    screen_width = displayInfo.current_w
    screen_height = displayInfo.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))

    #Plasma Sprite Setup#
    imgPlasmas = []
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma00.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma01.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma02.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma03.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma04.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma05.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma06.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma07.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma08.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma09.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma10.png'))
    imgPlasmas.append(pygame.image.load('resources/plasma/plasma11.png'))
    sptPlasma = AnimatedObject(15, imgPlasmas)
    sptPlasma.imageSize([128,128])
    sptPlasma.imagePos([0,0])
    group = pygame.sprite.Group(sptPlasma)

    #Set the alpha value to 128 (0 fully transparent, 255 opaque)#
    #image.set_alpha(128)
    #imgBackgrounds = []
    #imgBackgrounds.append(pygame.image.load("resources/background.png").convert_alpha())
    #sptBackground = AnimatedObject(1, imgBackgrounds)
    #sptBackground.imageSize([screen_width, screen_height])
    #Instead of blitting the background image you could fill it 
    #(uncomment the next line to do so)
    #screen.fill((255,0,0))
    #group = pygame.sprite.Group([sptBackground, sptPlasma])
    imgBackground = pygame.image.load("resources/background.png")
    imgBackground = pygame.transform.scale(imgBackground, [screen_width, screen_height])
    imgBackground = imgBackground.convert_alpha()

    #Define the position of the smily#
    xpos = 740
    ypos = 450
    #How many pixels we move our smily each frame#
    step_x = 20
    step_y = 20

    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()
    
    # a clock for controlling the fps later
    clock = pygame.time.Clock()

    ##Setup Pinaps##
    pinapsOne.setControlInterfaceI2C()
    pinapsOne.setEEGSensorInterfaceI2C()
    pinapsOne.setBasicMode()

    pinapsTwo.setControlInterfaceI2C()
    pinapsTwo.setEEGSensorInterfaceI2C()
    pinapsTwo.setBasicMode()

    blinoParserOne = BlinoParser()
    blinoParserOne.qualityCallback = onQualityValueOne
    blinoParserOne.attentionCallback = onAttention
    blinoParserOne.meditationCallback = onMedititation
    blinoParserOne.eegPowersCallback = onEEGPowerReceived

    blinoParserTwo = BlinoParser()
    blinoParserTwo.qualityCallback = onQualityValueTwo
    blinoParserTwo.attentionCallback = onAttention
    blinoParserTwo.meditationCallback = onMedititation
    blinoParserTwo.eegPowersCallback = onEEGPowerReceived

    pinapsOne.deactivateAllLEDs() 

    #Define a variable to control the main loop#
    running = True
    while(running):
        screen.fill((0,0,0))
        screen.blit(imgBackground,(0,0))

        #screen.fill((0,0,0))
        #Event handling, gets all event from the eventqueue#
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        while(pinapsOne.dataWaiting()):
            data = pinapsOne.readEEGSensor()
            blinoParserOne.parseByte(data)
        while(pinapsTwo.dataWaiting()):
            data = pinapsTwo.readEEGSensor()
            blinoParserTwo.parseByte(data)
        
        if(blinoParserOne.attention > blinoParserTwo.attention):
            xpos = (xpos + step_x) if (xpos + step_x < (screen_width - 40)) else (xpos)
            #tugValue = tugValue + 10
        if(blinoParserOne.attention < blinoParserTwo.attention):
            xpos = (xpos - step_x) if (xpos - step_x > 0) else (xpos)
            #tugValue = tugValue - 10
        ##Check within range##

        ##Update position##
        #xpos = tugValue

        ##Draw lines##
        #pygame.draw.line(screen,WHITE,(0,ypos+30),(xpos-30,ypos+30),2)
        #pygame.draw.line(screen,WHITE,(xpos,ypos+30),(screen_width - 40,ypos+30),2)

        #Now blit the smily on screen#
        #screen.blit(image, (xpos, ypos))
        sptPlasma.imagePos([xpos,ypos])
        group.draw(screen)
        group.update(globalTick)
        #And update the screen (dont forget that!)#
        pygame.display.flip()
        
        #This will slow it down to 10 fps, so you can watch it,#
        #Otherwise it would run too fast#
        clock.tick(60)
        globalTick = globalTick + 1

        #timeEnd = pygame.time.get_ticks
        #if(timeEnd - timeBegin < )




if __name__ == '__main__':
    main()
