import time
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

global lastLeftTurn=0.2
global lastRightTurn=0.2


global timeTLeft
global timeTRight
timeTLeft=0
timeTRight=0
# we want to walk close to the right wall, between 0.5 and 1.0 m
# still, we handle close to left in order to not crash
# this method does not yet handle frontal coalissions
def handleData(leftDist,rightDist,motionMaestro):
	if(leftDist<leftMin and rightDist<rightMin):
		print "we are in a pickle"
		motionMaestro.stopWalking()
	elif(rightDist<rightMin):
		print "close to right, turning left"
		motionMaestro.moveLeft()
		time.sleep(1.0)

		now=time.time()
		delT=timeTRight-now
		rad=getTurnRad(delT)
		timeTLeft=now
		
		motionMaestro.turnLeftRad(rad)

	elif(leftDist<leftMin):
		print "close to left, turning right"
		motionMaestro.moveRight()
		time.sleep(1.0)

		now=time.time()
		delT=timeTLight-now
		rad=getTurnRad(delT)
		motionMaestro.turnRightRad(rad)
		timeTRight=now
	
	elif(rightDist>rightMax):
		print "too far from right, turning right"
		motionMaestro.moveRight()
		time.sleep(1.0)

		now=time.time()
		delT=timeTLight-now
		rad=getTurnRad(delT)
		motionMaestro.turnRightRad(rad)
		timeTRight=now
	else:
		print "far from walls"
		motionMaestro.continueStraight()



def getTurnRad(delT):
	rad=1.57*(1/(2.0**delT))
	print "you should turn this much ",rad
	return rad

def main():

	timeTLeft=time.now()
	timeTRight=time.now()
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
	for i in xrange(0,40):
		 leftDist=memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
		 rightDist=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
		 rightFrontDist=memoryProxy.getData("SonarRightDetected");
		 print leftDist,rightDist
		 handleData(leftDist,rightDist,motionMaestro)
		 time.sleep(1.0)

	print "finished walking"
	motionMaestro.stopWalking()


	




if __name__ == "__main__":
    main()
