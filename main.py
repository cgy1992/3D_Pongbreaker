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
from datetime import datetime
from twisted.internet.task import LoopingCall
from GameSpace import GameSpace

gs = GameSpace()


class DataConnection(Protocol):
	def __init__(self):
		pass
		self.lc = LoopingCall(self.sendSprites)

	def connectionMade(self):
		print "Data Connection Made"
		gs.main(self)

	def sendSprites(self):
		print "Made it into sendSprite"
		#data = str(gs.ball.z_pos) + ","
		#print "Sending:", data
		self.transport.write("hello")


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




