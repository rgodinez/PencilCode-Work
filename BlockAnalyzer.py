import os
import sys
import argparse

import EtFile

global isDebugging

def parseArguments():
    dataPath = None
    isDebugging = False
    
    # handle command line args
    parser = argparse.ArgumentParser(description='A program to build a CSV file from Pencil Code log files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_help = True
    parser.add_argument('path', help='path of a pickled log file from formatter (required)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='display debug information')
    args = parser.parse_args()
    if args.debug:  isDebugging = True
    if args.path: dataPath = args.path

    # Path required as parameter
    if not dataPath:
        print "Error: no path specified!"
        sys.exit(2)

    # debug program
    if isDebugging:
        print "SYSTEM"
        print sys.version
        print

    if not os.path.isfile(dataPath):
        print "Error: invalid path specified!"
        sys.exit(2)

    return dataPath

# Outgoing data format:
#   Per session:

def countSessionSet(sessions, context):
    totalData = 0
    sessionData = []
    typeData = dict()
	
    # For each session, count up the number of each general type.
    for session in sessions:
        sessionCount = 0
        typeCount = dict()
        # Check each log entry in the session; if the user selected a block and the log is valid, count it.
        for entry in session[1]:
            if entry[1] == "/log/~pickblock":
                try:
                    blockType = entry[3]["id"][0]

                    if blockType in typeCount.keys():
                        typeCount[blockType] += 1
                    else:
                        typeCount[blockType] = 1

                except KeyError:
                    print "No id entry: " + context + "/" + session[0] + "," + str(entry[0]) + " : " + entry[2]
                    
        # Once every log entry has been examined, count the total blocks and calculate percentages.
        for count in typeCount.values():
            sessionCount += count
            
        for blockType, count in typeCount.items():
            typeCount[blockType] = [count, float(count) / sessionCount]
            
        sessionData.append([sessionCount, typeCount])
        
    for counts in sessionData:
        totalData += 1 # Ricardo: changed from += counts[0] because this would always be 0
		
        for blockType, blockCount in counts[1].items():
            if blockType in typeData.keys():
                typeData[blockType] += blockCount[0]
            else:
                typeData[blockType] = blockCount[0]

    for index, counts in enumerate(sessionData):
        sessionData[index] = [counts[0], float(counts[0]) / (totalData if totalData != 0 else 1), counts[1]]
        
    for blockType, blockCount in typeData.items():
        typeData[blockType] = [blockCount, float(blockCount) / totalData]
	

    return [totalData, typeData, sessionData]

def calculateBlocksBySession(userSessions, anonymousSessions):
    userCounts = dict()
    typeCounts = dict()
    totalCount = 0

    userCounts[""] = countSessionSet(anonymousSessions, "[ANONYMOUS]")
    totalCount += userCounts[""][0]
	
    for user, sessions in userSessions.items():
        userCounts[user] = countSessionSet(sessions, user)
        totalCount += userCounts[user][0]

    for user, counts in userCounts.items():
        userCounts[user] = [counts[0], float(counts[0]) / totalCount, counts[1], counts[2]]

        for blockType, blockCount in counts[1].items():
            if blockType in typeCounts.keys():
                typeCounts[blockType] += blockCount[0]
            else:
                typeCounts[blockType] = blockCount[0]

    for blockType, blockCount in typeCounts.items():
        typeCounts[blockType] = [blockCount, float(blockCount) / totalCount]	
		
    return totalCount, typeCounts, userCounts

# TODO: Counts by file / across sessions (pattern)

#--Some users only one login, then never again; count and toss them from long-term trends?
#--Some sessions no user; count and toss them?
#--
#--Do we care about intrasession for blocks? Probably. Eventually break sessions into parts? May not be useful.
#-blocks -> text percentage over time (across sessions)
#-blocks->text switching within a session
#-blocks vs text percentage within a session
#-Change in switching and percentages, week-to-week

def main():
    dataPath = parseArguments()
    print "Loading sessions..."
    userSessions, anonymousSessions = EtFile.loadJsonFile(dataPath)
    print "User data loaded."
    totalCount, typeCounts, userCounts = calculateBlocksBySession(userSessions, anonymousSessions)
    print "Block data extracted."
    EtFile.saveJsonFile("userData.json", [totalCount, userCounts], indent=2, sort_keys=True)
    EtFile.saveJsonFile("typeData.json", [totalCount, typeCounts], indent=2, sort_keys=True)
    print "Block data saved."

if __name__ == "__main__":
    main()

