import os
import sys
import argparse
import glob
import re
import urlparse
import time
import calendar

import EtFile
import EtTools

global isDebugging

'''
@summary: Handles command line arguments and determines path(s).
'''
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
        print "SYSTEM" + " " + sys.version + "\n"

    return logPath

'''
@summary: Loads and formats logs.

This function will load, format, sort, and return a list of log entries.

Incoming log entry format:
'IPADDRESS USER UID [DD/Mmm/YYYY:HH:MM:SS +####] "REQUEST" STATUS SIZE REFERRER BROWSER'

Outgoing log entry format:
[IPADDRESS, USER, TIME_IN_MS, DOCUMENT, QUERY_STRING, { QUERY_KV_PAIR* }]
'''
def formatFromPath(logPath):
    logEntries = []
    errorEntries = []

    toBeLogged = ['log', 'error', 'load', 'save', 'home']
#    toBeSkipped = ['', 'lib', 'edit', 'worksheet', 'material', 'search', 'image']

    # load data and process
    logPaths = glob.glob(logPath)

    if len(logPaths) == 0:
        if not os.path.isfile(logPath) and not os.path.isdir(logPath):
            print "Error: invalid path specified!"
            sys.exit(2)
        logPaths = [logPath]

    # First, follow all directories and add their children to the path set.
    for path in logPaths:
        if os.path.isdir(path):
            print "Adding directory " + path + "..."
            logPaths.extend(EtFile.getFilesRecursive(path))

    # Once directories have been address, go through the individual logs.
    for path in logPaths:
        print "Processing " + path + "..."
        if os.path.isfile(path):
            logFile = EtFile.openFile(path, 'r')
    
            for line in logFile:
                row = map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', line))
                
                if len(row) == 0:
                    continue
        
				# Ricardo: added status code to entry data
                ipAddress, username, __, accessTime, request, status = row[:6]

                requestSplit = request.split(" ")
                if len(requestSplit) < 2:
                    print "Can't process request: " + str(row)
                    errorEntries.append(line)
                    continue
                else:
                    resourceUrl = request.split(" ")[1]
        
                resource = urlparse.urlparse(resourceUrl)
                document = resource.path
        
                diffSec = int(accessTime[-5:-4] + "1") * (int(accessTime[-2:]) + int(accessTime[-4:-2]) * 60) * 60
                accessTime = calendar.timegm(time.strptime(accessTime[:-6], "%d/%b/%Y:%H:%M:%S")) - diffSec
                queries = urlparse.parse_qs(EtTools.decodeString(resource.query), True)
                
                if document[1:document[1:].find('/')+1] in toBeLogged:
                    logEntries.append([ipAddress, username, accessTime, document, EtTools.decodeString(resourceUrl), queries, status])
        
    logEntries = sorted(logEntries)
    return logEntries, errorEntries

'''
@summary: Main module entry point.
'''
def main():
    logPath = parseArguments()
    logEntries, errorEntries = formatFromPath(logPath)
    print "Completed log loading: " + str(len(logEntries)) + " entries total."

    EtFile.saveJsonFile("logs.json", logEntries)
    EtFile.saveJsonFile("errors.json", errorEntries)
#    EtFile.savePickleFile(logEntries, "logs.pkl")

if __name__ == "__main__":
    main()
