from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

pinapsController = PiNapsController()

def main():
    pinapsController.defaultInitialise()
    #pinapsController.setControlInterfaceI2C()
    #pinapsController.setEEGSensorInterfaceI2C()
    #pinapsController.setBasicMode()

    logFilename = "loggingExample.csv"
    logFile = open(logFilename, "wb")  # Open file to write as binary.

    csvHeaderString = "quality,attention,meditation,hAlpha,lAlpha,hBeta,lBeta,mGamma,lGamma,delta,theta\n"
    logFile.write(csvHeaderString)

    blinoParser = BlinoParser()

    while True:
        while pinapsController.dataWaiting():
            #Reading EEG.
            data = pinapsController.readEEGSensor()

            #Parsing.
            blinoParser.parse(data)

            #Printing.
            if(blinoParser.updatedFFT):
                packedd = blinoParser.parsedPacket

                logFile.write("")
                logFile.write(bytes(packedd.quality))
                logFile.write(",")
                logFile.write(bytes(packedd.attention))
                logFile.write(",")
                logFile.write(bytes(packedd.meditation))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.delta))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.theta))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.lAlpha))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.hAlpha))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.lBeta))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.hBeta))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.lGamma))
                logFile.write(",")
                logFile.write(bytes(packedd.EEGPowers.mGamma))
                logFile.write("\n")

if __name__ == '__main__':
    main()