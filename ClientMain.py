# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS


from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

from GameSpace import GameSpace

##### Data Connection #####

class DataClient(Protocol):
	def connectionMade(self):
		print "connected to the server"

	def dataReceived(self, data):
		print "Server said:", data

	def connectionLost(self, reason):
		print "data connection lost"
		

class DataFactory(ClientFactory):
	def __init__(self):
		self.dataConnection = DataClient()

	def buildProtocol(self, addr):
		return self.dataConnection



if __name__ == '__main__':
	# For now, consider this the host main
	dataFactory = DataFactory()
	reactor.connectTCP("localhost", 9001, dataFactory)

	reactor.run()

