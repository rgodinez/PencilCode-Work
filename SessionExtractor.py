import os
import sys
import argparse

import EtFile

global isDebugging

def parseArguments():
    logPath = None
    isDebugging = False

    # handle command line args
    parser = argparse.ArgumentParser(description='A program to build a CSV file from Pencil Code log files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_help = True
    parser.add_argument('path', help='path of a pickled log file from formatter (required)')
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

    if not os.path.isfile(logPath):
        print "Error: invalid path specified!"
        print logPath
        sys.exit(2)
        
    return logPath

'''
@summary: Loads and formats logs.

This function will load a list of formatted, sorted log entries and return a sorted list of sessions.
Sessions are determined by a IP and user, with a timespan of no longer than one hour between actions.

Incoming log entry format:
[IPADDRESS, USER, TIME_IN_MS, DOCUMENT, QUERY_STRING, { QUERY_KV_PAIR* }]

Outgoing session log set format:
[IPADDRESS, USER, [ TRUNCATED_LOG_ENTRY* ]]

Truncated log entries do not contain the IP and username as these are redundant; equivalent to LOGENTRY[2:].
'''
def extractSessionSets(logEntries):
    logEntries = sorted(logEntries)
    
    # Extract session data; link IP, domain name, and no more than an hour between log entries.
    sessionLogSets = []

    if len(logEntries) > 0:
        thisSession = logEntries[0][:2]
        sessionEnd = int(logEntries[0][2])
        thisSession.append([])
    else:
        return sessionLogSets

    i = 0
    for entry in logEntries:
        if thisSession[:2] != entry[:2] or sessionEnd + 3600 < int(entry[2]):
            sessionLogSets.append(thisSession)
            thisSession = entry[:2]
            thisSession.append([])

        thisSession[2].append(entry[2:])
        sessionEnd = int(entry[2])
        i = i + 1
    
    return sorted(sessionLogSets)

def main():
    logPath = parseArguments()
    print "Loading logs..."
    logEntries = EtFile.loadJsonFile(logPath)
    print "Logs loaded."
    sessionSets = extractSessionSets(logEntries)
    print "Sessions extracted."
    
#    EtTools.savePickleFile(sessionSets, "sessions.pkl")
    EtFile.saveJsonFile("sessions.json", sessionSets, 2)
    print "Data exported."

if __name__ == "__main__":
    main()
