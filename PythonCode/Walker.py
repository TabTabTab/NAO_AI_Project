import time
from naoqi import ALProxy

IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559



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

def main():
	postureProxy=registerPostureProxy()
	motionProxy=registerMotionProxy()
	startWalking(postureProxy,motionProxy)
	time.sleep(10.0)
	stopWalking(motionProxy)




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