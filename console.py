import sys
import argparse

from pinaps.piNapsController import PiNapsController
from NeuroParser import NeuroParser

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
        logFile = open(logFilename, "wb") # Open file to write as binary.

    def eegCallback(packet):
        if(packet.code == NeuroParser.DataPacket.kPoorQuality):
            if(pinapArgs.printing):
                print("Poor quality: " + str(packet.poorQuality))
            if(pinapArgs.logging):
                logFile.write(bytes(packet.poorQuality))
        if(packet.code == NeuroParser.DataPacket.kAttention):
            if(pinapArgs.printing):
                print("Attention: " + str(packet.attention))
            if(pinapArgs.logging):
                logFile.write(bytes(packet.attention))
        if(packet.code == NeuroParser.DataPacket.kMeditation):
            if(pinapArgs.printing):
                print("Meditation: " + str(packet.meditation))
            if(pinapArgs.logging):
                logFile.write(bytes(packet.meditation))
        if(packet.code == NeuroParser.DataPacket.kRawSignal):
            if(pinapArgs.printing):
                print("Raw: " + str(packet.rawSamples))
            if(pinapArgs.logging):
                logFile.write(bytes(packet.rawSamples))
        if(packet.code == NeuroParser.DataPacket.kIntEEGPowers):
            if(pinapArgs.printing):
                print("Delta Powers: " + str(packet.delta))
                print("Theta Powers: " + str(packet.theta))
                print("Low Alpha Powers: " + str(packet.lAlpha))
                print("High Alpha Powers: " + str(packet.hAlpha))
                print("Low Beta Powers: " + str(packet.lBeta))
                print("High Beta Powers: " + str(packet.hBeta))
                print("Low Gamma Powers: " + str(packet.lGamma))
                print("Medium Gamma Powers: " + str(packet.mGamma))
            if(pinapArgs.logging):
                logFile.write(bytes(packet.delta))
                logFile.write(bytes(packet.theta))
                logFile.write(bytes(packet.lAlpha))
                logFile.write(bytes(packet.hAlpha))
                logFile.write(bytes(packet.lBeta))
                logFile.write(bytes(packet.hBeta))
                logFile.write(bytes(packet.lGamma))
                logFile.write(bytes(packet.mGamma))
                
    aParser = NeuroParser()

    while True:
        data = pinapsController.readEEGSensor()
        aParser.parse(data, eegCallback)


if __name__ == '__main__':
    main()
