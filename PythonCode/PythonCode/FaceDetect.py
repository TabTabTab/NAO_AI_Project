# -*- encoding: UTF-8 -*- 
# This test demonstrates how to use the ALFaceDetection module.
# Note that you might not have this module depending on your distribution
#
# - We first instantiate a proxy to the ALFaceDetection module
#     Note that this module should be loaded on the robot's naoqi.
#     The module output its results in ALMemory in a variable
#     called "FaceDetected"

# - We then read this ALMemory value and check whether we get
#   interesting things.

import time

from naoqi import ALProxy

IP = "192.168.0.101"  # Replace here with your NaoQi's IP address.
PORT = 9559
foundLastCheck=False
# Create a proxy to ALFaceDetection
try:
  faceProxy = ALProxy("ALFaceDetection", IP, PORT)
except Exception, e:
  print "Error when creating face detection proxy:"
  print str(e)
  exit(1)

#connect to posture
try:
    postureProxy = ALProxy("ALRobotPosture", IP, PORT)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e
    exit(1)

#connect to speech
try:
    ttsProxy = ALProxy("ALTextToSpeech", IP, PORT)
except Exception, e:
  print "Could not create proxy to ALTextToSpeech"
  print "Error was: ", e
  exit(1)

# Subscribe to the ALFaceDetection proxy
# This means that the module will write in ALMemory with
# the given period below
period = 500
faceProxy.subscribe("Test_Face", period, 0.0 )

# ALMemory variable where the ALFacedetection modules
# outputs its results
memValue = "FaceDetected"

# Create a proxy to ALMemory
try:
  memoryProxy = ALProxy("ALMemory", IP, PORT)
except Exception, e:
  print "Error when creating memory proxy:"
  print str(e)
  exit(1)



#postureProxy.goToPosture("StandInit", 1.0)
#postureProxy.goToPosture("SitRelax", 1.0)
#postureProxy.goToPosture("StandZero", 1.0)
#postureProxy.goToPosture("LyingBelly", 1.0)
#postureProxy.goToPosture("LyingBack", 1.0)
#postureProxy.goToPosture("Stand", 1.0)
#postureProxy.goToPosture("Crouch", 1.0)
#postureProxy.goToPosture("Sit", 1.0)

# A simple loop that reads the memValue and checks whether faces are detected.
for i in range(0, 4):
  time.sleep(0.8)
  val = memoryProxy.getData(memValue)

  print ""
  print "*****"
  print ""

  # Check whether we got a valid output.
  if(val and isinstance(val, list) and len(val) >= 2):

    # We detected faces !
    # For each face, we can read its shape info and ID.

    # First Field = TimeStamp.
    timeStamp = val[0]

    # Second Field = array of face_Info's.
    faceInfoArray = val[1]

    try:
      # Browse the faceInfoArray to get info on each detected face.
      for j in range( len(faceInfoArray)-1 ):
        faceInfo = faceInfoArray[j]

        # First Field = Shape info.
        faceShapeInfo = faceInfo[0]

        # Second Field = Extra info (empty for now).
        faceExtraInfo = faceInfo[1]

        print "  alpha %.3f - beta %.3f" % (faceShapeInfo[1], faceShapeInfo[2])
        print "  width %.3f - height %.3f" % (faceShapeInfo[3], faceShapeInfo[4])
        postureProxy.goToPosture("Sit", 1.0)
        if(foundLastCheck):
            ttsProxy.say("I still see you!")
        else:
            ttsProxy.say("I see you!")
            foundLastCheck=True


    except Exception, e:
      print "faces detected, but it seems getData is invalid. ALValue ="
      print val
      print "Error msg %s" % (str(e))
  else:
    print "No face detected"
    foundLastCheck=False
    postureProxy.goToPosture("SitRelax", 1.0)
    ttsProxy.say("I found nothing")

#postureProxy.goToPosture("Sit", 1.0)
postureProxy.goToPosture("SitRelax", 1.0)
# Unsubscribe the module.
faceProxy.unsubscribe("Test_Face")

print "Test terminated successfully."
