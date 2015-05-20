#!/usr/bin/python

import lineFinder



def runLineRobot():
	lineRunner=lineFinder.LineFinder()
	lineRunner.onLoad()
	lineRunner.onInput_onStart()



def run():
	stop="0"
	proceed="1"
	command=proceed
	while(command!=stop):
		command=raw_input("enter a command; 0 - to stop: ");
		print "got command: '",command,"'"
	print "stopping"


runLineRobot()