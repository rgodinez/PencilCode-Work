import json

"""
	Credit to https://gist.github.com/sytrus-in-github
	Modified from source to return data as string for use in D3.js
"""

def json2js(jsonfilepath, functionname='getData'):
    """function converting json file to javascript file: json_data -> json_data.js

    :param jsonfilepath: path to json file
    :param functionname: name of javascript function which will return the data

    :return None
    """
    # load json data
    with open(jsonfilepath,'r') as jsonfile:
        data = json.load(jsonfile)
    # write transformed javascript file
    with open(jsonfilepath+'.js', 'w') as jsfile:
		jsfile.write('function '+functionname+'(){return \'')
		jsfile.write(json.dumps(data))
		jsfile.write('\';}')

if __name__ == '__main__':
    from sys import argv
    l = len(argv)
    if l == 2:
        json2js(argv[1])
    elif l == 3:
        json2js(argv[1], argv[2])
    else:
        raise ValueError('Correct syntax: python pathTo/json2js.py jsonfilepath [jsfunctionname]')
