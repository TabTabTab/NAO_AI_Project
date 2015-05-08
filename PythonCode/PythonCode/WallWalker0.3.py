import time
import math

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule



from SonarRLModule import SonarRLModule 


from MotionMaestro import MotionMaestro
import RegisterMaestro


IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559

IP2="127.0.0.1"
PORT2=39327


#IP=IP2
#PORT=PORT2

global leftMin
leftMin=0.5

global rightMin
rightMin=0.5

global rightMax
rightMax=1.0

global radDecFactor
radDecFactor=0.7

global lastLeftTurn
lastLeftTurn=0.2
global lastRightTurn
lastRightTurn=0.2


global timeTLeft
global timeTRight
timeTLeft=0
timeTRight=0
# we want to walk close to the right wall, between 0.5 and 1.0 m
# still, we handle close to left in order to not crash
# this method does not yet handle frontal coalissions

def main():

	timeTLeft=time.time()
	timeTRight=time.time()
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
	myBroker = ALBroker("myBroker","0.0.0.0",0,IP,PORT)

	       
	#now we try sonar
	sonarProxy=RegisterMaestro.registerSonarProxy()
	memoryProxy=RegisterMaestro.registerMemoryProxy()

	sonarProxy.subscribe("myApplication")

	postureProxy=RegisterMaestro.registerPostureProxy()

	motionProxy=RegisterMaestro.registerMotionProxy()

	motionMaestro = MotionMaestro(postureProxy,motionProxy)


	#global SonarRL
	#SonarRL = SonarRLModule("SonarRL",motionMaestro)

	"""
	motionMaestro.moveLeft()
	time.sleep(4)
	motionMaestro.stopWalking()
	return 
	"""

	motionMaestro.startWalking()
	print "start walking test"

	optRDist=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
	lastRight=optRDist
	print lastRight
	deltaR=0
	valPer3sec=0.2
	wiggleRoom=0.5
	maxRDist=optRDist+wiggleRoom
	minRDist=optRDist-wiggleRoom
	distLastWalked=0.0
	actionTreshold=0.1

	for i in xrange(0,5):
		time.sleep(3.0)
		distLastWalked=distLastWalked+valPer3sec
		rightDist=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
		print "rdist c1: ",rightDist

		deltaR=rightDist-lastRight
		

		if(math.fabs(deltaR)>distLastWalked):
			print "failure due to large values in deltaR"
			printEm(deltaR,lastRight,rightDist,distLastWalked,actionTreshold,"no theta","oob")
			continue
		theta=math.asin(deltaR/(distLastWalked))
		if(math.fabs(deltaR)<actionTreshold):
			printEm(deltaR,lastRight,rightDist,distLastWalked,actionTreshold,theta,"skipping")
			continue

		
		

		theta=math.asin(deltaR/(distLastWalked))
		printEm(deltaR,lastRight,rightDist,distLastWalked,actionTreshold,theta,"turning")
		
		lastRight=rightDist
		
		distLastWalked=0.0
		motionMaestro.turnRad(theta)
		motionMaestro.startWalking()
		

	print "finished walking"
	motionMaestro.stopWalking()


	

def printEm(deltaR,lastRight,rightDist,distLastWalked,actionTreshold,theta,msg):
	print "\n======status========"
	print "deltaR: ",deltaR
	print "lastRight ",lastRight
	print "rightDist ",rightDist
	print "distLastWalked ",distLastWalked
	print "actionTreshold ",actionTreshold
	print "theta ",theta
	print "msg: ",msg
	print "============="




if __name__ == "__main__":
    main()
