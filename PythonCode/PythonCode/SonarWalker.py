import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from SonarLModule import SonarLModule 


from MotionMaestro import MotionMaestro
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

	motionMaestro = MotionMaestro(postureProxy,motionProxy)


	global SonarL
	SonarL = SonarLModule("SonarL")


	motionMaestro.startWalking()
	print "start walking test"
	time.sleep(5)
	print "finished walking"
	motionMaestro.stopWalking()


	




if __name__ == "__main__":
    main()
