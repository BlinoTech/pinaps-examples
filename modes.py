import sys
import argparse

from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

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

    blinoParser = BlinoParser()

    while(1):
        while(pinapsController.dataWaiting()):
            ##Read Sensor##
            data = pinapsController.readEEGSensor()

            ##Parsing##
            blinoParser.parseByte(data)

            ##Printing##
            if(blinoParser.updatedFFT):
                packedd = blinoParser.parsedPacket

                print("")
                print("Quality value: %d" % packedd.quality)
                print("Attention value: %d" % packedd.attention)
                print("Meditation value: %d" % packedd.meditation)


if __name__ == '__main__':
    main()
