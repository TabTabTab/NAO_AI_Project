from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

import MotionMaestro

class SonarRModule(ALModule):
  """ Mandatory docstring.
      comment needed to create a new python module
  """
  def sonarHandler(self, key, value, message):
    """ Mandatory docstring.
        comment needed to create a bound method
    """
    memory.unsubscribeToEvent("SonarLeftNothingDetected","SonarR")
    print "sonar?"
    print key
    print value
    print message
    self.tts.say("something at my right,nothing else")
    if (value<0.8):
      print "turning left"
      MotionMaestro.turnLeftRad(motionProxy,0.2)
      print "turned left"

    memory.subscribeToEvent("SonarLeftNothingDetected","SonarR","sonarHandler")

  	

  def __init__(self, name,postureProxy,motionProxy):
    ALModule.__init__(self, name)
    self.tts = ALProxy("ALTextToSpeech")
    self.postureProxy=postureProxy
    self.motionProxy=motionProxy
    global memory
    memory = ALProxy("ALMemory")
    memory.subscribeToEvent("SonarLeftNothingDetected","SonarR","sonarHandler")