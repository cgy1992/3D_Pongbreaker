# Tim Pusateri
# Jon Richelsen
# CSE30332
# Final Project: PyGame + Twisted
# 3D_Pongbreaker

import cPickle as pickle
import sys

from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from GameSpace import GameSpace
from CONSTANTS import FRAMERATE

class Host_Protocol(Protocol):
	def __init__(self):
		self.gs = GameSpace()
		self.lc = LoopingCall(self.send_objects)

	def connectionMade(self):
		print 'Connected to client'
		self.lc.start(float(1) / FRAMERATE)

	def dataReceived(self, data):
		try:
			(mouse_x, mouse_y, launch_paddle_2) = data.split(',')
			self.gs.paddle_2.manual_x = int(mouse_x)
			self.gs.paddle_2.manual_y = int(mouse_y)
			if int(launch_paddle_2) is 1:
				self.gs.paddle_2.launch = True
			elif int(launch_paddle_2) is 0:
				self.gs.paddle_2.launch = False
		except:
			pass

	def send_objects(self):
		self.gs.gameloop()

		objects = {
			'p1' : (self.gs.paddle_1.rect.center, self.gs.paddle_1.score),
			'p2' : (self.gs.paddle_2.rect.center, self.gs.paddle_2.score)
		}

		bricks = set()
		for brick in self.gs.bricks:
			bricks.add((brick.rect.center, brick.z_pos, brick.color))
		objects['bricks'] = bricks

		balls = set()
		for ball in self.gs.balls:
			balls.add((ball.rect.center, ball.z_pos, ball.color))
		objects['balls'] = balls

		pickled_objects = pickle.dumps(objects)
		self.transport.write(pickled_objects)

	def connectionLost(self, reason):
		print 'Connection lost:', reason
		sys.exit

class Host_Factory(ServerFactory):
	def buildProtocol(self, addr):
		return Host_Protocol()

reactor.listenTCP(9313, Host_Factory())
reactor.run()
