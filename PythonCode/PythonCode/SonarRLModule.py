from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from MotionMaestro import MotionMaestro

class SonarRLModule(ALModule):
  """ Mandatory docstring.
      comment needed to create a new python module
  """
  def sonarLeftHandler(self, key, value, message):
    """ Mandatory docstring.
        comment needed to create a bound method
    """
    memory.unsubscribeToEvent("SonarLeftDetected",self.name)
    print "sonar left front event"
    print key
    print value
    print message
    self.tts.say("something at my left front")
    print "Now I am turning right"
    self.motionMaestro.turnRightRad(0.5)
    memory.subscribeToEvent("SonarLeftDetected",self.name,"sonarLeftHandler")


  def sonarRightHandler(self, key, value, message):
    """ Mandatory docstring.
        comment needed to create a bound method
    """
    memory.unsubscribeToEvent("SonarRightDetected",self.name)
    print "sonar right front event"
    print key
    print value
    print message
    self.tts.say("something at my right front")
    print "Now I am turning left"
    self.motionMaestro.turnLeftRad(0.5)
    memory.subscribeToEvent("SonarRightDetected",self.name,"sonarRightHandler")

  	

  def __init__(self, name,motionMaestro):
    ALModule.__init__(self, name)
    self.motionMaestro=motionMaestro
    self.name=name
    self.tts = ALProxy("ALTextToSpeech")
    global memory
    memory = ALProxy("ALMemory")
    memory.subscribeToEvent("SonarLeftDetected",name,"sonarLeftHandler")
    memory.subscribeToEvent("SonarRightDetected",name,"sonarRightHandler")