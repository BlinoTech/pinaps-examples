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
    argParser.add_argument('-l', default='eeg.log', dest='logging',
                    help='Log to specified file.')
    argParser.add_argument('-p', dest='printing', action='store_true',
                    help='Print to console.')

    pinapArgs = argParser.parse_args()
    #print(pinapArgs)

    if(pinapArgs.control == 'GPIO'):
        pinapsController.setControlInterfaceGPIO()
    if(pinapArgs.control == 'I2C'):
        pinapsController.setControlInterfaceI2C()

    if(pinapArgs.interface == 'UART'):
        pinapsController.setEEGSensorInterfaceUART()
    if(pinapArgs.interface == 'I2C'):
        pinapsController.setEEGSensorInterfaceI2C()

    if(pinapArgs.mode == 'basic'):
        pinapsController.setBasicMode()
    if(pinapArgs.mode == 'full'):
        pinapsController.setFullMode()

    if(pinapArgs.logging != None):
        logFilename = pinapArgs.logging
        logFile = open(logFilename, "wb") # file to write to

    blinoParser = BlinoParser()

    while(1):
        while(pinapsController.dataWaiting()):
            ##Read Sensor##
            data = pinapsController.readEEGSensor()

            ##Parsing##
            blinoParser.parseByte(data)

            ##Printing##
            if(pinapArgs.printing and blinoParser.updatedFFT):
                packedd = blinoParser.parsedPacket

                print("")
                print("Quality value: %d" % packedd.quality)
                print("Attention value: %d" % packedd.attention)
                print("Meditation value: %d" % packedd.meditation)
                print("Delta value: %d" % packedd.EEGPowers.delta)
                print("Theta value: %d" % packedd.EEGPowers.theta)
                print("Low alpha value: %d" % packedd.EEGPowers.lAlpha)
                print("High alpha value: %d" % packedd.EEGPowers.hAlpha)
                print("Low beta value: %d" % packedd.EEGPowers.lBeta)
                print("High beta value: %d" % packedd.EEGPowers.hBeta)
                print("Low Gamma value: %d" % packedd.EEGPowers.lGamma)
                print("Medium gamma value: %d" % packedd.EEGPowers.mGamma)
            if(pinapArgs.printing and blinoParser.updatedRaw):
                print("Raw value: %d" % blinoParser.raw)

            ##Logging##
            if(pinapArgs.logging and blinoParser.updatedFFT):
                packedd = blinoParser.parsedPacket

                logFile.write("")
                logFile.write(bytes(packedd.quality))
                logFile.write(bytes(packedd.attention))
                logFile.write(bytes(packedd.meditation))
                logFile.write(bytes(packedd.EEGPowers.delta))
                logFile.write(bytes(packedd.EEGPowers.theta))
                logFile.write(bytes(packedd.EEGPowers.lAlpha))
                logFile.write(bytes(packedd.EEGPowers.hAlpha))
                logFile.write(bytes(packedd.EEGPowers.lBeta))
                logFile.write(bytes(packedd.EEGPowers.hBeta))
                logFile.write(bytes(packedd.EEGPowers.lGamma))
                logFile.write(bytes(packedd.EEGPowers.mGamma))
            if(pinapArgs.logging and blinoParser.updatedRaw):
                logFile.write(bytes(blinoParser.raw))


if __name__ == '__main__':
    main()
