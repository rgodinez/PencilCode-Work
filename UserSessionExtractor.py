import os
import sys
import argparse

import EtFile
import EtTools

global isDebugging

def parseArguments():
    sessionPath = None
    isDebugging = False
    
    # handle command line args
    parser = argparse.ArgumentParser(description='A program to build a CSV file from Pencil Code log files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_help = True
    parser.add_argument('path', help='path of a pickled log file from formatter (required)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='display debug information')
    args = parser.parse_args()
    if args.debug:  isDebugging = True
    if args.path: sessionPath = args.path

    # Path required as parameter
    if not sessionPath:
        print "Error: no path specified!"
        sys.exit(2)

    # debug program
    if isDebugging:
        print "SYSTEM"
        print sys.version
        print

    if not os.path.isfile(sessionPath):
        print "Error: invalid path specified!"
        sys.exit(2)

    return sessionPath

'''
@summary: Loads and formats logs.

This function will load a list of session log sets, and return a dictionary of user session data.
Sessions are associated definitively with a user by identifying a "save" action which requires
authentication. Sessions that do not contain a "save" action are not associated with a user, but
instead are added to a list of anonymous sessions (as identity cannot be confirmed.)

Incoming session log set format:
[ IPADDRESS, USER, [ TRUNCATED_LOG_ENTRY* ] ]

Outgoing user session data format:
{ (username : [ TRUNCATED_SESSION_ENTRY* ])* }

Truncated session entries do not contain the username as this is redundant; equivalent to SESSION_ENTRY[1:].
'''
def extractUserSessions(sessionLogSets):
    # See if the sessionLogSets can be tied to a specific user; if so, add the session to the userdata.
    userSessions = dict()
    anonymousSessions = []
    
    for session in sessionLogSets:
        username = session.pop(1)
        authenticated = False
        if username == "":
            anonymousSessions.append(session)
            continue

        for entry in session[1]:
            if entry[1][:6] == "/save/":
                if username in userSessions.keys():
                    userSessions[username].append(session)
                else:
                    userSessions[username] = [session]

                # Once the session is added, break out of the loop.
                authenticated = True
                break

        # If the session wasn't added to a user, add it to the anonymous list.
        if not authenticated:
            anonymousSessions.append(session)
            
    for username in userSessions.keys():
        # If the user had only one authenticated entry, it is treated as anonymous
        # (since no trend data can be retreived.)
        if len(userSessions[username]) == 1:
            del userSessions[username]
            anonymousSessions.append(session) 

    return userSessions, sorted(anonymousSessions)

def main():
    sessionPath = parseArguments()
    print "Loading sessions..."
    sessionSets = EtFile.loadJsonFile(sessionPath)
    print "Sessions loaded."
    userSessions, anonymousSessions = extractUserSessions(sessionSets)
    print "User data extracted."

    EtFile.saveJsonFile("users.json", [ userSessions, anonymousSessions ], 2)
    print "User data saved."

if __name__ == "__main__":
    main()
