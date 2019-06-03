import pygame

from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

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

class PlasmaBall(pygame.sprite.Sprite):
    def __init__(self):

        super(PlasmaBall, self).__init__()
        self.images = []
        self.images.append(pygame.image.load('resources/plasma/plasma00.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma01.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma02.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma03.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma04.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma05.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma06.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma07.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma08.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma09.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma10.png'))
        self.images.append(pygame.image.load('resources/plasma/plasma11.png'))

        for pos in range(len(self.images)):
            self.images[pos] = pygame.transform.scale(self.images[pos], (128, 128))

        #self.images.append(self.image3)
        # assuming both images are 64x64 pixels

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(5, 5, 64, 64)
        self.currentTick = 0
        self.animationTick = 0

    def update(self, tick, position):
        '''This method iterates through the elements inside self.images and 
        displays the next one each tick. For a slower animation, you may want to 
        consider using a timer of some sort so it updates slower.'''
        self.currentTick += 1
        if(self.currentTick >= self.animationTick):
            self.index += 1
            self.currentTick = 0
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]

        self.rect.center = position

    def setAnimationTick(self, tick):
        self.animationTick = tick

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
    tick = 0

    #Initialize the pygame module#
    pygame.init()
    
    #load and set the logo#
    logo = pygame.image.load("resources/logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("movement")
    
    #Create a surface on screen that has the size of 240 x 180#
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    #load image (it is in same directory)#
    image = pygame.image.load("resources/01_image.png")
    #Set the colorkey, so the pink border is not visible anymore#
    image.set_colorkey((255,0,255))
    sprite = PlasmaBall()
    sprite.setAnimationTick(15)
    group = pygame.sprite.Group(sprite)

    #Set the alpha value to 128 (0 fully transparent, 255 opaque)#
    #image.set_alpha(128)
    bgd_image = pygame.image.load("resources/background.png")

    #blit image(s) to screen#
    screen.blit(bgd_image,(0,0)) # first background
    #Instead of blitting the background image you could fill it 
    #(uncomment the next line to do so)
    #screen.fill((255,0,0))

    #Define the position of the smily#
    xpos = 740
    ypos = 450
    #How many pixels we move our smily each frame#
    step_x = 20
    step_y = 20
    
    #And blit it on screen#
    screen.blit(image, (xpos, ypos))
    
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
        #timeBegin = pygame.time.get_ticks()

        screen.fill((0,0,0))
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
        pygame.draw.line(screen,WHITE,(0,ypos+30),(xpos-30,ypos+30),2)
        pygame.draw.line(screen,WHITE,(xpos,ypos+30),(screen_width - 40,ypos+30),2)

        #Now blit the smily on screen#
        #screen.blit(image, (xpos, ypos))
        group.draw(screen)
        group.update(tick, [xpos, ypos])
        #And update the screen (dont forget that!)#
        pygame.display.flip()
        
        #This will slow it down to 10 fps, so you can watch it,#
        #Otherwise it would run too fast#
        clock.tick(60)
        tick = tick + 1

        #timeEnd = pygame.time.get_ticks
        #if(timeEnd - timeBegin < )




if __name__ == '__main__':
    main()
