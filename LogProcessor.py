import sys
import argparse

import EtFile

import LogFormatter
import SessionExtractor
import UserSessionExtractor
import BlockAnalyzer

global isDebugging
'''
@summary: Main module entry point.  Handles command line args and starts program.
'''
# TODO: Grab UID; compare with domain on save event.

def parseArguments():
    logPath = None
    isDebugging = False
    # handle command line args
    parser = argparse.ArgumentParser(description='A program to build a CSV file from Pencil Code log files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_help = True
    parser.add_argument('path', help='path of a log file or directory (required)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='display debug information')
    args = parser.parse_args()
    if args.debug:  isDebugging = True
    if args.path: logPath = args.path

    # Path required as parameter
    if not logPath:
        print "Error: no path specified!"
        sys.exit(2)

    # debug program
    if isDebugging:
        print "SYSTEM"
        print sys.version
        print
        
    return logPath

def main():
    logPath = parseArguments()    
    logEntries, errorEntries = LogFormatter.formatFromPath("C:/Users/admin/Desktop/Dropbox/PencilCodeDataWork/Feb2015Data/access.log-20150219") # logPath
    print "Completed log loading: " + str(len(logEntries)) + " entries total."
    EtFile.saveJsonFile("errors.json", errorEntries)
    print "Error entries saved."
    EtFile.saveJsonFile("logs.json", logEntries)
    print "Formatted logs saved."

    sessionSets = SessionExtractor.extractSessionSets(logEntries)
    print "Sessions extracted."
    EtFile.saveJsonFile("sessions.json", sessionSets)	# Ricardo: removed ', 2)' because this would give argument errors
    print "Sessions saved."

    userSessions, anonymousSessions = UserSessionExtractor.extractUserSessions(sessionSets)
    print "User and anonymous sessions grouped and sorted."
    EtFile.saveJsonFile("users.json", [ userSessions, anonymousSessions ])	# Ricardo: removed ', 2)' because this would give argument errors
    print "User and anonymous sessions saved."

    totalCount, typeCounts, userCounts = BlockAnalyzer.calculateBlocksBySession(userSessions, anonymousSessions)
    print "User and general block click data computed."
    EtFile.saveJsonFile("userData.json", [totalCount, userCounts], indent=2, sort_keys=True)
    EtFile.saveJsonFile("typeData.json", [totalCount, typeCounts], indent=2, sort_keys=True)
    print "Block data saved."

if __name__ == "__main__":
    main()
