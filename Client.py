# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker

import cPickle as pickle
import sys

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from ClientSpace import ClientSpace
from CONSTANTS import FRAMERATE

class Client_Protocol(Protocol):
	def __init__(self):
		self.cs = ClientSpace()
		self.lc = LoopingCall(self.send_mouse)

	def connectionMade(self):
		print 'Connected to the host'
		self.lc.start(float(1) / FRAMERATE)

	def dataReceived(self, data):
		try:
			objects = pickle.loads(data)
			self.cs.update_screen(objects)
		except:
			pass

	def send_mouse(self):
		(mouse_x, mouse_y) = self.cs.get_mouse()
		mouse_pos_str = "{0},{1}".format(mouse_x, mouse_y)
		self.transport.write(mouse_pos_str)

	def connectionLost(self, reason):
		print 'Connection lost:', reason
		sys.exit()

class Client_Factory(ClientFactory):
	def buildProtocol(self, addr):
		return Client_Protocol()

reactor.connectTCP('fitz70', 9300, Client_Factory())
reactor.run()
