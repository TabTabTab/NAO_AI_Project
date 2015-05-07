import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from SonarRModule import SonarRModule 
from SonarRFModule import SonarRFModule

import MotionMaestro
import RegisterMaestro


IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559


def main():


    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
	myBroker = ALBroker("myBroker","0.0.0.0",0,IP,PORT)

	       
	#now we try sonar
	sonarProxy=RegisterMaestro.registerSonarProxy()

	sonarProxy.subscribe("myApplication")

	postureProxy=RegisterMaestro.registerPostureProxy()

	motionProxy=RegisterMaestro.registerMotionProxy()

	global SonarRF
	SonarRF = SonarRFModule("SonarRF")

	global SonarR
	SonarR = SonarRModule("SonarR")

	#MotionMaestro.startWalking(postureProxy,motionProxy)
	#time.sleep(3)
	print "turning test"
	MotionMaestro.turnRight3(motionProxy)
	print "finished turning"
	time.sleep(5)
	#for i in xrange(0,2):
	#	time.sleep(1.0)
	MotionMaestro.stopWalking(motionProxy)


	




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