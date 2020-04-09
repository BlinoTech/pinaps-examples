from pinaps.piNapsController import PiNapsController
from NeuroParser import NeuroParser

pinapsController = PiNapsController()

def main():
    pinapsController.defaultInitialise()

    logFilename = "loggingExample.csv"
    logFile = open(logFilename, "wb")  # Open file to write as binary.

    csvHeaderString = "quality,attention,meditation,hAlpha,lAlpha,hBeta,lBeta,mGamma,lGamma,delta,theta\n"
    logFile.write(csvHeaderString)

    def logCallback(packet):
        if(packet.code == NeuroParser.DataPacket.kPoorQuality):
            logFile.write("")
            logFile.write(bytes(packet.poorQuality))
            logFile.write(",")
        if(packet.code == NeuroParser.DataPacket.kAttention):
            logFile.write(bytes(packet.attention))
            logFile.write(",")
        if(packet.code == NeuroParser.DataPacket.kMeditation):
            logFile.write(bytes(packet.meditation))
            logFile.write(",")
        if(packet.code == NeuroParser.DataPacket.kIntEEGPowers):
            logFile.write(bytes(packet.delta))
            logFile.write(",")
            logFile.write(bytes(packet.theta))
            logFile.write(",")
            logFile.write(bytes(packet.lAlpha))
            logFile.write(",")
            logFile.write(bytes(packet.hAlpha))
            logFile.write(",")
            logFile.write(bytes(packet.lBeta))
            logFile.write(",")
            logFile.write(bytes(packet.hBeta))
            logFile.write(",")
            logFile.write(bytes(packet.lGamma))
            logFile.write(",")
            logFile.write(bytes(packet.mGamma))
            logFile.write("\n")

    aParser = NeuroParser()

    while True:
        data = pinapsController.readEEGSensor()
        aParser.parse(data, logCallback)

if __name__ == '__main__':
    main()