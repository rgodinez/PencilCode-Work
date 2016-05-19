(to extract data from apache logs all the way to organized json data) is like this:

python LogProcessor.py path-to-logs/access-logs-*

It will also automatically unzip gzipped log files and add that data to the set.

~~For Ricardo only: python LogProcessor.py C:/Users/Poxoti/Desktop/Dropbox/PencilCodeDataWork/Feb2015Data/access.log-*