import os
import sys

import EtFile
import UserAnalyzer

# Generates list of users from the passed session data
def getUsers(sessionData):
	uniqueUsers = []
	
	# User strings for general website folder accesses
	artificialUsers = ['activity', 'promo', 'guide', 'wps', 'frame', 'event', 'share', 'monitor', 'drop', 'csp', 'reference', 'win']

	for session in sessionData:
		if session[1] not in uniqueUsers and session[1] not in artificialUsers:
			uniqueUsers.append(session[1])

	return uniqueUsers
	
# ~~~~~~	DETERMINE FOR DEPRECATION	
def writeUsersToFile(sessionData):
	userList = getUsers(sessionData)

	textFile = open('userReadable.txt', 'w')
	
	for user in userList:
		textFile.write(user)
		textFile.write("\n")
		
	textFile.close()

# Returns session data that belongs to the passed user	
def getUserData(sessionData, user):
	data = []

	for session in sessionData:
	# Sessions are separated by logged IPs, there can be multiple sessions for the same user
	#	session[1]	-	user string
		if user == session[1]:
			data.append(session)

	return data
	
# Filters user code log data from a user session
def getUserCode(userData):

	#	codeEntries	:=	[entryIndex][entryMode, entryTimestamp, entryCode]
	codeEntries = []
	blocks = dict()
	
#	IP	-	IP-specific data for user	
	for IP in userData:
		for row in range(0, len(IP[2])):
			
			if IP[2][row][1].find("/log/") != -1:
				entryTimestamp = IP[2][row][0]
				entryData = IP[2][row][3]
				## TODO: might want to group by project names with project = IP[2][row][1].split('/log')[1]
				if "code" in entryData:
					# .split('|') formats the code string to a list of code line strings
					codeEntries.append( [entryData['mode'][0], entryTimestamp, entryData['code'][0].split('|') ] )
				elif "id" in entryData:
					blockKey = entryData['id'][0]
					
					if blocks.has_key(blockKey):
						blocks[blockKey] += 1
					else:
						blocks[blockKey] = 1
						
	return codeEntries, blocks

# ~~~~~~~TBD FOR DEPRECATION
# TODO: find out what is useful from entry to append	
# Filters user load log data from a user session
def getUserLoad(userData):

	for entry in userData:
		if entry[2][0][1].find("/load/") != -1:
			data.append(entry)
			#data.append(entry[2][0][3]['code'][0])
				
	return data
	
# Gets list of IPs for user	data
def getUserIP(userData):
	ipList = []
	
	for entry in userData:
		ipList.append(entry[0])
			
	return ipList
	
# WIP	
# Joins user data by IP address	
def joinUserByIP(userData, anonymousData):
	
	joinedData = userData
	userIP = getUserIP(userData)
	userName = userData[0][0]
	
	for entry in anonymousData:
		if entry[0] in userIP:
			joinedData.append([ entry[0], userName, entry[2] ])
			
	return joinedData		

#	* TO DO * IMPORTANT *
def writeUserDataFile(sessionData, user):
	
	userData = getUserData(sessionData, user)
	userCode, blockData = getUserCode(userData)
	
	if userCode and userCode[0]:
		print "Writing " + user + " analysis"
		test = UserAnalyzer.analyzeUser(user, userCode, blockData)
		return 1
	return 0
	
def writeDataFile(sessionData):
	
	print "Generating unique users..."
	userList = getUsers(sessionData)
	filesWritten = 0
	
	for user in userList:
		filesWritten += writeUserDataFile(sessionData, user)
	
	print("{} users logged".format(filesWritten))
	
def main():
	print "Loading session data..."
	sessionData = EtFile.loadJsonFile('sessions.json')

	print "Generating user code files..."
	writeDataFile(sessionData)

if __name__ == "__main__":
	main()
