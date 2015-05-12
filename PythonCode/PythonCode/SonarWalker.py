import time
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from SonarLModule import SonarLModule 


from MotionMaestro import MotionMaestro
import RegisterMaestro


IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559

v=v1=v2=v3=v4=v5=v6=v7=v8=v9=0
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

	memoryProxy=RegisterMaestro.registerMemoryProxy()

	#global SonarL
	#SonarL = SonarLModule("SonarL")

	

	motionMaestro.startWalking()
	print "start walking test"
	for i in xrange(0,5):
		#printRVals(memoryProxy)
		v=v1=v2=v3=v4=v5=v6=v7=v8=v9=0.0
		
		samp=20
		samps=samp+0.0
		for i in xrange(0,samp):
			v=v+memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
			v1=v1+ memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value1")
			v2=v2+ memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value2")
			v3=v3+memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value3")
			v4=v4+ memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value4")
			v5=v5+memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value5")
			v6=v6+memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value6")
			v7=v7+memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value7")
			v8=v8+ memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value8")
			v9=v9+memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value9")
		
		v=v/samps
		v1=v1/samps
		v2=v2/samps
		v3=v3/samps
		v4=v4/samps
		v5=v5/samps
		v6=v6/samps
		v7=v7/samps
		v8=v8/samps
		v9=v9/samps
		printVals(v,v1,v2,v3,v4,v5,v6,v7,v8,v9)


	
	print "finished walking"
	motionMaestro.stopWalking()

def printVals(v,v1,v2,v3,v4,v5,v6,v7,v8,v9):
	print "\n====vals in order ===="
	print v
	print v1
	print v2
	print v3
	print v4
	print v5
	print v6
	print v7
	print v8
	print v9

def printRVals(memoryProxy):
	print "\n====vals in order ===="
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value1")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value2")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value3")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value4")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value5")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value6")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value7")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value8")
	print memoryProxy.getData("Device/SubDeviceList/US/Right/Sensor/Value9")
	




if __name__ == "__main__":
    main()
