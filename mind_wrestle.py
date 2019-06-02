import pygame

from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

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

    #Initialize the pygame module#
    pygame.init()
    
    #load and set the logo#
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("movement")
    
    #Create a surface on screen that has the size of 240 x 180#
    screen_width = 240
    screen_height = 180
    screen = pygame.display.set_mode((screen_width, screen_height))

    #load image (it is in same directory)#
    image = pygame.image.load("01_image.png")
    #Set the colorkey, so the pink border is not visible anymore#
    image.set_colorkey((255,0,255))
    #Set the alpha value to 128 (0 fully transparent, 255 opaque)#
    #image.set_alpha(128)
    bgd_image = pygame.image.load("background.png")

    #blit image(s) to screen#
    screen.blit(bgd_image,(0,0)) # first background
    #Instead of blitting the background image you could fill it 
    #(uncomment the next line to do so)
    #screen.fill((255,0,0))

    #Define the position of the smily#
    xpos = 90
    ypos = 50
    #How many pixels we move our smily each frame#
    step_x = 10
    step_y = 10
    
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
            xpos += 1
            #tugValue = tugValue + 10
        if(blinoParserOne.attention < blinoParserTwo.attention):
            xpos -= 1
            #tugValue = tugValue - 10
        ##Check within range##

        ##Update position##
        #xpos = tugValue

        #Now blit the smily on screen#
        screen.blit(image, (xpos, ypos))
        #And update the screen (dont forget that!)#
        pygame.display.flip()
        
        #This will slow it down to 10 fps, so you can watch it,#
        #Otherwise it would run too fast#
        clock.tick(10)




if __name__ == '__main__':
    main()
