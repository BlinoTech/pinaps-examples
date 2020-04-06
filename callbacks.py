from pinaps.piNapsController import PiNapsController
from NeuroParser import NeuroParser

def printCallback(packet):
    if(packet.code == NeuroParser.DataPacket.kPoorQuality):
        print("Poor quality: " + str(packet.poorQuality))
    if(packet.code == NeuroParser.DataPacket.kAttention):
        print("Attention: " + str(packet.attention))
    if(packet.code == NeuroParser.DataPacket.kMeditation):
        print("Meditation: " + str(packet.meditation))
    if(packet.code == NeuroParser.DataPacket.kRawSignal):
        print("Raw: " + str(packet.rawSamples))
    if(packet.code == NeuroParser.DataPacket.kIntEEGPowers):
        print("Delta Powers: " + str(packet.delta))
        print("Theta Powers: " + str(packet.theta))
        print("Low Alpha Powers: " + str(packet.lAlpha))
        print("High Alpha Powers: " + str(packet.hAlpha))
        print("Low Beta Powers: " + str(packet.lBeta))
        print("High Beta Powers: " + str(packet.hBeta))
        print("Low Gamma Powers: " + str(packet.lGamma))
        print("Medium Gamma Powers: " + str(packet.mGamma))

pinapsController = PiNapsController()

def main():
    pinapsController.defaultInitialise()
    pinapsController.setFullMode()

    pinapsController.deactivateAllLEDs()

    aParser = NeuroParser()

    while True:
        data = pinapsController.readEEGSensor()
        for d in data:
            aParser.parse(d, printCallback)

if __name__ == '__main__':
    main()
