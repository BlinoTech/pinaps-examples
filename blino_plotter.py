import matplotlib.pyplot as plt
from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

def main():

	counter = 1
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

	blinoParser = BlinoParser()

	while True:
		while pinapsController.dataWaiting():
			data = pinapsController.readEEGSensorBuffer()
		for d in data:
			blinoParser.parseByte(d)
		if(blinoParser.updatedFFT):
			packedd = blinoParser.parsedPacket
			if(packedd.quality < 26):
				print("Quality low enough for plot: %d", packedd.quality)
				deltas.append(packedd.EEGPowers.delta)
				thetas.append(packedd.EEGPowers.theta)
				lAlphas.append(packedd.EEGPowers.lAlpha)
				hAlphas.append(packedd.EEGPowers.hAlpha)
				lBetas.append(packedd.EEGPowers.lBeta)
				hBetas.append(packedd.EEGPowers.hBeta)
				lGammas.append(packedd.EEGPowers.lGamma)
				mGammas.append(packedd.EEGPowers.mGamma)
				counters.append(counter)
				counter += 1

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

if __name__ == '__main__':
    main()
