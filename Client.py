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
from twisted.internet.task import LoopingCall
import cPickle as pickle
from CONSTANTS import *

from ClientSpace import ClientSpace

class Client_Protocol(Protocol):
	def __init__(self):
		self.cs = ClientSpace()
		self.lc = LoopingCall(self.send_mouse)

	def connectionMade(self):
		print 'Connected to the host'
		self.lc.start(float(1) / FRAMERATE)

	def send_mouse(self):
		mouse_pos = self.cs.get_mouse()
		self.transport.write("{0},{1}".format(mouse_pos[0], mouse_pos[1]))

	def dataReceived(self, data):
		try:
			info = pickle.loads(data)
			self.cs.update_screen(info)
		except:
			pass

	def connectionLost(self, reason):
		print 'Connection lost:', reason
		sys.exit()

class Client_Factory(ClientFactory):
	def buildProtocol(self, addr):
		return Client_Protocol()

reactor.connectTCP('fitz70@helios.nd.edu', 9300, Client_Factory())
reactor.run()
