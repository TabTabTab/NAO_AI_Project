from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "127.0.0.1", 52864)
tts.say("Party Party Baby!")