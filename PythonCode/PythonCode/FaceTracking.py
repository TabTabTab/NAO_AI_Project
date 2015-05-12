
from naoqi import ALProxy
import time
import sys
from MotionMaestro import MotionMaestro
import RegisterMaestro


from naoqi import ALBroker
from naoqi import ALModule
IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559




def set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled):
    """Make a proxy to nao's ALFaceDetection and enable/disable tracking.

    """
    faceProxy = ALProxy("ALFaceDetection", nao_ip, nao_port)

    print "Will set tracking to '%s' on the robot ..." % tracking_enabled

    # Enable or disable tracking.
    faceProxy.enableTracking(tracking_enabled)

    # Just to make sure correct option is set.
    print "Is tracking now enabled on the robot?", faceProxy.isTrackingEnabled()


def main():
    # Specify your IP address here.
    nao_ip = IP
    nao_port = PORT
    myBroker = ALBroker("myBroker","0.0.0.0",0,IP,PORT)
    tracking_enabled = True
    set_nao_face_detection_tracking(nao_ip, nao_port, tracking_enabled)
    postureProxy=RegisterMaestro.registerPostureProxy()
    motionProxy=RegisterMaestro.registerMotionProxy()
    motionMaestro = MotionMaestro(postureProxy,motionProxy)
    motionMaestro.standUp()

    faceProxy = ALProxy("ALFaceDetection", IP, PORT)

    faceVal=faceProxy.learnFace("Folke")
    print "this is the f-result"
    print faceVal
    return 
    for i in xrange(0,10):
        print "still active"
        time.sleep(10)


if __name__ == "__main__":
    main()