import os
import sys
import difflib


def safe_str(obj):
    ##return the byte string representation of obj
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')

# Returns difference strings 	
def codeDifference(previousCode, currentCode):
	
	differences = []
	
	# Creates the list of line differences with line location
	for lineNumber, line in enumerate(difflib.ndiff(previousCode, currentCode)):
		differences.append( (str(lineNumber + 1)) + "\t" + line ) ##safe_str("{}\t{}".format(lineNumber + 1, line))
	
	return differences

## TODO: seems to be difficult to construct a comprehensive solution, might have to stick with simple-enough block types
# def blockCountFromCode(userCode):
	# userBlocks = dict()
	# previousTime = userCode[0][1]
	# previousCode = userCode[0][2]
	
	## TODO: read from BlockIDs.txt to initialize dictionary keys
	## TODO: remove block counting from SessionParser, do it all in here
	
	# for entry in userCode:
		# currentTime = entry[1]
		# timeElapsed = currentTime - previousTime
		# previousTime = currentTime
		
		# if timeElapsed != 0:
			# difference = codeDifference(previousCode, entry[2])
			
			# for line in difference:
				# blockKey = line[2:].split(' ')[1]
				# what about comments? ex. '#turn the right way'
				#		currently grouping 
				# if line[0] == '+':
					# if userBlocks.has_key(blockKey):
						# userBlocks[blockKey] += 1
					# else:
						# userBlocks[blockKey] = 1
				# elif line[0] == ' ':
						
def analyzeUser(user, userCode, userBlocks):
	
	userFile = open("User_" + user + ".txt", "w")
	
	userFile.write("Analysis data for:\t" + user + "\n\n")
	userFile.write("Block counts\n")
	
	for block in userBlocks:
		userFile.write("\t{}:\t{}\n".format(block, userBlocks[block]))
	
	userFile.write("\nCode Analysis\n")
	
	
# Session elapsed time variables
	#	(int) time elapsed between code saves	
	timeElapsed = 0
	#	(int) time elapsed while in block mode
	blockElapsed = 0
	#	(int) time elapsed while in text mode
	textElapsed = 0
	#	(list) mode,duration event-pairs during session
	#		pairs are structured as [ mode(string) , duration(int)]
	modeEvents = []
	#	mode start time
	startMode = 0

	totalElapsed = 0	
	modeChanges = 0
	sessionNumber = 1
	
	# First-case initializations
	previousMode = userCode[0][0]
	previousTime = userCode[0][1]
	previousCode = userCode[0][2]
	
	userFile.write("\n~~~~~~~~~~~~~~~~~ Session 1 ~~~~~~~~~~~~~~~~~")
	
	for entry in userCode:
		currentMode = entry[0]
		currentTime = entry[1]
		
		# If mode has not changed, stays null-string
		#	else, change string to mode that the user has changed to
		hasModeChanged = ''
		
		if currentMode != previousMode:
			modeChanges += 1
			previousMode = currentMode
			hasModeChanged = currentMode
		
		## BUGFIX: noticed that if there is no previous code in the session before differences, time elapsed comes out negative
		##		BANDAID: taking absolute difference
		timeElapsed = abs(currentTime - previousTime)
		previousTime = currentTime
		
		if timeElapsed != 0:
			# Sessions are separated by hour-long timestamp differences
			if timeElapsed > 3600:
				userFile.write("\n***************** Session Summary *****************")
				
				for pair in modeEvents:
					userFile.write( pair[0] + "({}) ".format(pair[1]) )
				
				userFile.write("\nTotal session time: {} seconds".format(totalElapsed))
				userFile.write("\nBlock mode time: {} seconds".format(blockElapsed))
				userFile.write("\nText mode time: {} seconds".format(textElapsed))
				sessionNumber += 1
				userFile.write("\n\n~~~~~~~~~~~~~~~~~ Session {} ~~~~~~~~~~~~~~~~~".format(sessionNumber))
				#	Reset elapsed time variables for previous session
				blockElapsed = 0
				textElapsed = 0
				totalElapsed = 0
				
			totalElapsed += timeElapsed
			# If mode has changed, attribute elapsed time to previous mode
			if hasModeChanged == 'b':
				modeEvents.append( ['t' , totalElapsed - startMode] )
				textElapsed += timeElapsed
				startMode = totalElapsed
			elif hasModeChanged == 't':
				modeEvents.append( ['b' , totalElapsed - startMode] )
				blockElapsed += timeElapsed
				startMode = totalElapsed5
			# Else, attribute elapsed time to current mode
			elif currentMode == 'b':
				blockElapsed += timeElapsed
			elif currentMode == 't':
				textElapsed += timeElapsed
			
			difference = codeDifference(previousCode, entry[2])
			##TODO: change to have differences adjacent to previous(current) code: maybe just change \n to \t (and some change)
			userFile.write("\nDifferences from previous code")
			userFile.write("\n\n\tTime between changes: " + str(secondsToTime(timeElapsed)))
			
			for line in difference:
				## TODO: need a better fix than unicode().encode('utf-8')
				userFile.write("\n\t" + unicode(line).encode('utf-8'))
			
			previousCode = entry[2]
			
			userFile.write("\n\n~~~~~~~~~~~~~~~~~ ")
			userFile.write("Code from " + str(secondsToTime(previousTime)) + "\tMode: " + previousMode)
			userFile.write(" ~~~~~~~~~~~~~~~~~")
			
			for line in previousCode:
				## TODO: need a better fix than unicode().encode('utf-8')
				userFile.write("\n" + unicode(line).encode('utf-8'))
			
	userFile.write("\n\n***************** Session Summary *****************")
	
		for pair in modeEvents:
			userFile.write( pair[0] + "({}) ".format(pair[1]) )
				
	userFile.write("\nTotal session time: {} seconds".format(totalElapsed))
	userFile.write("\nBlock mode time: {} seconds".format(blockElapsed))
	userFile.write("\nText mode time: {} seconds".format(textElapsed))
	
	userFile.write("\n\nTotal mode changes: " + str(modeChanges))
	userFile.write("\nTotal sessions: " + str(sessionNumber))
	
	userFile.close()
	
# Converts TIME_IN_MS timestamp from a log entry to a HH:MM:SS representation
def secondsToTime(timestamp):
	
	seconds = timestamp % 60
	remainder = timestamp / 60
	
	minutes = remainder % 60
	remainder = remainder / 60

	hours = remainder % 24
	time = "{}:{}:{}".format(hours, minutes, seconds)
	
	return time