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
import cPickle as pickle


class Data_Host_Protocol(Protocol):
	def __init__(self):
		self.gs = GameSpace()
		self.lc = LoopingCall(self.send_screen)

	def connectionMade(self):
		print 'Connected to client'
		self.lc.start(float(1) / FRAMERATE)

	def dataReceived(self, data):
		# Host has received that player 2 moved his mouse, update paddle
		positions = data.split(',')
		self.gs.paddle_2.manual_x = positions[0]
		self.gs.paddle_2.manual_y = positions[1]

	def send_screen(self):
		print 'In send_screen'
		self.gs.gameloop()
		data = { 'p1' : self.gs.paddle_1.rect.center,
				 'p2' : self.gs.paddle_2.rect.center
				}

		balls = []
		for ball in self.gs.balls:
			balls.append((ball.rect.topleft, ball.z_pos))
		bricks = []
		for brick in self.gs.bricks:
			bricks.append((brick.rect.topleft, brick.z_pos, brick.color))
		
		data['balls'] = balls
		data['bricks'] = bricks

		pd = pickle.dumps(data)
		data = "Paddle 1 center x: {0}".format(self.gs.paddle_1.rect.centerx)
		print 'Sending:', data
		self.transport.write(pd)

class Data_Factory(ServerFactory):
	def buildProtocol(self, addr):
		return Data_Host_Protocol()

reactor.listenTCP(9001, Data_Factory())
reactor.run()
