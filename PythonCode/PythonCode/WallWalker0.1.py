import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import almath as m
import math
from SonarRLModule import SonarRLModule 


from MotionMaestro import MotionMaestro
import RegisterMaestro


IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559

IP2="127.0.0.1"
PORT2=39327


#IP=IP2
#PORT=PORT2


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


	#global SonarRL
	#SonarRL = SonarRLModule("SonarRL",motionMaestro)


	robotPositionBeforeCommand  = m.Pose2D(motionProxy.getRobotPosition(False))
	motionMaestro.startWalking()
	print "start walking test"
	print "before:"
	print robotPositionBeforeCommand
	time.sleep(2)
	robotPositionAfterCommand = m.Pose2D(motionProxy.getRobotPosition(False))
	print "\nafter:"
	print robotPositionAfterCommand



	print "disance walked:"
	dx=robotPositionBeforeCommand.x-robotPositionAfterCommand.x
	dy=robotPositionBeforeCommand.y-robotPositionAfterCommand.y
	dist=math.sqrt(dx**2+dy**2)
	print "dx: ",dx
	print "dy: ",dy
	print "dist: ",dist

	print "finished walking"
	motionMaestro.stopWalking()


	




if __name__ == "__main__":
    main()
