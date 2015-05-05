from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "192.168.0.101", 9559)
tts.say("Party Party Baby!")