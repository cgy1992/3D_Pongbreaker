# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker
#
# FUTURE IMPROVEMENTS

from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from GameSpace import GameSpace
from CONSTANTS import FRAMERATE

class Data_Host_Protocol(Protocol):
	def __init__(self):
		self.gs = GameSpace()
		self.lc = LoopingCall(self.send_screen)

	def connectionMade(self):
		print 'Connected to client'
		self.lc.start(float(1) / FRAMERATE)

	def send_screen(self):
		print 'In send_screen'
		self.gs.gameloop()
		data = "Paddle 1 center x: {0}".format(self.gs.paddle_1.rect.centerx)
		print 'Sending:', data
		self.transport.write(data)

class Data_Factory(ServerFactory):
	def buildProtocol(self, addr):
		return Data_Host_Protocol()

reactor.listenTCP(9001, Data_Factory())
reactor.run()
