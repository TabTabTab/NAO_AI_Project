import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule


IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559



# create python module
class SonarModule(ALModule):
  """ Mandatory docstring.
      comment needed to create a new python module
  """
  def sonarHandler(self, key, value, message):
    """ Mandatory docstring.
        comment needed to create a bound method
    """
    unsubscribeEvents()
    print "sonar?"
    print key
    print value
    print message
    self.tts.say("something at my right")
    subscribeToEvents()

  def unsubscribeEvents():
  	memory.unsubscribeToEvent("SonarRightDetected",
            "SonarModule")
  	memory.unsubscribeToEvent("SonarLeftDetected","SonarModule")
  def subscribeToEvents():
  	memory.subscribeToEvent("SonarLeftDetected",
            "SonarModule",
            "sonarHandler")
  	memory.subscribeToEvent("SonarRightDetected",
            "SonarModule",
            "sonarHandler")
  def __init__(self, name):
  	ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
	self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the FaceDetected event:
	global memory
	memory = ALProxy("ALMemory")
	memory.subscribeToEvent("SonarLeftDetected",
            "SonarModule",
            "sonarHandler")
  	memory.subscribeToEvent("SonarRightDetected",
            "SonarModule",
            "sonarHandler")
	print "now I surely am subscribed"


# create python module
class BumpModule(ALModule):
  """ Mandatory docstring.
      comment needed to create a new python module
  """
  def bumpHandler(self, key, value, message):
    """ Mandatory docstring.
        comment needed to create a bound method
    """
    print "bump?"
    print key
    print value
    print message


  def __init__(self, name):
  	ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
	self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the FaceDetected event:
	global memory
	memory = ALProxy("ALMemory")
	memory.subscribeToEvent("FaceDetected",
            "BumpModule",
            "bumpHandler")

    



def registerPostureProxy():
	postureProxy=False
	#connect to posture
	try:
		postureProxy = ALProxy("ALRobotPosture", IP, PORT)
		return postureProxy
	except Exception, e:
		print "Could not create proxy to ALRobotPosture"
    	print "Error was: ", e
    	postureProxy=False
    	return postureProxy

def registerMotionProxy():
	motionProxy=False
	#connect to posture
	try:
		motionProxy = ALProxy("ALMotion", IP, PORT)
		return motionProxy
	except Exception, e:
		print "Could not create proxy to ALMotion"
    	print "Error was: ", e
    	motionProxy=False
    	return motionProxy

def registerMemoryProxy():
	memoryProxy=False
	#connect to posture
	try:
		memoryProxy = ALProxy("ALMemory", IP, PORT)
		return memoryProxy
	except Exception, e:
		print "Could not create proxy to ALMemory"
    	print "Error was: ", e
    	memoryProxy=False
    	return memoryProxy


def registerSonarProxy():
	sonarProxy=False
	#connect to posture
	try:
		sonarProxy = ALProxy("ALSonar", IP, PORT)
		return sonarProxy
	except Exception, e:
		print "Could not create proxy to ALSonar"
    	print "Error was: ", e
    	sonarProxy=False
    	return sonarProxy


def standUp(postureProxy):
	print "Standing Up"
	postureProxy.goToPosture("Stand", 1.0)

def sitDown(postureProxy):
	print "Sitting Down"
	postureProxy.goToPosture("Sit", 1.0)

def startWalking(postureProxy,motionProxy):
	stiffnessOn(motionProxy)
	postureProxy.goToPosture("StandInit", 0.5)
	motionProxy.setWalkArmsEnabled(True, True)
	motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
	X = 0.5  
	Y = 0.0
	Theta = 0.0
	Frequency =0.0 # low speed
	motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def turnRight(postureProxy,motionProxy):
	stiffnessOn(motionProxy)
	postureProxy.goToPosture("StandInit", 0.5)
	motionProxy.setWalkArmsEnabled(True, True)
	X = 0.0  
	Y = 0.5
	Theta = 0.0
	Frequency =0.0 # low speed
	motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)




