(to extract data from apache logs all the way to organized json data) is like this:

python LogProcessor.py path-to-logs/access-logs-*

It will also automatically unzip gzipped log files and add that data to the set.

~~For Ricardo only: python LogProcessor.py C:/Users/Poxoti/Desktop/Dropbox/PencilCodeDataWork/Feb2015Data/access.log-*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Sessions.json~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
How are SessionSets (sessions.json) organized?

	When read into a variable through EtFile.loadJsonFile(SESSION_PATH/FILE_NAME.json), it is stored as a multi-dimensional array, like so:
	sessions = EtFile.loadJsonFile(session.json)
	
	-	session[#] returns a log entry from the session for a specific IP_ADDRESS
		-	log entries are composed of [ IP_ADDRESS, USER_NAME, LOG_DATA[] ]
			-	IP_ADDRESS
			-	USER_NAME could be an actual user's name, or fit into the various sub-domains of the PencilCode website. If the user is not registered on PencilCode, or logged in, the USER_NAME value will be '-'.
			-	LOG_DATA is a multi-dimensional array composed of all log data for the unique IP_ADDRESS the log entry corresponds to.
				-	LOG_DATA[ENTRY #] holds data for a single entry in the form of a list:
				[0] is the timestamp for the entry, in milliseconds
				[1] is the generic webpage document directory for the website
				[2] is the exact webpage request, composed of Pencil Code program data. This is neatly organized in the next element
				[3] is a dictionary holding the program data from the HTTP request. The following items are the dictionary keys contained 
				(note: the data in the key is in a list, so you need to append a [0] after the key when accessing the actual data, ex. [3]['code'][0] to access the string data within the key 'code')
					['lang'] holds the value representing the programming language the user is submitting their program in
					['code'] holds the code for the program submitted, as a single string. Newlines are represented within the string as bars, '|'; tabs are already accounted for
					['run'] never holds a value
					['mode'] holds the value for what mode the user is viewing the data in, 't' for text and 'b' for block
				[4] holds the HTTP status code
	

