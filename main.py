# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

from twisted.internet.protocol import Factory
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from CONSTANTS import FRAMERATE
from twisted.internet.task import LoopingCall
from GameSpace import GameSpace

gs = GameSpace()


class DataConnection(Protocol):
	def __init__(self):
		pass
		self.lc = LoopingCall(self.sendSprites)

	def connectionMade(self):
		print "Data Connection Made"
		gs.main()
		self.lc.start(float(1) / FRAMERATE)

	def sendSprites(self):
		print "Made it into sendSprite"
		gs.GameLoop()
		data = str(gs.paddle_1.rect.centerx) + ","
		print "Sending:", data
		self.transport.write(data)


class DataFactory(ServerFactory):
	def __init__(self):
		self.dataConnection = DataConnection()

	def buildProtocol(self, addr):
		return self.dataConnection


if __name__ == '__main__':
	# For now, consider this the host main
	dataFactory = DataFactory()
	reactor.listenTCP(9001, dataFactory)
	reactor.run()




