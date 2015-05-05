import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule


IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559




def stopWalking(motionProxy):
    X = 0.0
    Y = 0.0
    Theta = 0.0
    Frequency =1.0
    motionProxy.setWalkTargetVelocity(X, Y, Theta, Frequency)


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



def main():
		stopWalking(registerMotionProxy())


if __name__ == "__main__":
    main()