def footFeed(memoryProxy):
	leftBumper = memoryProxy.getData('LeftBumperPressed')
	rightBumper = memoryProxy.getData('RightBumperPressed')
	return leftBumper or rightBumper

def stopWalking(motionProxy):
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency =1.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)

def stiffnessOn(motionProxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)



def printWallStatus(memoryProxy):
	leftVal=getLeftSonarValue(memoryProxy)
	rightVal=getRightSonarValue(memoryProxy)
	if(leftVal<rightVal):
		print "turn right ", leftVal-rightVal
	else:
		print "turn left ", leftVal-rightVal


def printSonarValues(memoryProxy):
	printLeftSonarValues(memoryProxy)
	#leftData=memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")
	#rightData=memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
	#print "leftdata",leftData
	#print "rightdata",rightData
def getLeftSonarValue(memoryProxy):
	return memoryProxy.getData("Device/SubDeviceList/US/Left/Sensor/Value")

def getRightSonarValue(memoryProxy):
	return memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")

def printLeftSonarValues(memoryProxy):
	vals =[
	"Device/SubDeviceList/US/Left/Sensor/Value",
	"Device/SubDeviceList/US/Left/Sensor/Value1",
	"Device/SubDeviceList/US/Left/Sensor/Value2",
	"Device/SubDeviceList/US/Left/Sensor/Value3",
	"Device/SubDeviceList/US/Left/Sensor/Value4",
	"Device/SubDeviceList/US/Left/Sensor/Value5",
	"Device/SubDeviceList/US/Left/Sensor/Value6",
	"Device/SubDeviceList/US/Left/Sensor/Value7",
	"Device/SubDeviceList/US/Left/Sensor/Value8",
	"Device/SubDeviceList/US/Left/Sensor/Value9"
	]
	#print vals[0],memoryProxy.getData(vals[0]) 
	#printWallStatus(memoryProxy)
	for s in vals:
		print s,memoryProxy.getData(s) 
	#print "\n"
	

def main():

	pip=IP
	pport=PORT


    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
	myBroker = ALBroker("myBroker","0.0.0.0",0,pip,pport)

	       
	#now we try sonar
	sonarProxy=registerSonarProxy()

	sonarProxy.subscribe("myApplication")
	memoryProxy=registerMemoryProxy()
	postureProxy=registerPostureProxy()
	standUp(postureProxy)
	motionProxy=registerMotionProxy()
	startWalking(postureProxy,motionProxy)

	global SonarModule
	SonarModule = SonarModule("SonarModule")


	for i in xrange(0,10):
		time.sleep(1.0)
	stopWalking(motionProxy)

	# demo for reporting sonars
	# printLeftSonarValues(memoryProxy)


	#for i in xrange(0,10):
	#	time.sleep(1.0)


	#now we end sonar

	#global SonarModule
	#SonarModule = SonarModule("SonarModule")
	#global BumpModule
	#BumpModule = BumpModule("BumpModule")

	#for i in xrange(0,10):
	#	time.sleep(1.0)
	#	bumped=footFeed(memoryProxy)
	#	print bumped


	return


	postureProxy=registerPostureProxy()
	sitDown(postureProxy)
	motionProxy=registerMotionProxy()
	startWalking(postureProxy,motionProxy)
	time.sleep(5.0)
	#turnRight(postureProxy,motionProxy)
	#time.sleep(2.0)
	#startWalking(postureProxy,motionProxy)
	#time.sleep(5.0)
	stopWalking(motionProxy)
	turnRight(postureProxy,motionProxy)
	time.sleep(2.0)
	stopWalking(motionProxy)
	sitDown(postureProxy)



if __name__ == "__main__":
    main()

#postureProxy.goToPosture("StandInit", 1.0)
#postureProxy.goToPosture("SitRelax", 1.0)
#postureProxy.goToPosture("StandZero", 1.0)
#postureProxy.goToPosture("LyingBelly", 1.0)
#postureProxy.goToPosture("LyingBack", 1.0)
#postureProxy.goToPosture("Stand", 1.0)
#postureProxy.goToPosture("Crouch", 1.0)
#postureProxy.goToPosture("Sit", 1.0)