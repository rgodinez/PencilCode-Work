"""
JSON format:
userX.json
	"sessionId"	:	int
		"logs"
			"code"	:	string
			"mode"	:	string "t" or "b"
			"timestamp"	:	int
			"blocks"
				"id"	:	string
				"count"	:	int
		"sessionTimes"
			"blockModeTime"	:	int
			"textModeTime"	:	int
			"totalTime"	:	int
		"differences"
			"codeDifference"	:	string
			"timeDifference"	:	int
"""