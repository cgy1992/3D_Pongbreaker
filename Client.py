# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import cPickle as pickle

from GameSpace import GameSpace

class Data_Client_Protocol(Protocol):
	def connectionMade(self):
		print 'Connected to the host'

	def dataReceived(self, data):
		info = pickle.loads(data)
		print "Server said:", info['balls']

	def connectionLost(self, reason):
		print "data connection lost"

class DataFactory(ClientFactory):
	def __init__(self):
		self.dataConnection = Data_Client_Protocol()

	def buildProtocol(self, addr):
		return self.dataConnection

if __name__ == '__main__':
	# For now, consider this the host main
	dataFactory = DataFactory()
	reactor.connectTCP("localhost", 9001, dataFactory)

	reactor.run()

