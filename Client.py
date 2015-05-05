# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

import sys

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
import cPickle as pickle

from GameSpace import GameSpace

class Client_Protocol(Protocol):
	def connectionMade(self):
		print 'Connected to the host'

	def dataReceived(self, data):
		info = pickle.loads(data)
		print "Server said:", info['balls']

		print 'Host said:', data


	def connectionLost(self, reason):
		print 'Connection lost:', reason
		sys.exit()

class Client_Factory(ClientFactory):
	def buildProtocol(self, addr):
		return Client_Protocol()

reactor.connectTCP('localhost', 9001, Client_Factory())
reactor.run()
