from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

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
    memory.subscribeToEvent("SonarLeftNothingDetected","SonarR","sonarHandler")

  	

  def __init__(self, name):
  	ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
	self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the FaceDetected event:
	global memory
	memory = ALProxy("ALMemory")
	memory.subscribeToEvent("SonarLeftNothingDetected","SonarR","sonarHandler")