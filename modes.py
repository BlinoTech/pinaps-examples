import sys
import argparse

from pinaps.piNapsController import PiNapsController
from NeuroParser import NeuroParser

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

def onRawSignal(rawSignal):
    print("Raw value: %d" % rawSignal)

pinapsController = PiNapsController()

def main():
    argParser = argparse.ArgumentParser(description='Activate and control the Pinaps EEG sensor.')
    argParser.add_argument('control', default='I2C', choices=['GPIO', 'I2C'],
                    help='The pinaps control method.')
    argParser.add_argument('interface', default='UART', choices=['UART', 'I2C'],
                    help='The pinaps EEG sensor interface.')
    argParser.add_argument('mode', default='basic', choices=['basic', 'full'],
                    help='The pinaps EEG operating mode.')

    pinapArgs = argParser.parse_args()

    if(pinapArgs.control == 'GPIO'):
        pinapsController.setControlInterfaceGPIO()
    if(pinapArgs.control == 'I2C'):
        pinapsController.setControlInterfaceI2C()

    if(pinapArgs.interface == 'UART'):
        pinapsController.setEEGSensorInterfaceUART()
    if(pinapArgs.interface == 'I2C'):
        pinapsController.setEEGSensorInterfaceI2C()

    if(pinapArgs.mode == 'basic'):
        print("")
        print("Entering EEG basic mode.")
        print("Basic mode includes the following information: Signal Quality, Attention, Meditation & FFT powers.")
        pinapsController.setBasicMode()
    if(pinapArgs.mode == 'full'):
        print("")
        print("Entering EEG full mode.")
        print("Full mode includes the following information: Signal Quality, Attention, Meditation, FFT powers & raw signal.")
        pinapsController.setFullMode()

    aParser = NeuroParser()

    while True:
        data = pinapsController.readEEGSensor()
        for d in data:
            aParser.parse(d, printCallback)


if __name__ == '__main__':
    main()
