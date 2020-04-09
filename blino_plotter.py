import matplotlib.pyplot as plt
from pinaps.piNapsController import PiNapsController
from NeuroParser import NeuroParser

counter = 0
def main():
	counters = []
	deltas = []
	thetas = []
	lAlphas = []
	hAlphas = []
	lBetas = []
	hBetas = []
	lGammas = []
	mGammas = []

	plt.ion()
	plt.show()
	plt.draw()
	plt.pause(1.0)

	pinapsController = PiNapsController()
	pinapsController.defaultInitialise()
	def plotCallback(packet):
		if(packet.code == NeuroParser.DataPacket.kIntEEGPowers):
			global counter
			counter += 1
			deltas.append(packet.delta)
			thetas.append(packet.theta)
			lAlphas.append(packet.lAlpha)
			hAlphas.append(packet.hAlpha)
			lBetas.append(packet.lBeta)
			hBetas.append(packet.hBeta)
			lGammas.append(packet.lGamma)
			mGammas.append(packet.mGamma)
			counters.append(counter)

			plt.plot(counters, deltas)
			plt.plot(counters, thetas)
			plt.plot(counters, lAlphas)
			plt.plot(counters, hAlphas)
			plt.plot(counters, lBetas)
			plt.plot(counters, hBetas)
			plt.plot(counters, lGammas)
			plt.plot(counters, mGammas)
			plt.draw()
			plt.pause(0.001)

	aParser = NeuroParser()

	while True:
		data = pinapsController.readEEGSensor()
		aParser.parse(data, plotCallback)

if __name__ == '__main__':
    main()
