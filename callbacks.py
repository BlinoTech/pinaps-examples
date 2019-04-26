from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

def onQualityValue(quality):
    print("Quality value: %d" % quality)
    if quality > 10:
        pinapsController.activateRedLED()
        pinapsController.deactivateGreenLED()
        print ("RED");
    else:
        pinapsController.deactivateRedLED()
        pinapsController.activateGreenLED()
        print ("GREEN");


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

pinapsController = PiNapsController()

def main():
    pinapsController.defaultInitialise()

    blinoParser = BlinoParser()
    blinoParser.qualityCallback = onQualityValue
    blinoParser.attentionCallback = onAttention
    blinoParser.meditationCallback = onMedititation
    blinoParser.eegPowersCallback = onEEGPowerReceived

    pinapsController.deactivateAllLEDs() 

    while(1):
        while(pinapsController.dataWaiting()):
            data = pinapsController.readEEGSensor()
            blinoParser.parseByte(data)

if __name__ == '__main__':
    main()
